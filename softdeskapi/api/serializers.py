from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type']


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'role']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'assignee_user_id',
                  'created_time']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'description', 'author_user_id', 'issue_id',
                  'created_time']
