from django.shortcuts import render, reverse
from django.views import generic
from .mixins import OrganiserandLoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelform
from django.core.mail import send_mail
import random

class AgentListView(OrganiserandLoginRequiredMixin, generic.ListView):
    template_name="agents/agent_list.html"

    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(OrganiserandLoginRequiredMixin, generic.CreateView):
    template_name='agents/agent_create.html'
    form_class=AgentModelform

    def form_valid(self, form):
        user=form.save(commit=False)
        user.is_agent=True
        user.is_organizer=False
        user.set_password(str(random.randint(0, 1000)))
        user.save()
        Agent.objects.create(
            user=user, 
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject="New Agent",
            message="you are invited as an agent",
            from_email="sarvarusmn@gmail.com",
            recipient_list=[user]
        )
        return super(AgentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('agents:agent-list')

class AgentDetailview(OrganiserandLoginRequiredMixin, generic.DetailView):
    template_name='agents/agent_detail.html'
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    context_object_name="agent"


class AgentUpdateview(OrganiserandLoginRequiredMixin, generic.UpdateView):
    template_name='agents/agent_update.html'
    form_class=AgentModelform
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    
    def get_success_url(self):
        return reverse('agents:agent-list')


class AgentDeleteview(OrganiserandLoginRequiredMixin, generic.DeleteView):
    template_name='agents/agent_delete.html'
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    def get_success_url(self):
        return reverse('agents:agent-list')
    

