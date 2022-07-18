"""REST views"""
import datetime
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
# from rest_framework import viewsets
from rest_framework.response import Response
from polls import models
from . import serials


class GetPollList(GenericAPIView):
    """Get polls available today."""
    serializer_class = serials.PollSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        today = datetime.date.today()
        objects = models.Poll.objects.all().filter(date0__lte=today).filter(date1__gte=today)
        result = serials.PollSerializer(objects, many=True)
        return Response(result.data)


class GetPollQuests(GenericAPIView):
    """Get poll questions."""
    serializer_class = serials.QuestSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pid):
        objects = models.Quest.objects.all().filter(poll_id=pid)
        result = serials.QuestSerializer(objects, many=True)
        return Response(result.data)


class GetVotes(GenericAPIView):
    """Get customer votes."""
    serializer_class = serials.VoteSerializer
    permission_classes = (AllowAny,)

    def get(self, request, cid):
        objects = models.Poll.objects.filter(quest__answer__cust_id=cid).distinct()
        print(objects.count())
        result = serials.VoteSerializer(objects, many=True)
        return Response(result.data)


class GetAnswers(GenericAPIView):
    """Get customer answers."""
    serializer_class = serials.AnswerDeSerializer
    permission_classes = (AllowAny,)

    def get(self, request, cid, pid):
        quests = models.Answer.objects.filter(cust_id=cid, quest__poll_id=pid)
        result = serials.AnswerSerializer(quests, many=True)
        return Response(result.data)


class AddAnswer(GenericAPIView):
    """Add new customer's answer."""
    serializer_class = serials.AnswerDeSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        answer = serials.AnswerDeSerializer(data=request.data, context=request)
        if answer.is_valid(raise_exception=True):
            answer.save()
            return Response({'result': 'OK'})
