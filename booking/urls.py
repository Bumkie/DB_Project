
from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.theater_list, name='theater_list'),
    path('reservation/<int:theater_id>/', views.reservation, name='reservation'),
    path('booking_detail/<int:screening_id>/', views.booking_detail, name='booking_detail'),
    path('create/', views.create_booking, name='create_booking'),
    path('check/', views.check_booking, name='check_booking'),
]
