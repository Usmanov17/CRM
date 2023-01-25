from django.contrib import admin
from .models import User, Agent, Lead, Userprofile, Category, FollowUp


class LeadAdmin(admin.ModelAdmin):
    # fields=(
    #     'category',
    #     'agent'
    # )

    list_display=['first_name',  'last_name'] #here you write name of fields you want to display in admin panel

    list_display_links=['first_name'] # in this case you can only see lead information by clicking its last name

    list_editable=['last_name'] # this means you can edit first without entering inside of sspecific lead in admin
    
    list_filter=['category'] # it filters model by its one specific field in this case it is filtering by category   
     
    search_fields=['first_name',  'last_name'] #it allows you to search things my fields 

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Userprofile)
admin.site.register(Agent)
admin.site.register(Lead, LeadAdmin)
admin.site.register(FollowUp)
 
