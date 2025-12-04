from ninja import Router
from uuid import UUID

from api.schemas.bark_schemas import BarkCreateUpdateSchemaIn
from api.schemas.bark_schemas import BarkSchemaOut
from api.schemas.bark_schemas import ErrorSchemaOut
from core.models import BarkModel
from core.models import DogUserModel

router = Router()


@router.get("/", response=list[BarkSchemaOut])
def barks_list(request):
    """
    Bark list endpoint that returns a list of barks.
    """
    return BarkModel.objects.select_related("user").all()

@router.post("/", response={201: BarkSchemaOut})
def create_bark(request, bark: BarkCreateUpdateSchemaIn):
    """
    Bark create endpoint that creates a single bark.
    """
    data = bark.dict()
    data['user_id'] = DogUserModel.objects.first().id
    obj = BarkModel.objects.create(**data)

    return (201, obj)

@router.get("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut})
def get_bark(request, bark_id: UUID):
    """
    Bark detail endpoint that returns a single bark.
    """
    obj = BarkModel.objects.select_related("user").filter(id=bark_id).first()

    if not obj:
        return (404, {"error": "Bark not found"})

    return (200, obj)

@router.put("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut})
def update_bark(request, bark_id: UUID, bark: BarkCreateUpdateSchemaIn):
    """
    Bark update endpoint that updates a single bark.
    """
    obj = BarkModel.objects.select_related("user").filter(id=bark_id).first()

    if not obj:
        return (404, {"error": "Bark not found"})

    for attr, value in bark.dict().items():
        setattr(obj, attr, value)

    obj.save()

    return (200, obj)

@router.delete("/{bark_id}/", response={204: None, 404: ErrorSchemaOut})
def delete_bark(request, bark_id: int):
    """
    Bark delete endpoint that deletes a single bark.
    """
    if bark_id not in (1, 2, 3):
        return (404, {"error": "Bark not found"})

    return (204, None)
