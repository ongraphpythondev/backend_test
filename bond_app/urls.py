from django.urls import path
from . import views

app_name = "bond_app"

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login',views.login, name = 'login'),
    path('logout',views.logout, name = 'logout'),

    path('publishbond', views.publish_bond, name='publishbond'),
    path('bondlist', views.bond_list, name='bondlist'),
    path('buybond', views.buy_bond, name='buybond'),
    path('listinusdollar', views.bond_list_usdollar, name='listinusdollar'),
]


