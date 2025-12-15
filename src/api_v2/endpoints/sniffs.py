from ninja import Router

from api_v2.logic.exceptions import get_error_response
from api_v2.logic.sniff_logic import handle_create_sniff
from api_v2.schemas.common_schemas import ErrorSchemaOut
from api_v2.schemas.sniff_schemas import SniffCreateSchemaIn
from api_v2.schemas.sniff_schemas import SniffSchemaOut

router = Router()


@router.post("/", response={201: SniffSchemaOut, 409: ErrorSchemaOut, 404: ErrorSchemaOut})
def create_sniff(request, sniff: SniffCreateSchemaIn):
    """Sniff a bark"""
    user = request.auth
    bark_id = sniff.bark_id

    try:
        bark = handle_create_sniff(bark_id=bark_id, user=user)
    except Exception as e:
        status_code, error_response = get_error_response(e)

        return (status_code, error_response)

    return(201, bark)
