from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Project, Contributor, Issue, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type',
                  'author_user_id']


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
