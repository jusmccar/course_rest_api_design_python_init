from api_v2.logic.exceptions import DuplicateResourceError
from api_v2.logic.exceptions import ResourceNotFoundError
from core.models import BarkModel
from core.models import DogUserModel
from core.models import UserSniffModel


def handle_create_sniff(bark_id: str, user: DogUserModel) -> BarkModel:
    """Handle creating a sniff (like) on a bark"""
    bark = BarkModel.objects.filter(id=bark_id).first()

    if not bark:
        raise ResourceNotFoundError("Bark not found")

    if UserSniffModel.objects.filter(user=user, bark=bark).exists():
        raise DuplicateResourceError("You've already sniffed this bark")

    UserSniffModel.objects.create(user=user, bark=bark)
    bark.sniff_count += 1
    bark.save()

    return bark
