from ninja import Router
from uuid import UUID

from api.schemas.user_schemas import DogUserSchemaOut
from core.models import DogUserModel

router = Router()


@router.get("/", response=list[DogUserSchemaOut])
def dog_users_list(request):
    """
    Dog users list endpoint that returns a list of dog users.
    """
    return DogUserModel.objects.all()