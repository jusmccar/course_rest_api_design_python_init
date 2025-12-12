import base64
import json
from typing import Any

from django.http import HttpRequest
from ninja import Schema
from ninja.pagination import PaginationBase

class SkipPagination(PaginationBase):
    """
    Custom pagination class that allows skipping a number of items
    and specifying the number of items per page.
    """
    class Input(Schema):
        skip: int = 0
        per_page: int = 5

    class Output(Schema):
        items: list[Any]
        total: int
        pages: int
        per_page: int
        skip: int
        next: str | None = None
        previous: str | None = None

    def paginate_queryset(self, queryset, pagination: Input, **params):
        skip = pagination.skip
        per_page = pagination.per_page
        count = queryset.count()

        # Build the base URL from the current request
        request: HttpRequest = params.get('request')
        base_url = self._get_base_url(request)

        # Calculate next link (if there are more items)
        next_link = None

        if skip + per_page < count:
            # Your code to construct next link
            next_skip = skip + per_page
            next_link = f"{base_url}?skip={next_skip}&per_page={per_page}"

        # Calculate previous link (if not on first page)
        previous_link = None

        if skip > 0:
            # Your code to construct previous link
            previous_skip = max(0, skip - per_page)
            previous_link = f"{base_url}?skip={previous_skip}&per_page={per_page}"

        # Return response with navigation links
        return {
            'items': queryset[skip : skip + per_page],
            'total': queryset.count(),
            'pages': (queryset.count() + per_page - 1) // per_page,
            'per_page': per_page,
            'skip': skip,
            'next': next_link,
            'previous': previous_link,
        }

    def _get_base_url(self, request):
        """Build the base URL without query parameters"""
        if not request:
            return ''

        # Get the full path without query parameters
        path = request.path

        # Get the scheme (http or https)
        scheme = 'https' if request.is_secure() else 'http'

        # Get the host
        host = request.get_host()

        # Construct the base URL
        return f"{scheme}://{host}{path}"


class TimestampCursorPagination(PaginationBase):
    """
    Cursor pagination using timestamps.
    """
    class Input(Schema):
        cursor: str | None = None
        limit: int = 10

    class Output(Schema):
        items: list[Any]
        next: str | None = None
        next_cursor: str | None = None
        previous: str | None = None
        previous_cursor: str | None = None

    def paginate_queryset(self, queryset, pagination: Input, **params):
        limit = min(pagination.limit, 100)
        cursor = pagination.cursor

        # Build the base URL from the current request
        request: HttpRequest = params.get("request")
        base_url = self._get_base_url(request)

        # Default ordering
        queryset = queryset.order_by('-created_at')

        # Decode cursor if provided
        filter_kwargs = {}
        if cursor:
            decoded = self.decode_cursor(cursor)

            if decoded is not None:
                timestamp = decoded.get("timestamp")

                if timestamp:
                    filter_kwargs["created_at__lt"] = timestamp

        # This gets one more than requested to determine if there's a next page
        results = list(queryset.filter(**filter_kwargs)[:limit + 1])

        # If we got more results than requested, there's a next page
        has_next = len(results) > limit

        if has_next:
            # Remove the extra item
            results = results[:-1]

        # Generate the next cursor
        next_cursor = None

        if has_next and results:
            next_timestamp = results[-1].created_at.isoformat()
            next_cursor = self.encode_cursor({"timestamp": next_timestamp})

        # Generate the previous cursor
        previous_cursor = None

        if results and cursor:
            # Step 1: Find the timestamp of the first item in our current results
            first_timestamp = results[0].created_at.isoformat()

            # Step 2: We need to find items NEWER than our current page
            prev_items = list(
                queryset.filter(created_at__gt=first_timestamp).order_by("created_at")[
                    :limit
                ]
            )

            # Step 3: If we found any items, the last one will be the oldest of the newer items
            if prev_items:
                oldest_prev_item = (
                    prev_items[-1].created_at.isoformat() if prev_items else None
                )

                if oldest_prev_item:
                    # Step 4: Create the encoded cursor for this item
                    previous_cursor = self.encode_cursor(
                        {"timestamp": oldest_prev_item}
                    )

        return {
            "items": results,
            "next": f"{base_url}?cursor={next_cursor}&limit={limit}" if next_cursor else None,
            "next_cursor": next_cursor,
            "previous": f"{base_url}?cursor={previous_cursor}&limit={limit}" if previous_cursor else None,
            "previous_cursor": previous_cursor,
        }

    def decode_cursor(self, cursor):
        """Decode the cursor data from a URL-safe string"""
        if not cursor:
            return None

        try:
            decoded = base64.b64decode(cursor.encode()).decode()
            return json.loads(decoded)
        except (ValueError, json.JSONDecodeError):
            return None

    def encode_cursor(self, data):
        """Encode the cursor data into a URL-safe string"""
        json_str = json.dumps(data)
        encoded = base64.b64encode(json_str.encode()).decode()

        return encoded

    def _get_base_url(self, request):
        """Build the base URL without query parameters"""
        if not request:
            return ""

        # Get the full path without query parameters
        path = request.path

        # Get the scheme (http or https)
        scheme = "https" if request.is_secure() else "http"

        # Get the host
        host = request.get_host()

        # Construct the base URL
        return f"{scheme}://{host}{path}"
