from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.http.response import JsonResponse
from .models import Lead, Agent, Category, FollowUp
from .forms import ModelformLead, CustomUserCreationForm, AssignAgentform, Leadcategoryupdateform, CategoryModelform, FollowupForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganiserandLoginRequiredMixin
import logging
import datetime

logger=logging.getLogger(__name__)
#CRUD+L create retrieve update delete list

class SignupView(CreateView):
    template_name='registration/signup.html'
    form_class=CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class Landingview(TemplateView):
    template_name='landing.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


# def landing_page(request):
#     return render(request, 'landing.html')

class DashboardView(OrganiserandLoginRequiredMixin, TemplateView):
    template_name='dashboard.html'

    def get_context_data(self, **kwargs):
        context=super(DashboardView, self).get_context_data(**kwargs)

        user=self.request.user

        # How many leads we have in total
        total_lead_count=Lead.objects.filter(organisation=user.userprofile).count()
        
        # How many new leads in the last 30 days
        thirthy_days_ago=datetime.date.today() - datetime.timedelta(days=30)

        total_in_past30=Lead.objects.filter(
            organisation=user.userprofile,
            date_added__gte=thirthy_days_ago,
        ).count()

        # How many converted leads in the last 30 days
        converted_category=Category.objects.get(name="Converted")
        converted_in_past30=Lead.objects.filter(
            organisation=user.userprofile,
            category=converted_category,
            converted_date__gte=thirthy_days_ago
        ).count

        context.update({
            'total_lead_count':total_lead_count,
            'total_in_past30':total_in_past30,
            'converted_in_past30':converted_in_past30
        })

        return context

class LeadListview(LoginRequiredMixin, ListView):
    template_name='leads/lead_list.html' 
    context_object_name='leads'  # if we don't do this django sets default context name object_list and we should give this name for html to
    def get_queryset(self):
        user=self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset=Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else: 
            queryset=Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            #filter for the agent that is logged in
            queryset=queryset.filter(agent__user=user)#double underscore means filter the lead based on agent field where that agent
#has a user equal to self.request.user
        logger.warning('You entered to Leadlistview')
        return queryset
    
    def get_context_data(self, **kwargs):
        user=self.request.user
        context=super(LeadListview, self).get_context_data(**kwargs) #by using super command and kwargs we are grabbing an already existing content 
        if user.is_organizer:
            queryset=Lead.objects.filter(organisation=user.userprofile,
            agent__isnull=True) # when you you check for the foreign keyn you use __ agent is the name of the foreign key
            context.update({
                'unassigned_leads':queryset
            }) #inside update method we pass dictionary of context that we want to pass in, this how we pass context to class based view
        return context
            


    #iterate but if you give context name you kay give it in html
    # def lead_list(request):
#     leads=Lead.objects.all()
#     context={
#         'leads':leads
#     }
#     return render(request, 'leads/lead_list.html', context)

class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
# def lead_detail(request, pk):
#     lead=Lead.objects.get(id=pk)
#     context={
#         "lead":lead
#     }
#     return render(request, 'leads/lead_detail.html', context )

class LeadCreateView(OrganiserandLoginRequiredMixin,CreateView):
    template_name='leads/lead_create.html'
    form_class=ModelformLead

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, 'Lead have successfuly created')
        return super(LeadCreateView, self).form_valid(form)
# def lead_create(request):  #CREATING FORM WITH DJANGO'S MODEL NAMELY MODELFORM
#     form=ModelformLead()
#     if request.method=='POST':
#         form=ModelformLead(request.POST)
#         form.save()
#         return redirect('/leads')
#     context={
#      'form':form
#     }
#     return render(request, 'leads/lead_create.html', context)

class LeadUpdateView(OrganiserandLoginRequiredMixin, UpdateView):
    template_name='leads/lead_update.html'
    form_class=ModelformLead
    def get_queryset(self):
        user=self.request.user
        if user.is_organizer:
            return Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "Lead have successfully updated")
        return super(LeadUpdateView, self).form_valid(form)
# def lead_update(request, pk):
#     lead=Lead.objects.get(id=pk)
#     form=ModelformLead(instance=lead) #from instance djago will know wether we are creating a form or updating, instance will create new instance of model
#     if request.method=='POST':
#         form=ModelformLead(request.POST, instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect('/leads')
     # context={
    #  'form':form
    # }
    # return render(request, 'leads/lead_update.html', context)


class LeadDeleteView(OrganiserandLoginRequiredMixin, DeleteView):
    template_name='leads/lead_delete.html'
    def get_queryset(self):
        user=self.request.user
        if user.is_organizer:
            return Lead.objects.filter(organisation=user.userprofile)
    def get_success_url(self):
        return reverse("leads:lead-list")
# def lead_delete(request, pk):
#     lead=Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect('/leads')

class Assignagentview(OrganiserandLoginRequiredMixin, FormView):
    template_name='leads/assign_agent.html'
    form_class=AssignAgentform

    def get_form_kwargs(self, **kwargs): # by this method we can pass the form extra information
        kwargs=super(Assignagentview, self).get_form_kwargs(**kwargs)
        kwargs.update({ #this dictionary contains want we to pass to the form as a extra keywordarguments
            'request':self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent=form.cleaned_data['agent']
        lead=Lead.objects.get(id=self.kwargs['pk'])
        lead.agent=agent
        lead.save()
        return super(Assignagentview, self).form_valid(form)

class CategoryListview(LoginRequiredMixin, ListView):
    template_name='leads/category_list.html'
    context_object_name='category_list'

    def get_context_data(self, **kwargs):
        context=super(CategoryListview, self).get_context_data(**kwargs) 
        user=self.request.user

        if user.is_organizer:
            queryset=Lead.objects.filter(organisation=user.userprofile)
        else: 
            queryset=Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
                'unassigned_lead_count':queryset.filter(category__isnull=True).count()
            })
        return context

    def get_queryset(self):
        user=self.request.user
        if user.is_organizer:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else: 
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class CategoryDetailview(LoginRequiredMixin, DetailView):
    template_name='leads/category_detail.html'
    context_object_name='category'

    # def get_context_data(self, **kwargs):
    #     context=super(CategoryDetailview, self).get_context_data(**kwargs)
    #     leads=Lead.objects.filter(category=self.get_object()) #get object method will fetch the whichever model that you are working with (in the detailview)
    #     #self.get_object().lead_set.all() it does the same thing as the code above
    #     #self.get_object.leads.all() after giving relationship name you can like this
    #     context.update({
    #             'leads':leads
    #         })
    #     return context
    def get_queryset(self):
        user=self.request.user
        if user.is_organizer:
            queryset=Category.objects.filter(organisation=user.userprofile)
        else: 
            queryset=Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name='leads/lead_category_update.html'
    form_class=Leadcategoryupdateform
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset           

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={'pk':self.get_object().id})

    def form_valid(self, form):
        lead_before_update=self.get_object()
        instance=form.save(commit=False)
        converted_category=Category.objects.get(name="Converted")
        if form.cleaned_data['category'] == converted_category:
            if lead_before_update.category != converted_category:
                instance.converted_date=datetime.datetime.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)

class CategoryCreateview(OrganiserandLoginRequiredMixin, CreateView):
    template_name='leads/category_create.html'
    form_class=CategoryModelform

    def get_success_url(self):
        return reverse("leads:category-list")
    
    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateview, self).form_valid(form)

class CategoryUpdateView(OrganiserandLoginRequiredMixin, UpdateView):
    template_name='leads/category_update.html'
    form_class=CategoryModelform

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_success_url(self):
        return reverse("leads:category-list")

class CategoryDeleteView(OrganiserandLoginRequiredMixin, DeleteView):
    template_name='leads/category_delete.html'
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:category-list") 

class FollowupcreateView(LoginRequiredMixin, CreateView):
    template_name='leads/followup_create.html'
    form_class=FollowupForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context=super(FollowupcreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowupcreateView, self).form_valid(form)

class FollowupUpdateView(LoginRequiredMixin, UpdateView):
    template_name='leads/followup_update.html'
    form_class=FollowupForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().lead.id})

class FollowUpdeleteview(OrganiserandLoginRequiredMixin, DeleteView):
    template_name='leads/followup_delete.html'

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organizer:
            queryset = FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.lead.pk})

class LeadJsonView(View):
    def get(self, request, *args, **kwargs):
        qs=list(Lead.objects.all().values('first_name')) #why we are makeing list bcause json only contains dict and list

        return JsonResponse({
            'qs':qs
        })
