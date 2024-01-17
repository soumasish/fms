from django.urls import path
from rest_framework.routers import SimpleRouter

from fleet.views import TaskCreateView

router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    path('task/create/', TaskCreateView.as_view(), name='task-create'),
] + router.urls

