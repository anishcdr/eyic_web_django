    # myapp/urls.py
from django.urls import path
from . import views
from .views import ReceiveDataFromRoverAPIView


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('npk/', views.grid_section_detail, name='npk'),
    path('water/', views.moisture, name='water'),
    #path('receive_data_from_rover/', views.receive_data_from_rover, name='receive_data_from_rover'),
    path('receive_data_from_rover/', ReceiveDataFromRoverAPIView.as_view(), name='receive_data_from_rover'),
]
