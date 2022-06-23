
from .views import *
from django.urls import path



urlpatterns = [
    path('', index, name='home'),
    path('UserInfo/log/', log, name='log'),

]

