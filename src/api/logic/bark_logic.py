from api.logic.exceptions import ResourceNotFoundError
from core.models import BarkModel
from core.models import DogUserModel


def handle_barks_list() -> list[BarkModel]:
    return BarkModel.objects.select_related("user").all()


def handle_create_bark(user: DogUserModel, data: dict) -> BarkModel:
    data['user_id'] = user.id
    bark = BarkModel.objects.create(**data)

    return bark


def handle_get_bark(bark_id: str) -> BarkModel:
    bark = BarkModel.objects.select_related("user").filter(id=bark_id).first()

    if not bark:
        raise ResourceNotFoundError("Bark not found")

    return bark
