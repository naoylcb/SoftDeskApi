from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'groups']


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type']


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ['title', 'desc', 'tag', 'priority', 'project_id', 'status',
                  'author_user_id', 'assignee_user_id', 'created_time']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'description', 'author_user_id', 'issue_id',
                  'created_time']
