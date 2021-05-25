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
