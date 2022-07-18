from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic import CreateView, UpdateView, DeleteView

from . import models

PAGE_SIZE = 25


class PollList(ListView):
    """List polls"""
    model = models.Poll
    # template_name = 'polls/poll_list.html'
    # paginate_by = PAGE_SIZE


class PollDetail(DetailView):
    """Poll details"""
    model = models.Poll
    # template_name = 'polls/poll_detail.html'


class PollCreate(CreateView):
    """Add new poll.
    FIXME: chk date1 >= date0
    """
    model = models.Poll
    fields = ['title', 'date0', 'date1', 'comments']
    # template_name = 'polls/poll_form.html'


class PollUpdate(UpdateView):
    """Edit poll.
    FIXME: chk date1 >= date0
    """
    model = models.Poll
    fields = ['title', 'date1', 'comments']
    # template_name = 'polls/poll_form.html'


class PollDelete(DeleteView):
    """Delete poll."""
    model = models.Poll
    # template_name = 'polls/poll_delete.html'
    success_url = reverse_lazy('poll_list')


class QuestCreate(CreateView):
    """Add new question to a poll."""
    model = models.Quest
    fields = ['title', 'mult', 'payload']
    poll_id = object = None  # helpers

    def dispatch(self, request, *args, **kwargs):
        self.poll_id = int(kwargs['pk'])
        return super().dispatch(request, args, kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.poll = models.Poll.objects.get(pk=self.poll_id)
        self.object.save()
        return super().form_valid(form)


class QuestUpdate(UpdateView):
    """Edit question"""
    model = models.Quest
    fields = ['title', 'mult', 'payload']


class QuestDelete(DeleteView):
    """Delete question."""
    model = models.Quest
    success_url = reverse_lazy('poll_list')

    def dispatch(self, request, *args, **kwargs):
        poll_id = models.Quest.objects.get(pk=kwargs['pk']).poll_id
        self.success_url = reverse_lazy('poll_view', args=[poll_id])
        return super().dispatch(request, args, kwargs)


class CustList(ListView):
    """List of customers voted."""
    template_name = 'polls/cust_list.html'

    def get_queryset(self):
        return set(models.Answer.objects.values_list('cust_id', flat=True))


class CustVotes(ListView):
    """List of customer's votes."""
    template_name = 'polls/cust_votes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cid'] = self.kwargs['cid']
        return context

    def get_queryset(self):
        return models.Poll.objects.filter(quest__answer__cust_id=self.kwargs['cid']).distinct()


class CustAnswers(ListView):
    """List of customer's answers for the poll."""
    template_name = 'polls/cust_answers.html'

    def get_queryset(self):
        cust_id = self.kwargs['cid']
        poll_id = self.kwargs['pid']
        return models.Answer.objects.filter(cust_id=cust_id, quest__poll_id=poll_id)
