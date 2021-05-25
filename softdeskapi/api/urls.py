from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

app_name = 'api'

api_root = views.ApiRootView.as_view()
login = TokenObtainPairView.as_view()
registration = views.RegistrationView.as_view()
project_list = views.ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
project_detail = views.ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
user_list = views.UserView.as_view()
user_detail = views.UserDetailView.as_view()
issue_list = views.IssueView.as_view()
issue_detail = views.IssueDetailView.as_view()
comment_list = views.CommentView.as_view()
comment_detail = views.CommentDetailView.as_view()

urlpatterns = [
    path('', api_root),
    path('login/', login),
    path('signup/', registration),
    path('projects/', project_list, name='projects'),
    path('projects/<int:pk>/', project_detail),
    path('projects/<int:p_id>/users/', user_list),
    path('projects/<int:p_id>/users/<int:pk>/', user_detail),
    path('projects/<int:p_id>/issues/', issue_list),
    path('projects/<int:p_id>/issues/<int:pk>/', issue_detail),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/', comment_list),
    path('projects/<int:p_id>/issues/<int:i_id>/comments/<int:pk>/',
         comment_detail),
]
