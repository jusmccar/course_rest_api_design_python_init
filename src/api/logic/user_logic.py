from api.logic.exceptions import DuplicateResourceError
from api.logic.exceptions import ResourceNotFoundError
from core.models import AuthTokenModel
from core.models import DogUserModel


def handle_dog_users_list():
    """
    Returns a list of all dog users.
    """
    return DogUserModel.objects.all()

def handle_create_dog_user(username: str, password: str) -> tuple[DogUserModel, AuthTokenModel]:
    """
    Creates a single dog user.
    """
    if DogUserModel.objects.filter(username=username).exists():
        raise DuplicateResourceError("Username already exists")

    user = DogUserModel.objects.create_user(username=username, password=password)
    token = AuthTokenModel.objects.create(user=user)

    return (user, token)

def handle_get_current_user(user: DogUserModel) -> DogUserModel:
    return user

def handle_update_me(user: DogUserModel, data: dict) -> DogUserModel:
    if "username" in data and data["username"] != user.username and DogUserModel.objects.filter(username=data["username"]).exists():
        raise DuplicateResourceError("Username already exists")

    for attr, value in data.items():
        setattr(user, attr, value)

    user.save()

    return user

def handle_get_dog_user(user_id: int) -> DogUserModel:
    user = DogUserModel.objects.filter(id=user_id).first()

    if not user:
        raise ResourceNotFoundError("Dog user not found")

    return user
