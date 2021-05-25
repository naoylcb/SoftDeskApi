from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from .models import Project, Issue, Comment
from .utils import extract_ids, is_contributor


class CanReadOrEditProject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return is_contributor(request.user, obj)

        return obj.author_user_id == request.user


class CanReadOrEditUser(permissions.BasePermission):

    def has_permission(self, request, view):
        # Extract project id from the url.
        ids = extract_ids(request.path)
        project = get_object_or_404(Project, project_id=ids[0])

        if request.method == "GET":
            return is_contributor(request.user, project)

        return project.author_user_id == request.user


class CanReadOrEditIssue(permissions.BasePermission):

    def has_permission(self, request, view):
        # Extract ids from the url.
        ids = extract_ids(request.path)
        project = get_object_or_404(Project, project_id=ids[0])

        if request.method == 'PUT' or request.method == 'DELETE':
            try:
                Issue.objects.get(id=ids[1], author_user_id=request.user,
                                  project_id=project)
            except Issue.DoesNotExist:
                return False
            return True

        return is_contributor(request.user, project)


class CanReadOrEditComment(permissions.BasePermission):

    def has_permission(self, request, view):
        # Extract ids from the url.
        ids = extract_ids(request.path)

        if request.method == 'PUT' or request.method == 'DELETE':
            try:
                Comment.objects.get(comment_id=ids[2],
                                    author_user_id=request.user,
                                    issue_id=ids[1])
            except Comment.DoesNotExist:
                return False
            return True

        project = get_object_or_404(Project, project_id=ids[0])
        return is_contributor(request.user, project)
