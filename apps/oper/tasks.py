# -*- coding:utf-8 -*-
__author__ = 'Ren Kang'
__date__ = '2018/4/23 17:28'


from django.db.models import ObjectDoesNotExist
from django.core.cache import cache
from django.contrib.auth import get_user_model
from blog.tasks import task_lock


from celery import shared_task
from celery.utils.log import get_task_logger

from oper.models import NotificationUnReadCounter


logger = get_task_logger(__name__)
User = get_user_model()
key_template = "oper:notification:%s"


@shared_task(bind=True)
def update_n_unread(self, user_id, value):
    """
    更新用户未读数量
        1. 若缓存中存在用户的未读数，更新缓存。
        2. 若缓存中不存在， 则在缓存中新建用户的未读计数器。
    :param user_id:
    :param value:
    :return:
    """
    key = key_template%user_id
    logger.debug('update_n_unread key[%s] value[%s]' % (key, value))

    if cache.has_key(key):
        return cache.incr(key, value)
    else:
        return cache.set(key, value, None)


@shared_task(bind=True)
def get_n_unread(self, user_id):
    """
    获取用户未读消息数量
        1. 若缓存中存在，直接返回。
        2. 若缓存中不存在，从数据库读取到缓存。
    :param user_id:
    :return:
    """
    key = key_template % user_id

    if cache.has_key(key):
        return cache.get(key)
    else:
        user = User.objects.get(pk=user_id)
        try:
            nt_c = NotificationUnReadCounter.objects.get(user=user)
        except NotificationUnReadCounter.DoesNotExist as e:
            cache.set(key, 0, None)
        else:
            cache.set(key, nt_c.n_unread, None)

        return cache.get(key)


@shared_task(bind=True)
def mark_as_read(self, user_id, notification_id):
    from oper.models import Notification
    #写成一条语句，更新has_read，相当于把这些操作看成一次事务，自动加锁。
    #这样如果并发时有多个请求更改has_read的操作，其它请求会等待在第一个请求执行完has_read=True
    #最后其它请求就会知道has_read已经为True了。
    #这里的has_read会被竞争性访问修改，只有保证了这一步的原子性，下一步原子更新未读数才有意义。
    affected_rows = Notification.objects.filter(pk=notification_id, has_read=False).update(has_read=True)
    update_n_unread.delay(user_id, -affected_rows)


@shared_task(bind=True)
def sync_n_unread(self):
    """
    定时任务
    1. 将缓存中的未读数同步到数据库
    2. 如果缓存中没有计数器，直接返回
    3. 如果缓存中存在计数器，则更新数据库的计数器
    4. 如果缓存中的计数和数据库相同，则不做更新
    :param self:
    :return:
    """
    lock_key = __name__ + ".mutex_lock"

    with task_lock(lock_key, self.app.oid) as aquired:
        if aquired:
            if any(filter(lambda x: x.startswith('oper:notification:'), cache.keys('*'))):
                for c in filter(lambda x: x.startswith('oper:notification:'), cache.keys('*')):
                    user_id = c.split(':').pop()
                    try:
                        user = User.objects.get(pk=user_id)
                    except User.DoesNotExist as e:
                        return True

                    cache_n_unread = cache.get(c)

                    try:
                        nt_c = NotificationUnReadCounter.objects.get(user=user)
                    except ObjectDoesNotExist as e:
                        affect_rows = NotificationUnReadCounter.objects.create(user=user, n_unread=cache_n_unread)
                        logger.debug('sync_n_unread user[%s] user_id[%s] n_unread[%s] affect_rows[%s]' % (user, user_id, cache_n_unread, affect_rows))
                        continue

                    if cache_n_unread != nt_c.n_unread:
                        affect_rows = NotificationUnReadCounter.objects.filter(user=user).update(n_unread=cache_n_unread)
                        logger.debug('sync_n_unread user[%s] user_id[%s] n_unread[%s] affect_rows[%s]' % (user, user_id, cache_n_unread, affect_rows))
                    else:
                        logger.debug('sync_n_unread idle user[%s] user_id[%s] n_unread[%s] affect_rows[%s]' % (user, user_id, cache_n_unread, 0))
                return True
            else:
               return False
        else:
            logger.debug('sync_n_unread is already being worked by another worker')
            return False