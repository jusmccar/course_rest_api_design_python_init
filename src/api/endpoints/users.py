from ninja import Router
from uuid import UUID

from api.logic.exceptions import get_error_response
from api.logic.user_logic import handle_create_dog_user
from api.logic.user_logic import handle_dog_users_list
from api.logic.user_logic import handle_get_current_user
from api.logic.user_logic import handle_get_dog_user
from api.logic.user_logic import handle_update_me
from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.user_schemas import DogUserCreateSchemaIn
from api.schemas.user_schemas import DogUserSchemaOut
from api.schemas.user_schemas import DogUserUpdateSchemaIn
from api.schemas.user_schemas import DogUserWithTokenSchemaOut

router = Router()


@router.get("/", response=list[DogUserSchemaOut])
def dog_users_list(request):
    """
    Dog users list endpoint that returns a list of dog users.
    """
    users = handle_dog_users_list()

    return (200, users)


@router.post("/", response={201: DogUserWithTokenSchemaOut, 409: ErrorSchemaOut}, auth=None)
def create_dog_user(request, user: DogUserCreateSchemaIn):
    """
    Dog user create endpoint that creates a single dog user.
    """
    try:
        user_obj, token = handle_create_dog_user(username=user.username, password=user.password)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (201, {"user": user_obj, "token": token.key})


@router.get("/me/", response={200: DogUserSchemaOut})
def get_current_user(request):
    """
    Dog user detail endpoint that returns the currently authenticated dog user.
    """
    user_obj = request.auth
    user_obj = handle_get_current_user(user_obj)

    return (200, user_obj)


@router.patch("/me/", response={200: DogUserSchemaOut, 409: ErrorSchemaOut})
def update_me(request, user: DogUserUpdateSchemaIn):
    """
    Dog user update endpoint that updates the currently authenticated dog user.
    """
    user_obj = request.auth
    data = user.dict(exclude_unset=True)

    try:
        user_obj = handle_update_me(user_obj, data)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (200, user_obj)


@router.get("/{user_id}/", response={200: DogUserSchemaOut, 404: ErrorSchemaOut})
def get_dog_user(request, user_id: UUID):
    """
    Dog user detail endpoint that returns a single dog user.
    """
    try:
        user_obj = handle_get_dog_user(user_id)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (200, user_obj)
