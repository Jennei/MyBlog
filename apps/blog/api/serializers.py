#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:    nico 
@file:      serializers.py 
@time:      2018/05/03 
"""

from rest_framework import serializers

from blog.models import Category, Post, Tag, Resources


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, parent):
        queryset = parent.get_children()
        serializer = CategoryTreeSerializer(queryset, many=True, read_only=True, context=self.context)

        return serializer.data

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'children']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, parent):
        queryset = parent.get_children()
        serializer = PostTreeSerializer(queryset, many=True, read_only=True, context=self.context)

        return serializer.data

    class Meta:
        model = Post
        exclude = (
            'lft',
            'rght',
            'tree_id',
            'level'
        )


class BasePostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        extra_kwargs = {
            'url': {'view_name': "blog:post-detail"},
            'parent': {'view_name': "blog:post-detail"},
            'children': {'view_name': "blog:post-detail"},
            'category': {'view_name': "blog:category-detail"},
            'tags': {'view_name': "blog:tag-detail"},
            'author': {'view_name': 'bloguser:user-detail'}
        }


class PostListSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        fields = (
            'url',
            'title',
            'excerpt',
            'cover_url',
            'n_praise',
            'n_comments',
            'n_browsers',
            'published_time'
        )


class PostSerializer(BasePostSerializer):
    children = serializers.SerializerMethodField()
    category = CategorySerializer()

    def get_children(self, parent):
        queryset = parent.get_children()
        serializer = PostListSerializer(queryset, many=True, read_only=True, context=self.context)

        return serializer.data

    class Meta(BasePostSerializer.Meta):
        exclude = (
            'lft',
            'rght',
            'tree_id',
            'level'
        )


class PostDetailSerializer(PostSerializer):
    tags = TagSerializer(many=True)

    class Meta(PostSerializer.Meta):
        pass


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = "__all__"
