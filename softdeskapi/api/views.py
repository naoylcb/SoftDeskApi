from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
    UserSerializer,
)
from .permissions import (
    CanReadOrEditProject,
    CanReadOrEditUser,
    CanReadOrEditIssue,
    CanReadOrEditComment
)


class ApiRootView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({
            'projects': reverse('api:projects', request=request, format=format)
        })


class RegistrationView(APIView):

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated and CanReadOrEditUser]

    def get(self, request, p_id, format=None):
        project = get_object_or_404(Project, pk=p_id)
        contributors = Contributor.objects.filter(project_id=project)
        p_users = [c.user_id for c in contributors]
        serializer = UserSerializer(p_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, p_id, format=None):
        request.data['project_id'] = p_id
        serializer = ContributorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated and CanReadOrEditUser]

    def delete(self, request, p_id, pk, format=None):
        contributor = get_object_or_404(Contributor, user_id=pk,
                                        project_id=p_id)
        contributor.delete()
        return Response(status=status.HTTP_200_OK)


class IssueView(APIView):
    permission_classes = [IsAuthenticated and CanReadOrEditIssue]

    def get(self, request, p_id, format=None):
        project = get_object_or_404(Project, pk=p_id)
        issues = Issue.objects.filter(project_id=project)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, p_id, format=None):
        request.data['project_id'] = p_id
        request.data['author_user_id'] = request.user.id
        request.data['assignee_user_id'] = request.data.get(
            'assignee_user_id', request.user.id)

        # Verify that assignee_user_id is a project contributor.
        get_object_or_404(
            Contributor,
            user_id=request.data['assignee_user_id'],
            project_id=p_id
        )

        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetailView(APIView):
    permission_classes = [IsAuthenticated and CanReadOrEditIssue]

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
    permission_classes = [IsAuthenticated and CanReadOrEditComment]

    def get(self, request, p_id, i_id, format=None):
        issue = get_object_or_404(Issue, pk=i_id, project_id=p_id)
        comments = Comment.objects.filter(issue_id=issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, p_id, i_id, format=None):
        issue = get_object_or_404(Issue, pk=i_id, project_id=p_id)
        request.data['issue_id'] = issue.id
        request.data['author_user_id'] = request.user.id

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated and CanReadOrEditComment]

    def get(self, request, p_id, i_id, pk, format=None):
        issue = get_object_or_404(Issue, pk=i_id, project_id=p_id)
        comment = get_object_or_404(Comment, pk=pk, issue_id=issue)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    permission_classes = [IsAuthenticated and CanReadOrEditProject]

    def list(self, request):
        projects_list = []

        for p in self.queryset:
            if Contributor.objects.filter(user_id=request.user, project_id=p):
                projects_list.append(p)

        serializer = ProjectSerializer(projects_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data['author_user_id'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['author_user_id'] = request.user.id
        return super().update(request, *args, **kwargs)
