from django.urls import path
from .views import CounterView, metrics_view

urlpatterns = [
    path('', CounterView.as_view(), name='counter'),
    path('metrics/', metrics_view, name='metrics'),
]

