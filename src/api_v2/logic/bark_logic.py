import csv
from io import StringIO

from django.db.models import QuerySet
from django.http import HttpResponse

from api_v2.logic.exceptions import ResourceNotFoundError
from common.filters import apply_ordering
from common.filters import BarksFilter
from core.models import BarkModel
from core.models import DogUserModel


def handle_barks_list(filters: BarksFilter) -> QuerySet[BarkModel]:
    barks = BarkModel.objects.select_related("user").all()
    barks = filters.filter(barks)

    if filters.trending:
        barks = barks.order_by("-sniff_count")
    elif filters.order_by:
        barks = apply_ordering(queryset=barks, order_by=filters.order_by, model_class=BarkModel)

    return barks


def handle_create_bark(user: DogUserModel, data: dict) -> BarkModel:
    data['user_id'] = user.id
    bark = BarkModel.objects.create(**data)

    return bark


def handle_export_top_barks_csv(user: DogUserModel) -> HttpResponse:
    """
    Handle the logic for exporting user's top 10 sniffed barks as CSV.
    Returns an HttpResponse with CSV content.
    """
    # Get the user's top 10 most sniffed barks
    top_barks = BarkModel.objects.select_related("user").filter(user=user, sniff_count__gt=0).order_by("-sniff_count")[:10]

    # Create CSV content
    output = StringIO()
    writer = csv.writer(output)

    # Write CSV header
    writer.writerow([
        "Message",
        "Sniff Count",
        "Created At",
        "Username",
    ])

    # Write bark data
    for bark in top_barks:
        writer.writerow([
            bark.message,
            bark.sniff_count,
            bark.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            bark.user.username,
        ])

    # Create HTTP response with CSV content
    response = HttpResponse(output.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="top_barks.csv"'

    return response


def handle_get_bark(bark_id: str) -> BarkModel:
    bark = BarkModel.objects.select_related("user").filter(id=bark_id).first()

    if not bark:
        raise ResourceNotFoundError("Bark not found")

    return bark


def handle_update_bark(bark_id: str, user: DogUserModel, data: dict) -> BarkModel:
    bark = BarkModel.objects.select_related("user").filter(id=bark_id, user_id=user.id).first()

    if not bark:
        raise ResourceNotFoundError("Bark not found")

    for attr, value in data.items():
        setattr(bark, attr, value)

    bark.save()

    return bark


def handle_delete_bark(bark_id: str, user: DogUserModel) -> None:
    bark = BarkModel.objects.select_related("user").filter(id=bark_id, user_id=user.id).first()

    if not bark:
        raise ResourceNotFoundError("Bark not found")

    bark.delete()
