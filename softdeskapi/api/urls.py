from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

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
    path('', views.ApiRootView.as_view()),
    path('login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('signup/', views.RegistrationView.as_view()),
    path('projects/', project_list, name='projects'),
    path('projects/<int:pk>/', project_detail),
    path('projects/<int:p_id>/users/', views.UserView.as_view()),
    path('projects/<int:p_id>/users/<int:pk>/',
         views.UserDetailView.as_view()),
    path('projects/<int:p_id>/issues/', views.IssueView.as_view()),
    path('projects/<int:p_id>/issues/<int:pk>/',
         views.IssueDetailView.as_view()),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/',
         views.CommentView.as_view()),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/<int:pk>/',
         views.CommentDetailView.as_view()),
]
