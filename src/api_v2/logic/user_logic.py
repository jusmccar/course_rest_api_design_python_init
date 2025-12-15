from django.core.files.storage import default_storage
from django.db.models import QuerySet
from ninja.files import UploadedFile

from api_v2.logic.exceptions import DuplicateResourceError
from api_v2.logic.exceptions import InvalidFileError
from api_v2.logic.exceptions import ResourceNotFoundError
from common.filters import apply_ordering
from common.filters import UsersFilter
from core.models import AuthTokenModel
from core.models import DogUserModel


def handle_dog_users_list(filters: UsersFilter) -> QuerySet[DogUserModel]:
    """
    Returns a list of dog users.
    """
    users = DogUserModel.objects.all()
    users = filters.filter(users)

    if filters.order_by:
        users = apply_ordering(queryset=users, order_by=filters.order_by, model_class=DogUserModel)

    return users


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
    """
    Returns the currently authenticated dog user.
    """
    return user


def handle_update_me(user: DogUserModel, data: dict) -> DogUserModel:
    """
    Updates the currently authenticated dog user.
    """
    if "username" in data and data["username"] != user.username and DogUserModel.objects.filter(username=data["username"]).exists():
        raise DuplicateResourceError("Username already exists")

    for attr, value in data.items():
        setattr(user, attr, value)

    user.save()

    return user


def handle_upload_profile_image(user: DogUserModel, image: UploadedFile) -> DogUserModel:
    """
    Handle the logic for uploading a profile image.
    Validates the image and saves it to the user's profile.
    """
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']

    if image.content_type not in allowed_types:
        raise InvalidFileError("Invalid image type")

    # Validate file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB in bytes

    if image.size > max_size:
        raise InvalidFileError("Image size too large")

    # Delete old profile image if it exists
    if user.profile_image:
        if default_storage.exists(user.profile_image.name):
            default_storage.delete(user.profile_image.name)

    # Save new image
    user.profile_image = image
    user.save()

    return user


def handle_get_dog_user(user_id: int) -> DogUserModel:
    """
    Returns a single dog user.
    """
    user = DogUserModel.objects.filter(id=user_id).first()

    if not user:
        raise ResourceNotFoundError("Dog user not found")

    return user
