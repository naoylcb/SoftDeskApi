from django.db import models
from django.conf import settings


class Project(models.Model):
    BACKEND = 'back-end'
    FRONTEND = 'front-end'
    IOS = 'iOS'
    ANDROID = 'Android'
    TYPES_LIST = [
        (BACKEND, BACKEND),
        (FRONTEND, FRONTEND),
        (IOS, IOS),
        (ANDROID, ANDROID)
    ]

    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=128, choices=TYPES_LIST)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)


class Contributor(models.Model):

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    class Meta:
        unique_together = ('user_id', 'project_id')


class Issue(models.Model):
    LOW = 'FAIBLE'
    MEDIUM = 'MOYENNE'
    HIGH = 'ÉLEVÉE'
    PRIORITIES_LIST = [
        (LOW, LOW),
        (MEDIUM, MEDIUM),
        (HIGH, HIGH)
    ]

    BUG = 'BUG'
    IMPROVEMENT = 'AMÉLIORATION'
    TASK = 'TÂCHE'
    TAGS_LIST = [
        (BUG, BUG),
        (IMPROVEMENT, IMPROVEMENT),
        (TASK, TASK)
    ]

    TODO = 'À faire'
    INPROGRESS = 'En cours'
    FINISHED = 'Terminé'
    STATUS_LIST = [
        (TODO, TODO),
        (INPROGRESS, INPROGRESS),
        (FINISHED, FINISHED)
    ]

    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=1024)
    tag = models.CharField(max_length=128, choices=TAGS_LIST)
    priority = models.CharField(max_length=128, choices=PRIORITIES_LIST)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=128, choices=STATUS_LIST)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='created_by')
    assignee_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                         on_delete=models.CASCADE,
                                         related_name='assigned_to')
    created_time = models.DateTimeField(auto_now_add=True, editable=False)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1024)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, editable=False)
