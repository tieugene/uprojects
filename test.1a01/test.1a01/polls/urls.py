from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('p/', login_required(views.PollList.as_view()), name='poll_list'),
    path('p/a/', login_required(views.PollCreate.as_view()), name='poll_add'),
    path('p/<int:pk>/', login_required(views.PollDetail.as_view()), name='poll_view'),
    path('p/<int:pk>/e/', login_required(views.PollUpdate.as_view()), name='poll_edit'),
    path('p/<int:pk>/d/', login_required(views.PollDelete.as_view()), name='poll_del'),
    path('p/<int:pk>/a/', login_required(views.QuestCreate.as_view()), name='quest_add'),
    path('q/<int:pk>/e/', login_required(views.QuestUpdate.as_view()), name='quest_edit'),
    path('q/<int:pk>/d/', login_required(views.QuestDelete.as_view()), name='quest_del'),
    path('c/', login_required(views.CustList.as_view()), name='cust_list'),
    path('c/<int:cid>/', login_required(views.CustVotes.as_view()), name='cust_votes'),
    path('c/<int:cid>/<int:pid>/', login_required(views.CustAnswers.as_view()), name='cust_answers'),
]
