from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer
from .serializers import IssueSerializer, CommentSerializer
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('project_id')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all().order_by('user_id')
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all().order_by('-created_time')
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_time')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
