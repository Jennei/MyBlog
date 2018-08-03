#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:    nico 
@file:      serializers.py 
@time:      2018/05/03 
"""

from rest_framework import serializers, reverse
from drf_writable_nested import NestedCreateMixin, NestedUpdateMixin

from blog.models import Category, Post, Tag, Resources
from blog import enums
from blog.api import fields


class CategoryTreeSerializer(NestedCreateMixin, NestedUpdateMixin, serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    author = serializers.HyperlinkedRelatedField(view_name='bloguser:user-detail', read_only=True)
    url = serializers.SerializerMethodField()
    parent = fields.CategoryParentField(queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ['id', 'url', 'name', 'author', 'parent', 'children']

    def get_url(self, instance):
        return reverse.reverse("blog:category-detail", request=self.context['request'], kwargs={"pk": instance.id})

    def get_children(self, parent):
        queryset = parent.get_children()
        serializer = CategoryTreeSerializer(queryset, many=True, read_only=True, context=self.context)

        return serializer.data

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.author = self.context["request"].user
        instance.save()
        return instance

    def validate_parent(self, parent):
        if parent.author != self.context["request"].user:
            raise serializers.ValidationError('你只能使用自己的分类')

        return parent


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class TagDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('url', 'name', 'author')
        extra_kwargs = {
            'url': {'view_name': "blog:tag-detail"},
            'author': {'view_name': 'bloguser:user-detail', "read_only": True}
        }


    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.author = self.context["request"].user
        instance.save()
        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', )


class PostArchiveSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    post_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_url(self, date):
        return reverse.reverse('blog:post-list', request=self.context["request"]) + "?published_time__year=" + str(
            date.year) + "&published_time__month=" + str(date.month)

    def get_post_count(self, date):
        queryset = self.context['queryset']
        ar_list = queryset.filter(published_time__year=date.year, published_time__month=date.month)
        return ar_list.count()


class BasePostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        extra_kwargs = {
            'url': {'view_name': "blog:post-detail"},
            'parent': {'view_name': "blog:post-detail"},
            'children': {'view_name': "blog:post-detail"},
            'category': {'view_name': "blog:category-detail"},
            'tags': {'view_name': "blog:tag-detail"},
            'author': {'view_name': 'bloguser:user-detail', "read_only": True}
        }


class PostListSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = (
            'url',
            'title',
            'author',
            'excerpt',
            'cover',
            'n_praise',
            'n_comments',
            'n_browsers',
            'published_time'
        )


class PostSerializer(NestedCreateMixin, NestedUpdateMixin, BasePostSerializer):
    parent = fields.PostParentField(
        queryset=Post.objects.filter(status=enums.POST_STATUS_PUBLIC, post_type=enums.POST_TYPE_POST),
        view_name="blog:post-detail"
    )

    class Meta(BasePostSerializer.Meta):
        fields = (
            'url',
            'title',
            'category',
            'tags',
            'author',
            'content',
            'cover',
            'status',
            'post_type',
            'is_free',
            'parent'
        )
        read_only_fields = ("tags" ,)

    def validate_parent(self, parent):
        if parent.author != self.context["request"].user:
            raise serializers.ValidationError('你只能使用自己博文')

        return parent

    def create(self, validated_data):
        post = super().create(validated_data)
        post.author = self.context["request"].user
        post.save()
        return post


class PostDetailSerializer(BasePostSerializer):
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    children = serializers.SerializerMethodField()

    def get_children(self, parent):
        queryset = parent.get_children()
        serializer = PostListSerializer(queryset, many=True, read_only=True, context=self.context)
        return serializer.data

    class Meta(BasePostSerializer.Meta):
        exclude = (
            'lft',
            'rght',
            'tree_id',
            'level',
            'cover_url'
        )


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = "__all__"
