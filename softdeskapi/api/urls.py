from django.urls import path

from . import views

app_name = 'api'

project_list = views.ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

project_detail = views.ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', views.api_root),
    path('projects/', project_list, name='projects'),
    path('projects/<int:pk>/', project_detail),
    path('projects/<int:p_id>/users/', views.UserView.as_view()),
    path('projects/<int:p_id>/users/', views.UserView.as_view()),
    path('projects/<int:p_id>/users/<int:pk>/', views.UserView.as_view()),
    path('projects/<int:p_id>/issues/', views.IssueView.as_view()),
    path('projects/<int:p_id>/issues/', views.IssueView.as_view()),
    path('projects/<int:p_id>/issues/<int:pk>/', views.IssueView.as_view()),
    path('projects/<int:p_id>/issues/<int:pk>/', views.IssueView.as_view()),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/',
         views.CommentView.as_view()),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/',
         views.CommentView.as_view()),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/<int:pk>/',
         views.CommentView.as_view()),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/<int:pk>/',
         views.CommentView.as_view()),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/<int:pk>/',
         views.CommentView.as_view()),
]    