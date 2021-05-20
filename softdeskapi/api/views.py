from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer
from .serializers import IssueSerializer, CommentSerializer
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        projects_list = []

        for project in self.queryset:
            if Contributor.objects.filter(user_id=request.user,
                                          project_id=project):
                projects_list.append(project)

        serializer = ProjectSerializer(projects_list, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post'])
    def users(self, request, pk=None):
        if request.method == 'GET':
            project = self.get_object()
            contributors = Contributor.objects.filter(project_id=project)
            p_users = [c.user_id for c in contributors]
            serializer = UserSerializer(p_users, many=True,
                                        context={'request': request})
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ContributorSerializer(data=request.data,
                                               context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='users/(?P<id>[^/.]+)')
    def del_user(self, request, id, pk=None):
        project = self.get_object()
        contributor = Contributor.objects.filter(user_id=id,
                                                 project_id=project)
        if contributor:
            contributor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
