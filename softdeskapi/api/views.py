from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer
from .serializers import IssueSerializer, CommentSerializer
from .serializers import UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'projects': reverse('api:projects', request=request, format=format)
    })


class UserView(APIView):

    def get(self, request, p_id, format=None):
        project = get_object_or_404(Project, pk=p_id)
        contributors = Contributor.objects.filter(project_id=project)
        p_users = [c.user_id for c in contributors]
        serializer = UserSerializer(p_users, many=True)
        return Response(serializer.data)

    def post(self, request, p_id, format=None):
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, p_id, pk, format=None):
        contributor = get_object_or_404(Contributor, user_id=pk,
                                        project_id=p_id)
        contributor.delete()
        return Response(status=status.HTTP_200_OK)


class IssueView(APIView):

    def get(self, request, p_id, format=None):
        project = get_object_or_404(Project, pk=p_id)
        issues = Issue.objects.filter(project_id=project)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, p_id, format=None):
        request.data['project_id'] = p_id
        request.data['author_user_id'] = request.user.id
        request.data['assignee_user_id'] = request.data.get(
            'assignee_user_id', request.user.id)

        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, p_id, pk, format=None):
        issue = get_object_or_404(Issue, pk=pk, project_id=p_id)
        request.data['project_id'] = issue.project_id.project_id
        request.data['author_user_id'] = issue.author_user_id.id
        request.data['assignee_user_id'] = issue.assignee_user_id.id

        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, p_id, pk, format=None):
        issue = get_object_or_404(Issue, pk=pk, project_id=p_id)
        issue.delete()
        return Response(status=status.HTTP_200_OK)


class CommentView(APIView):

    def get(self, request, p_id, i_id, pk=None, format=None):
        issue = get_object_or_404(Issue, pk=i_id, project_id=p_id)
        if pk is None:
            comments = Comment.objects.filter(issue_id=issue)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        else:
            comment = get_object_or_404(Comment, pk=pk, issue_id=issue)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

    def post(self, request, p_id, i_id, format=None):
        issue = get_object_or_404(Issue, pk=i_id, project_id=p_id)
        request.data['issue_id'] = issue.id
        request.data['author_user_id'] = request.user.id

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, p_id, i_id, pk, format=None):
        issue = get_object_or_404(Issue, pk=i_id, project_id=p_id)
        comment = get_object_or_404(Comment, pk=pk, issue_id=issue)
        request.data['issue_id'] = comment.issue_id.id
        request.data['author_user_id'] = comment.author_user_id.id

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, p_id, i_id, pk, format=None):
        issue = get_object_or_404(Issue, pk=i_id, project_id=p_id)
        comment = get_object_or_404(Comment, pk=pk, issue_id=issue)
        comment.delete()
        return Response(status=status.HTTP_200_OK)


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
