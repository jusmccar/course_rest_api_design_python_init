from typing import Any

from django.db.models import Q
from django.db.models import QuerySet
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
    order_by: str | None = None

    def filter_order_by(self, value: str) -> Q:
        """Filter for ordering users"""
        return Q()


class BarksFilter(FilterSchema):
    """
    Filter schema for bark endpoints.
    """
    message: str | None = Field(None, q="message__icontains")
    trending: bool | None = None
    order_by: str | None = None

    def filter_trending(self, value: bool) -> Q:
        """Filter for trending barks"""
        if not value:
            return Q()

        one_day_ago = timezone.now() - timezone.timedelta(days=1)

        return Q(created_at__gte=one_day_ago) & Q(sniff_count__gte=1)

    def filter_order_by(self, value: str) -> Q:
        """Filter for ordering barks"""
        return Q()


def apply_ordering(queryset: QuerySet, order_by: str | None, model_class: Any = None) -> QuerySet:
    """
    Apply ordering to a queryset based on an order_by parameter.

    Args:
        queryset: The Django queryset to order
        order_by: The field to order by (with optional - prefix for descending)
        model_class: Optional model class to check if the field exists

    Returns:
        The ordered queryset
    """
    if not order_by:
        return queryset

    if model_class:
        field_name = order_by[1:] if order_by.startswith("-") else order_by

        if not hasattr(model_class, field_name):
            return queryset

    return queryset.order_by(order_by)
