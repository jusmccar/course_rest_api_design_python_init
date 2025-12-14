from django.db.models import Q
from django.utils import timezone
from ninja import Field
from ninja import FilterSchema


class UsersFilter(FilterSchema):
    """
    Filter schema for user endpoints.
    """
    username: str | None = Field(None, q="username__icontains")
    favorite_toy: str | None = Field(None, q="favorite_toy__icontains")
    search: str | None = Field(None, q=["username__icontains", "favorite_toy__icontains"])


class BarksFilter(FilterSchema):
    """
    Filter schema for bark endpoints.
    """
    message: str | None = Field(None, q="message__icontains")
    trending: bool | None = None

    def filter_trending(self, value: bool) -> Q:
        """Filter for trending barks"""
        if not value:
            return Q()

        one_day_ago = timezone.now() - timezone.timedelta(days=1)

        return Q(created_at__gte=one_day_ago) & Q(sniff_count__gte=1)
