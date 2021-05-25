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
from .utils import serialize


class ApiRootView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({
            'projects': reverse('api:projects', request=request, format=format)
        })


class RegistrationView(APIView):
    """View for user registration."""
    def post(self, request, format=None):
        return serialize(UserSerializer, request.data)


class UserView(APIView):
    """View for get project's contributors or add a contributor."""
    permission_classes = [IsAuthenticated and CanReadOrEditUser]

    def get(self, request, p_id, format=None):
        project = get_object_or_404(Project, pk=p_id)
        contributors = Contributor.objects.filter(project_id=project)
        p_users = [c.user_id for c in contributors]
        serializer = UserSerializer(p_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, p_id, format=None):
        request.data['project_id'] = p_id
        return serialize(ContributorSerializer, request.data)


class UserDetailView(APIView):
    """View for remove a project's contributor."""
    permission_classes = [IsAuthenticated and CanReadOrEditUser]

    def delete(self, request, p_id, pk, format=None):
        contributor = get_object_or_404(Contributor, user_id=pk,
                                        project_id=p_id)
        contributor.delete()
        return Response(status=status.HTTP_200_OK)


class IssueView(APIView):
    """View for get project's issues or add a issue."""
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
        try:
            Contributor.objects.get(user_id=request.data['assignee_user_id'],
                                    project_id=p_id)
        except Contributor.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return serialize(IssueSerializer, request.data)


class IssueDetailView(APIView):
    """View for edit or delete an issue."""
    permission_classes = [IsAuthenticated and CanReadOrEditIssue]

    def put(self, request, p_id, pk, format=None):
        issue = get_object_or_404(Issue, pk=pk, project_id=p_id)
        request.data['project_id'] = issue.project_id.project_id
        request.data['author_user_id'] = issue.author_user_id.id
        request.data['assignee_user_id'] = issue.assignee_user_id.id

        return serialize(IssueSerializer, request.data, issue)

    def delete(self, request, p_id, pk, format=None):
        issue = get_object_or_404(Issue, pk=pk, project_id=p_id)
        issue.delete()
        return Response(status=status.HTTP_200_OK)


class CommentView(APIView):
    """View for get issue's comments or add a comment."""
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

        return serialize(CommentSerializer, request.data)


class CommentDetailView(APIView):
    """View for get, edit or delete a comment."""
    permission_classes = [IsAuthenticated and CanReadOrEditComment]

    def get_comment(self, p_id, i_id, pk):
        issue = get_object_or_404(Issue, pk=i_id, project_id=p_id)
        return get_object_or_404(Comment, pk=pk, issue_id=issue)

    def get(self, request, p_id, i_id, pk, format=None):
        comment = self.get_comment(p_id, i_id, pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, p_id, i_id, pk, format=None):
        comment = self.get_comment(p_id, i_id, pk)
        request.data['issue_id'] = comment.issue_id.id
        request.data['author_user_id'] = comment.author_user_id.id

        return serialize(CommentSerializer, request.data, comment)

    def delete(self, request, p_id, i_id, pk, format=None):
        comment = self.get_comment(p_id, i_id, pk)
        comment.delete()
        return Response(status=status.HTTP_200_OK)


class ProjectViewSet(viewsets.ModelViewSet):
    """View for list, create, get, edit or delete project."""
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
