from django.urls import path
from .views import AgentListView, AgentCreateView, AgentDetailview, AgentUpdateview, AgentDeleteview


app_name='agents'
urlpatterns=[
     path("", AgentListView.as_view(), name='agent-list'),
     path('create/', AgentCreateView.as_view(), name='agent-create'),
     path('detail/<pk>', AgentDetailview.as_view(), name='agent-detail'),
     path('<int:pk>/update/', AgentUpdateview.as_view(), name='agent-update'),
     path('<int:pk>/delete/', AgentDeleteview.as_view(), name='agent-delete'),
]