from ninja import Router
from uuid import UUID

from api.schemas.common_schemas import ErrorSchemaOut
from api.schemas.user_schemas import DogUserCreateSchemaIn
from api.schemas.user_schemas import DogUserSchemaOut
from core.models import DogUserModel

router = Router()


@router.get("/", response=list[DogUserSchemaOut])
def dog_users_list(request):
    """
    Dog users list endpoint that returns a list of dog users.
    """
    return DogUserModel.objects.all()

@router.post("/", response={201: DogUserSchemaOut, 400: ErrorSchemaOut})
def create_dog_user(request, dog_user: DogUserCreateSchemaIn):
    """
    Dog user create endpoint that creates a single dog user.
    """
    if DogUserModel.objects.filter(username=dog_user.username).exists():
        return (400, {"error": "Username already exists"})

    data = dog_user.dict()
    obj = DogUserModel.objects.create(**data)

    return (201, obj)

@router.get("/{dog_user_id}/", response={200: DogUserSchemaOut, 404: ErrorSchemaOut})
def get_dog_user(request, dog_user_id: UUID):
    """
    Dog user detail endpoint that returns a single dog user.
    """
    obj = DogUserModel.objects.filter(id=dog_user_id).first()

    if not obj:
        return (404, {"error": "Dog user not found"})

    return (200, obj)
