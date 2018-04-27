from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('group/<int:group_id>', views.group_view, name='groupview'),
    path('start', views.start_game, name='startgame'),
    path('user/<int:user_id>', views.view_user, name='viewuser'),
    path('game', views.continue_game, name='game'),
    path('endgame', views.end_game, name='endgame'),
    path('losegame', views.lose_game, name='losegame'),
]
