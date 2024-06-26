from django.urls  import path, include
from . import views

urlpatterns = [
    path('todos/', views.TodoList.as_view(), name='todo-list'), #List all todos
    path('todos1/', views.TodoListCreate.as_view()),
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()),
    path('signup/', views.signup),
    path('login/', views.login),
    path('rest-auth/', include('dj_rest_auth.urls')),
]