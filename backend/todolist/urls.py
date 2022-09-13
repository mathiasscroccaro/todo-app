from django.contrib import admin

from django.urls import path

from todolist.views import (
    TasksView,
    TaskDetailsView,
    logout_view,
    login_view
)


urls = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('tasks/', TasksView.as_view()),
    path('tasks/<task_id>/', TaskDetailsView.as_view()),
]
