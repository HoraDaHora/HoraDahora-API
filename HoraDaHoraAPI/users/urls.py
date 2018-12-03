from django.urls import path
from users import views

urlpatterns = [
    path('', views.UserList.as_view(), name='users'),
    path('<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('profile/', views.ProfileList.as_view(), name='profile'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('abilities/', views.AbilitiesList.as_view(), name='abilities'),
    path('abilities/<int:pk>/', views.AbilitiesUpdate.as_view(), name='abilities-update'),
    path('availability/', views.AvailabilityList.as_view(), name='availability'),
    path('availability/<int:pk>/', views.AvailabilityUpdate.as_view(), name='availability-update'),
    path('availabilityUser/<int:pk>/', views.AvailabilityUser.as_view(), name='availability-update'),
]