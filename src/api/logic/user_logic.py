from core.models import DogUserModel


def handle_dog_users_list():
    """
    Returns a list of all dog users.
    """
    return DogUserModel.objects.all()
