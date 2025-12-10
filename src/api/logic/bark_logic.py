from core.models import BarkModel
from core.models import DogUserModel


def handle_create_bark(user: DogUserModel, data: dict) -> BarkModel:
    data['user_id'] = user.id
    bark = BarkModel.objects.create(**data)

    return bark
