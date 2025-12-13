from ninja import Router
from ninja.pagination import paginate
from uuid import UUID

from api.logic.bark_logic import handle_barks_list
from api.logic.bark_logic import handle_create_bark
from api.logic.bark_logic import handle_delete_bark
from api.logic.bark_logic import handle_get_bark
from api.logic.bark_logic import handle_update_bark
from api.logic.exceptions import get_error_response
from api.schemas.bark_schemas import BarkCreateUpdateSchemaIn
from api.schemas.bark_schemas import BarkSchemaOut
from api.schemas.common_schemas import ErrorSchemaOut

router = Router()


@router.get("/", response=list[BarkSchemaOut], auth=None)
@paginate
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
    bark_obj = handle_create_bark(user=user_obj, data=data)

    return (201, bark_obj)


@router.get("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut}, auth=None)
def get_bark(request, bark_id: UUID):
    """
    Bark detail endpoint that returns a single bark.
    """
    try:
        bark_obj = handle_get_bark(bark_id=bark_id)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (200, bark_obj)


@router.put("/{bark_id}/", response={200: BarkSchemaOut, 404: ErrorSchemaOut})
def update_bark(request, bark_id: UUID, bark: BarkCreateUpdateSchemaIn):
    """
    Bark update endpoint that updates a single bark.
    """
    user_obj = request.auth
    data = bark.dict()

    try:
        bark_obj = handle_update_bark(bark_id=bark_id, user=user_obj, data=data)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (200, bark_obj)


@router.delete("/{bark_id}/", response={204: None, 404: ErrorSchemaOut})
def delete_bark(request, bark_id: UUID):
    """
    Bark delete endpoint that deletes a single bark.
    """
    user_obj = request.auth

    try:
        handle_delete_bark(bark_id=bark_id, user=user_obj)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return (204, None)
