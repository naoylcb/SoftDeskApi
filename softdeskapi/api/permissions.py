from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from .models import Project, Issue, Comment
from .utils import extract_ids, is_contributor


class CanReadOrEditProject(permissions.BasePermission):
    """
    Permission to only allow contributors to access projects.
    Permission to only allow authors of a project to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return is_contributor(request.user, obj)

        return obj.author_user_id == request.user


class CanReadOrEditUser(permissions.BasePermission):
    """
    Permission to only allow contributors to see project's contributors.
    Permission to only allow project's authors to add or remove a contributor.
    """
    def has_permission(self, request, view):
        # Extract project id from the url.
        ids = extract_ids(request.path)
        project = get_object_or_404(Project, project_id=ids[0])

        if request.method == "GET":
            return is_contributor(request.user, project)

        return project.author_user_id == request.user


class CanReadOrEditIssue(permissions.BasePermission):
    """
    Permission to only allow contributors to access project's issues.
    Permission to only allow issue's authors to edit it.
    """
    def has_permission(self, request, view):
        # Extract ids from the url.
        ids = extract_ids(request.path)
        project = get_object_or_404(Project, project_id=ids[0])

        if request.method == 'PUT' or request.method == 'DELETE':
            issue = get_object_or_404(Issue, id=ids[1], project_id=project)
            return issue.author_user_id == request.user

        return is_contributor(request.user, project)


class CanReadOrEditComment(permissions.BasePermission):
    """
    Permission to only allow contributors to access issue's comments.
    Permission to only allow comment's authors to edit it.
    """
    def has_permission(self, request, view):
        # Extract ids from the url.
        ids = extract_ids(request.path)

        if request.method == 'PUT' or request.method == 'DELETE':
            comment = get_object_or_404(Comment, comment_id=ids[2],
                                        issue_id=ids[1])
            return comment.author_user_id == request.user

        project = get_object_or_404(Project, project_id=ids[0])
        return is_contributor(request.user, project)
