import json

from django.db import models
from django.urls import reverse


class Poll(models.Model):
    title = models.CharField(max_length=32, unique=True, verbose_name='Наименование')
    date0 = models.DateField(db_index=True, verbose_name='Дата начала')
    date1 = models.DateField(db_index=True, verbose_name='Дата окончания')
    comments = models.CharField(max_length=255, null=True, blank=True, verbose_name='Комментарии')

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('poll_view', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Quest(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, db_index=True, editable=True, verbose_name='Опрос')
    title = models.CharField(max_length=255, blank=False, verbose_name='Вопрос')
    mult = models.BooleanField(db_index=True, verbose_name='Multichoice',
                               help_text="&#9744;=radio, &#9745;=checkboxes")
    payload = models.TextField(null=True, blank=True, verbose_name='Варианты',
                               help_text="Empty: text answer, multiline text: radio/checkboxes (1 line == 1 item)")

    def __str__(self):
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('poll_view', kwargs={'pk': self.poll.pk})

    def get_type(self) -> int:
        """Return type of record.
        :return: 0=str, 1=radio, 2=checkboxes
        """
        return 0 if not self.payload else (1 if not self.mult else 2)

    def get_char(self) -> str:
        """Get html type representation"""
        return ("&#9997;", "&#9872;", "&#9745;")[self.get_type()]

    def get_list(self) -> list:
        """Get payload as list"""
        return self.payload.split("\r\n") if self.payload else None

    class Meta:
        ordering = ('poll', 'pk')
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    cust_id = models.PositiveIntegerField(db_index=True, verbose_name="Пользователь")
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, db_index=True, verbose_name='Вопрос')
    resume = models.CharField(max_length=255, null=False, blank=False, verbose_name="Ответ")

    def __str__(self):
        data = json.loads(self.resume)
        if qtype := self.quest.get_type():   # radio/checkboxes
            if qtype == 1:  # radio
                return self.quest.get_list()[data]
            else:           # checboxes
                return ','.join(list(self.quest.get_list()[i] for i in data))
        else:               # str
            return data

    class Meta:
        ordering = ('cust_id', 'quest')
        unique_together = (('cust_id', 'quest'),)
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
