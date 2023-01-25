from django.urls import path
from leads.views import (
    LeadCreateView, LeadUpdateView, LeadDeleteView,
    LeadListview, LeadDetailView, Assignagentview,
    CategoryListview, CategoryDetailview, LeadCategoryUpdateView, CategoryCreateview, CategoryUpdateView, 
    CategoryDeleteView, LeadJsonView, FollowupcreateView, FollowUpdeleteview, FollowupUpdateView
     )

app_name="leads"


urlpatterns = [
    path('', LeadListview.as_view(), name='lead-list'),
    path('json/', LeadJsonView.as_view(), name='lead-json'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('lead-create/', LeadCreateView.as_view(), name='lead-create'),

    path('<int:pk>/assign-agent/', Assignagentview.as_view(), name='assign-agent'),

    path('category/', CategoryListview.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailview.as_view(), name='category-detail'),
    path('create-category/', CategoryCreateview.as_view(), name='category-create'),
    path('categories/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),

   path('<int:pk>/followups/create/', FollowupcreateView.as_view(), name='lead-followup-create'),
    path('followups/<int:pk>/', FollowupUpdateView.as_view(), name='lead-followup-update'),
    path('followups/<int:pk>/delete/', FollowUpdeleteview.as_view(), name='lead-followup-delete'),

]