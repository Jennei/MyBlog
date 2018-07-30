#!usr/bin/env python  
# -*- coding:utf-8 -*-

""" 
@author:    nico 
@file:      filters.py 
@time:      2018/07/30 
"""

from blog.models import Post

from django_filters import rest_framework as filters


class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'parent': ['exact'],
            'id': ['exact'],
            'title': ['iexact'],
            'tags': ['iexact'],
            'status': ['exact'],
            'published_time': ['year__lte', 'year__gte', 'month__gte', 'month__lte', 'day__lte', 'day__gte']
        }
