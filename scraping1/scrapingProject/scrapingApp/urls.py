from django.urls import path
from  scrapingApp  import views

app_name = 'scrapingApp'
urlpatterns = [
    path('user_login',views.user_login ,name="user_login"),
    path('register',views.register ,name="register"),
    path('moviename',views.moviename ,name="moviename"),
    path('output',views.outputInfo ,name="output"),

]