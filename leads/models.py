from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
     # pass- it means we not going to add or made change we are just inheriteng features of abstractuser and that's enough
     is_organizer=models.BooleanField(default=True)
     is_agent=models.BooleanField(default=False)

class Userprofile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

def post_user_created_signal(sender, instance , created, **kwargs): #instance is the actual model that was saved, created tells us wether or not the model is created
    if created:
        Userprofile.objects.create(user=instance)
post_save.connect(post_user_created_signal, sender=User)

    

class Agent(models.Model): #in this code we making the user agentp
    user=models.OneToOneField(User, on_delete=models.CASCADE) #in this key we don't use foreing key because it allows to create 
#many agents for one user, but we want to create one agent for one user in this case we use onetoonefield()
    organisation=models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email


class Category(models.Model):
    name=models.CharField(max_length=30) #NEw  contacted converted unconverted
    organisation=models.ForeignKey(Userprofile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class BlankManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(category__isnull=True)

class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    # def get_age_below_50(self):
    #     return self.get_queryset().filter(age__lt=50) #by means of this method we can filter leads who ate under 50
    #     #Lead.objects.get_age_below_50()

class Lead(models.Model):
    # SOURCE_FIELD=(
    #     ('Youtube', 'Youtube'),
    #     ('Google', 'Google'),
    #     ('Newsletter', 'Newsletter')  
    # ) # the first value will be soted in database the second will be displayed
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    age=models.IntegerField(default=0) #it means it should not be less than 0
    organisation=models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    agent=models.ForeignKey(Agent, null=True, blank=True,  on_delete=models.SET_NULL) #on delete say django that how to handle when the given class(foreignkey)
    category=models.ForeignKey(Category, related_name='leads', null=True, blank=True,  on_delete=models.SET_NULL)
    # will be deleted, cascade means when the given foreingkey(class, Agent) will be  deleted, delete the class(Lead),  both delete
# another option is SET_NULL, it sets value of a foreign key to null, in order to use it we should set null to True
# third option is SET_DEFAULT, it helps us if we set value to default like default='something', and it will set default value if agent will be deleted
    description=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    phone_number=models.CharField(max_length=20)
    email=models.EmailField()
    objects=LeadManager
    profile_picture=models.ImageField()
    converted_date=models.DateTimeField(null=True, blank=True)
    # blank_objects=BlankManager #this manager filter categories which are blank lead.blan_objects.all() if you write like this it return blank categories    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # phoned=models.BooleanField(default=False)
    # source=models.CharField(choices=SOURCE_FIELD, max_length=100)
    # profile_picture=models.ImageField(blank=True, null=True) #it means it is optional, blan and null is the different thing
    # #blank means empty string, null means there is no value in database
    # special_files=models.FileField(blank=True, null=True)

def handle_upload_followups(instance, filename):
    return f"lead_followups/lead_{instance.lead.pk}/{filename}"

class FollowUp(models.Model):
    lead=models.ForeignKey(Lead, related_name='followups', on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)
    notes=models.TextField(blank=True, null=True)
    file=models.FileField(blank=True, null=True, upload_to=handle_upload_followups)

    def __str__(self):
        return f"{self.lead.first_name} {self.lead.first_name}"