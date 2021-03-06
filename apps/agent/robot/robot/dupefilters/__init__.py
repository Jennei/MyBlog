#!usr/bin/env python  
#-*- coding:utf-8 -*-

""" 
@author:    nico 
@file:      __init__.py.py 
@time:      2018/08/31 
"""

import os
import logging

from scrapy.dupefilters import BaseDupeFilter, RFPDupeFilter
from scrapy.utils.request import request_fingerprint
from scrapy.utils.job import job_dir

from scrapy_redis.connection import get_redis_from_settings

from robot.dupefilters import bloomfilter_memory, bloomfilter_redis


logger = logging.getLogger('dupefilters')


class BloomFilterRedis(BaseDupeFilter):
    def __init__(self, n=100000000, f=0.0001, server=None, block_nums=1, key_prefix='BLOOMFILTER', *args, **kwargs):

        self.bf = bloomfilter_redis.BloomFilter(n, f, server, block_nums, key_prefix)
        self.debug = kwargs.get('debug', True)
        self.logdupes = True

    @classmethod
    def from_settings(cls, settings):
        server = get_redis_from_settings(settings)
        key_prefix = settings.get("BLOOMFILTER_REDIS_KEY_PREFIX", "BLOOMFILTER")
        capacity = settings.get("BLOOMFILTER_REDIS_CAPACITY", 100000000)
        error_rate = settings.get("BLOOMFILTER_REDIS_FALSE_POSITIVE_PROBABILITY", 0.0001)
        block_nums = settings.get("BLOOMFILTER_REDIS_BLOCK_NUMS", 1)
        debug = settings.getbool('DUPEFILTER_DEBUG', False)
        return cls(capacity, error_rate, server, block_nums, key_prefix, debug=debug)

    @classmethod
    def from_spider(cls, spider):
        settings = spider.settings
        server = get_redis_from_settings(settings)
        key_prefix = settings.get("BLOOMFILTER_REDIS_KEY_PREFIX", "BLOOMFILTER")
        capacity = settings.get("BLOOMFILTER_REDIS_CAPACITY", 100000000)
        error_rate = settings.get("BLOOMFILTER_REDIS_FALSE_POSITIVE_PROBABILITY", 0.0001)
        block_nums = settings.get("BLOOMFILTER_REDIS_BLOCK_NUMS", 1)
        debug = settings.getbool('DUPEFILTER_DEBUG', False)
        return cls(capacity, error_rate, server, block_nums, key_prefix, debug=debug)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if fp in self.bf:
            return True
        else:
            self.bf.add(fp)

        return False

    def open(self):
        pass

    def close(self, reason):
        if self.bf.key:
            self.bf.server.delete(self.bf.key)

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            logger.debug(msg, {'request': request}, extra={'spider': spider})
        self.logdupes = False


class BloomFilterMemory(RFPDupeFilter):
    def __init__(self, n=100000000, f=0.0001, block_nums=1, *args, **kwargs):

        self.bf = bloomfilter_memory.BloomFilter(n, f, block_nums)
        self.debug = kwargs.get('debug', True)
        self.logdupes = True
        super(BloomFilterMemory, self).__init__(*args, **kwargs)

    @classmethod
    def from_settings(cls, settings):
        capacity = settings.get("BLOOMFILTER_MEMORY_CAPACITY", 100000000)
        error_rate = settings.get("BLOOMFILTER_MEMORY_FALSE_POSITIVE_PROBABILITY", 0.0001)
        block_nums = settings.get("BLOOMFILTER_MEMORY_BLOCK_NUMS", 1)
        debug = settings.getbool('DUPEFILTER_DEBUG', False)
        return cls(capacity, error_rate, block_nums, debug=debug, path=job_dir(settings))

    @classmethod
    def from_spider(cls, spider):
        settings = spider.settings
        capacity = settings.get("BLOOMFILTER_MEMORY_CAPACITY", 100000000)
        error_rate = settings.get("BLOOMFILTER_MEMORY_FALSE_POSITIVE_PROBABILITY", 0.0001)
        block_nums = settings.get("BLOOMFILTER_MEMORY_BLOCK_NUMS", 1)
        debug = settings.getbool('DUPEFILTER_DEBUG', False)
        return cls(capacity, error_rate, block_nums, debug=debug, path=job_dir(settings))

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if fp in self.bf:
            return True
        else:
            self.bf.add(fp)
            if self.file:
                self.file.write(fp + os.linesep)

        return False

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            logger.debug(msg, {'request': request}, extra={'spider': spider})
        self.logdupes = False