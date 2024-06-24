from django.urls import path
from .views import (
    StoneListView, StoneDetailView, StoneCreateView, StoneUpdateView, StoneDeleteView,
    FlangeListView, FlangeCreateView, FlangeUpdateView, FlangeDeleteView,
    StoneHandlingCreateView, StoneHandlingListView, StoneHandlingStep1View, StoneHandlingStep2View, StoneHandlingStep3View
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

    path('oldstonehandling/new/', StoneHandlingCreateView.as_view(), name='stonehandling_create'),
    path('oldstonehandling/', StoneHandlingListView.as_view(), name='stonehandling_list'),

    path('stonehandling/', StoneHandlingStep1View.as_view(), name='stonehandling_step1'),
    path('stonehandling/step2/', StoneHandlingStep2View.as_view(), name='stonehandling_step2'),
    path('stonehandling/step3/', StoneHandlingStep3View.as_view(), name='stonehandling_step3'),
    
]
