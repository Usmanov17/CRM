from django import forms
from django.core.exceptions import ValidationError
from .models import Lead, User, Agent, Category, FollowUp
from django.contrib.auth.forms import UserCreationForm, UsernameField


class ModelformLead(forms.ModelForm):
    class Meta:
        model=Lead
        fields=(
            'first_name', 
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
            'profile_picture',
        )


    def clean(self):
        first_name=self.cleaned_data['first_name']
        if len(first_name)<3:
            raise ValidationError('at least 3 characters')


    # def clean_first_name(self):
    #         data = self.cleaned_data['first_name']  
    #         if data != 'Joe':                   #     these lines of codes mean that if name of the lead is not joe there will be validation error
    #             raise ValidationError('your name is no joe')




    #class Leadfrom(forms.Form)
    # first_name=forms.CharField()
    # last_name=forms.CharField()
    # age=forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm): #why we are ceating user form even usercreationform can handle everything, because in the beginning we 
#created our own custom user for this reason django can't use its default user when we want to create a new user, that's why to prevent
#the error we are creating customusercreationform 
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

class AssignAgentform(forms.Form):
    agent=forms.ModelChoiceField(queryset=Agent.objects.none()) #why we set none becaus we want to override wueryset each time it rendered
    #because we want to specify agents that belongs to specific organisation

    def __init__(self, *args, **kwargs): #we are goin to check request user from this init method, and based that reuest user we can filter agents
        #that belongs to specific organisation
        request=kwargs.pop('request') 
        agents=Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentform, self).__init__(*args,**kwargs)
        self.fields['agent'].queryset=agents #here we saying that agent of the form equals to the agents which is filtered according organisat

class Leadcategoryupdateform(forms.ModelForm):
    class Meta:
        model=Lead
        fields=(
            'category',
        )

class CategoryModelform(forms.ModelForm):
    class Meta:
        model=Category
        fields=(
            'name',
        )

class FollowupForm(forms.ModelForm):
    class Meta:
        model=FollowUp
        fields=(
            'notes',
            'file',
        )