from django.urls import path
from .views import (
    StoneListView, StoneDetailView, StoneCreateView, StoneUpdateView, StoneDeleteView,
    FlangeListView, FlangeCreateView, FlangeUpdateView, FlangeDeleteView,
    StoneHandlingCreateView, StoneHandlingListView
)

urlpatterns = [
    path('stones/', StoneListView.as_view(), name='stone_list'),
    path('stones/<int:pk>/', StoneDetailView.as_view(), name='stone_detail'),
    path('stones/new/', StoneCreateView.as_view(), name='stone_create'),
    path('stones/<int:pk>/edit/', StoneUpdateView.as_view(), name='stone_update'),
    path('stones/<int:pk>/delete/', StoneDeleteView.as_view(), name='stone_delete'),

    path('flanges/', FlangeListView.as_view(), name='flange_list'),
    path('flanges/new/', FlangeCreateView.as_view(), name='flange_create'),
    path('flanges/<int:pk>/edit/', FlangeUpdateView.as_view(), name='flange_update'),
    path('flanges/<int:pk>/delete/', FlangeDeleteView.as_view(), name='flange_delete'),

    path('stonehandling/new/', StoneHandlingCreateView.as_view(), name='stonehandling_create'),
    path('stonehandling/', StoneHandlingListView.as_view(), name='stonehandling_list'),
]
