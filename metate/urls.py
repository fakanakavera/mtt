from django.urls import path
from .views import (
    StoneListView, StoneDetailView, StoneCreateView, StoneUpdateView, StoneDeleteView
)

urlpatterns = [
    path('stones/', StoneListView.as_view(), name='stone_list'),
    path('stones/<int:pk>/', StoneDetailView.as_view(), name='stone_detail'),
    path('stones/new/', StoneCreateView.as_view(), name='stone_create'),
    path('stones/<int:pk>/edit/', StoneUpdateView.as_view(), name='stone_update'),
    path('stones/<int:pk>/delete/', StoneDeleteView.as_view(), name='stone_delete'),
]
