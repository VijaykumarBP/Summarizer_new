from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='/'),
    path('reviews/<str:pk>/', views.reviews, name='reviews'),
    path('review_back/<str:pk>/', views.review_back, name='review_back'),
    path('summary_form',views.summary, name='summary_form')
]