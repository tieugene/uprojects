"""REST urls (actions)"""
from django.urls import path

from . import views

urlpatterns = [
    path('p/', views.GetPollList.as_view()),
    path('p/<int:pid>/', views.GetPollQuests.as_view()),
    path('v/<int:cid>/', views.GetVotes.as_view()),
    path('v/<int:cid>/<int:pid>/', views.GetAnswers.as_view()),
    path('a/', views.AddAnswer.as_view()),
]
