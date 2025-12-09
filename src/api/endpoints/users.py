from ninja import Router
from uuid import UUID

from api.logic.user_logic import handle_create_dog_user
from api.logic.user_logic import handle_dog_users_list
from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.user_schemas import DogUserCreateSchemaIn
from api.schemas.user_schemas import DogUserSchemaOut
from api.schemas.user_schemas import DogUserUpdateSchemaIn
from api.schemas.user_schemas import DogUserWithTokenSchemaOut
from core.models import AuthTokenModel
from core.models import DogUserModel

router = Router()


@router.get("/", response=list[DogUserSchemaOut])
def dog_users_list(request):
    """
    Dog users list endpoint that returns a list of dog users.
    """
    users = handle_dog_users_list()

    return 200, users

@router.post("/", response={201: DogUserWithTokenSchemaOut, 400: ErrorSchemaOut}, auth=None)
def create_dog_user(request, user: DogUserCreateSchemaIn):
    """
    Dog user create endpoint that creates a single dog user.
    """
    try:
        user_obj, token = handle_create_dog_user(username=user.username, password=user.password)
    except ValueError as e:
        return (400, {"error": str(e)})

    return (201, {"user": user_obj, "token": token.key})

@router.get("/me/", response={200: DogUserSchemaOut})
def get_current_user(request):
    """
    Dog user detail endpoint that returns the currently authenticated dog user.
    """
    obj = request.auth

    return (200, obj)

@router.patch("/me/", response={200: DogUserSchemaOut, 400: ErrorSchemaOut})
def update_me(request, dog_user: DogUserUpdateSchemaIn):
    """
    Dog user update endpoint that updates the currently authenticated dog user.
    """
    obj = request.auth
    data = dog_user.dict(exclude_unset=True)

    if "username" in data and data["username"] != obj.username and DogUserModel.objects.filter(username=data["username"]).exists():
        return (400, {"error": "Username already exists"})

    for attr, value in data.items():
        setattr(obj, attr, value)

    obj.save()

    return (200, obj)

@router.get("/{dog_user_id}/", response={200: DogUserSchemaOut, 404: ErrorSchemaOut})
def get_dog_user(request, dog_user_id: UUID):
    """
    Dog user detail endpoint that returns a single dog user.
    """
    obj = DogUserModel.objects.filter(id=dog_user_id).first()

    if not obj:
        return (404, {"error": "Dog user not found"})

    return (200, obj)
