"""Defines URL patterns for my_top_tens."""

from django.urls import path
from . import views

app_name = 'my_top_tens'

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('manage_ranks/<int:topic_id>/', views.manage_ranks, name='manage_ranks'),
    path('topics/<int:topic_id>/edit_description/', views.edit_topic_description, name='edit_topic_description'),
    path('select_topic_to_delete/', views.select_topic_to_delete, name='select_topic_to_delete'),
    path('delete_topic/', views.delete_topic, name='delete_topic'),
]