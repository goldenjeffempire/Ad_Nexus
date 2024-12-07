from django.urls import path
from .views import ad_recommendations, ad_simulation

urlpatterns = [
    path('recommendations/', ad_recommendations, name='ad_recommendations'),
    path('simulate/<int:ad_id>/', ad_simulation, name='ad_simulation'),
]
