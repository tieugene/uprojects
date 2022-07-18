"""DRF [de]serializers"""
import json
from rest_framework import serializers
from polls import models


class PollSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Poll
        fields = '__all__'
        # fields = ['pk', 'title', 'date0', 'date1', 'comments', 'quest_set']
        # depth = 2


class QuestSerializer(serializers.ModelSerializer):
    qtype = serializers.SerializerMethodField()
    qitems = serializers.SerializerMethodField()

    class Meta:
        model = models.Quest
        fields = ['pk', 'title', 'qtype', 'qitems']

    def get_qtype(self, quest):
        """Answer type:
        0: str,
        1: radio,
        2: checkboxes
        """
        return quest.get_type()

    def get_qitems(self, quest):
        """Items to choose for radio/chackboxes qtype
        ('null' for str).
        """
        return quest.get_list()


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Poll
        fields = ['id']


class AnswerSerializer(serializers.ModelSerializer):
    resume = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = ['quest_id', 'resume']

    def get_resume(self, answer):
        """Overwrites default serializer with jsoner"""
        return str(answer)


class AnswerDeSerializer(serializers.ModelSerializer):
    resume = serializers.JSONField(required=True)

    class Meta:
        model = models.Answer
        fields = ['cust_id', 'quest', 'resume']

    def validate_resume(self, resume):
        """Validate resume and converts it to str.
        :param resume: Value to check/convert
        :return: resume string representation
        :except:
        - [ ] TODO: bad type
        - [ ] TODO: out of range (str len = 1..255 or radio/checkbox index)
        - [ ] TODO: checkboxes: dups (=> set())
        """
        if isinstance(resume, str):
            if len(resume) > 253:
                raise serializers.ValidationError(f"String too big.")
        return json.dumps(resume, ensure_ascii=False)
