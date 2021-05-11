from django.urls import path
from . import views

app_name = 'app-research'

urlpatterns = [

    path('', views.index, name='home-page'),
    path('recommend-keywords/', views.recommend_keywords, name='recommend-paper-keywords'),
    path('recommend-abstract/', views.recommend_abstract, name='recommend-paper-abstract'),
    path('download/<str:filepath>/', views.download_file, name='recommend-paper-download'),

]
