from django.urls import path

from apps.notifications.views import NotificationReadAPIView, UnreadNotificationListView

urlpatterns = [
    path("unread/", UnreadNotificationListView.as_view(), name="unread-notifications"),
    path("<int:pk>/read/", NotificationReadAPIView.as_view(), name="notification-read"),
]
