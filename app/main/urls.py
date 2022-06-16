from django.urls import path
from main.views import home, graphics, alerts, payment, balance, set_left_menu_session

urlpatterns=[
    path('', home, name='home'),
    path('graphics/', graphics, name='graphics'),
    path('alerts/', alerts, name='alerts'),
    path('payment/', payment, name='payment'),
    path('balance/', balance, name='balance'),
    path('set_left_menu_session/', set_left_menu_session, name='set_left_menu_session'),
]
