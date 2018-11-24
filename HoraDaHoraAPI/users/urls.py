from django.urls import path
from users import views

urlpatterns = [
    path('', views.UserList.as_view(), name='users'),
    path('<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('profile/', views.ProfileList.as_view(), name='profile'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('abilities/', views.AbilitiesList.as_view(), name='abilities'),
]