from django.urls import path

from . import views


app_name = "polls"
urlpatterns = [
    #ex: /polls/
    path('', views.IndexView.as_view(), name='index'),

    #ex: /polls/6/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    #ex: /polls/6/results
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),

    #ex: /polls/6/vote
    path('<int:question_id>/vote', views.vote, name='vote'),
]