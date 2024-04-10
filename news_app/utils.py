from django.db.models import Count

from . import models
from .models import News, Comment


def get_most_popular_news():
    # Eng ko'p ko'rilgan yangiliklarni olish
    most_popular_news = News.objects.order_by('-views')[:5]
    return most_popular_news

def get_most_read_news():
    # Eng ko'p o'qilgan yangiliklarni olish
    most_read_news = News.objects.order_by('-read_count')[:5]
    return most_read_news

def get_recent_comments():
    # Eng so'nggi kommentlar ro'yxatini olish
    recent_comments = Comment.objects.order_by('-created_time')[:5]
    return recent_comments

def get_most_commented_news():
    most_commented_news = News.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:5]
    return most_commented_news