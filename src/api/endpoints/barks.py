from ninja import Router
from uuid import UUID

from api.logic.bark_logic import handle_barks_list
from api.logic.bark_logic import handle_create_bark
from api.schemas.bark_schemas import BarkCreateUpdateSchemaIn
from api.schemas.bark_schemas import BarkSchemaOut
from api.schemas.common_schemas import ErrorSchemaOut
from core.models import BarkModel

router = Router()


@router.get("/", response=list[BarkSchemaOut], auth=None)
def barks_list(request):
    """
    Bark list endpoint that returns a list of barks.
    """
    barks = handle_barks_list()

    return barks


@router.post("/", response={201: BarkSchemaOut})
def create_bark(request, bark: BarkCreateUpdateSchemaIn):
    """
    Bark create endpoint that creates a single bark.
    """
    user_obj = request.auth
    data = bark.dict()
    bark_obj = handle_create_bark(user_obj, data)

    return (201, bark_obj)


@router.get("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut}, auth=None)
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
    obj = BarkModel.objects.select_related("user").filter(id=bark_id, user_id=request.auth.id).first()

    if not obj:
        return (404, {"error": "Bark not found"})

    data = bark.dict()

    for attr, value in data.items():
        setattr(obj, attr, value)

    obj.save()

    return (200, obj)


@router.delete("/{bark_id}/", response={204: None, 404: ErrorSchemaOut})
def delete_bark(request, bark_id: UUID):
    """
    Bark delete endpoint that deletes a single bark.
    """
    obj = BarkModel.objects.select_related("user").filter(id=bark_id, user_id=request.auth.id).first()

    if not obj:
        return (404, {"error": "Bark not found"})

    obj.delete()

    return (204, None)
