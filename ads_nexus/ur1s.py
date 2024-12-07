from django.urls import path
from .views import ad_recommendations

urlpatterns = [
    path('recommendations/', ad_recommendations, name='ad_recommendations'),
]
