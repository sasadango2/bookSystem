from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path('profile/', views.member_profile, name="member_profile"),
    path('register/', views.member_register, name="member_register"),
    path('notifications/', views.notification_list, name="notification_list"),
    path('mark_notification_read/<int:notification_id>/', views.mark_notification_read, name="mark_notification_read"),
]
