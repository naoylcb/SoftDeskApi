from rest_framework.response import Response
from rest_framework import status

from .models import Contributor


def extract_ids(path):
    """Extract ids from an url."""
    ids = []
    for word in path.split('/'):
        if word.isdigit():
            ids.append(int(word))
    return ids


def is_contributor(user, project):
    """Verify if an user is a project's contributor."""
    try:
        Contributor.objects.get(user_id=user, project_id=project)
    except Contributor.DoesNotExist:
        return False
    return True


def serialize(serializer, data, obj=None):
    """Serialize in the database."""
    serializer = serializer(obj, data=data) if obj else serializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
