# Create your views here.


from django.core.paginator import Paginator
from django.utils.functional import cached_property
from neomodel import db
from neomodel.sync_.core import StructuredNode
from rest_framework import pagination


class LazyNeoQuery:
    """
    Class for setting up Neo4j queries in a lazy way
    """

    # Pretty much a copy of how QuerySets work
    # currently not a subclass of QuerySets as content diverges so much
    # but this might change in the future

    def __init__(self, obj: StructuredNode, query: str, order: str = "n.uuid"):
        """
        Setup object
        """
        self._object = obj
        self._chain = query
        self._filters = set()
        self._args = {}
        self._order = order
        self._skip = None
        self._limit = None
        self._result_cache = None

    @property
    def order(self):
        """
        return formatted order
        """
        if not self._order:
            return ""
        return f"ORDER BY {self._order}"

    @property
    def skip(self):
        """
        return formatted skip
        """
        if not self._skip:
            return ""
        return f"SKIP {self._skip}"

    @property
    def limit(self):
        """
        return formatted limit
        """
        if not self._limit:
            return ""
        return f"LIMIT {self._limit}"

    @cached_property
    @db.read_transaction
    def count(self) -> int:
        """
        get the count
        """
        if self._result_cache is not None:
            return len(self._result_cache)
        return self._object.cypher(
            "\n".join(
                [
                    self._chain,
                    self._get_filter_clause(),
                    "RETURN count(*)",
                    self.skip,
                    self.limit,
                ]
            ),
            self._args,
        )[0][0][0]

    def filter(self, filter_str: str, param: dict):
        """
        add filters to a query
        """
        self._filters.add(filter_str)
        self.add_param(param)

    def add_param(self, param):
        """
        add params to be passed to the query
        """
        self._args.update(param)

    def _get_filter_clause(self):
        """
        Format the WHERE clause for the filter query
        """
        if not self._filters:
            return ""
        return "WHERE " + " OR ".join(self._filters)

    def _resolve_query(self):
        if self._result_cache is not None:
            return len(self._result_cache)
        self._result_cache = self._object.cypher(
            "\n".join(
                [
                    self._chain,
                    self._get_filter_clause(),
                    "RETURN n",
                    self.order,
                    self.skip,
                    self.limit,
                ]
            ),
            self._args,
        )[0]
        return self._result_cache

    @db.read_transaction
    def __getitem__(self, k):
        """Retrieve an item or slice from the set of results."""
        if not isinstance(k, (int, slice)):
            raise TypeError(
                f"LazyNeoQuery indices must be integers or slices, not {type(k).__name__}."
            )
        if (isinstance(k, int) and k < 0) or (
            isinstance(k, slice)
            and (
                (k.start is not None and k.start < 0)
                or (k.stop is not None and k.stop < 0)
            )
        ):
            raise ValueError("Negative indexing is not supported.")

        if self._result_cache is not None:
            return self._result_cache[k]

        if isinstance(k, slice):
            if k.start is not None:
                self._skip = int(k.start)
            if k.stop is not None:
                self._limit = int(k.stop) - self._skip if self._skip else 0
            return (
                list(self._resolve_query())[:: k.step]
                if k.step
                else self._resolve_query()
            )

        self._skip = int(k)
        self._limit = 1
        self._resolve_query()
        return self._result_cache[0]


class CustomPaginator(Paginator):

    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        return self.object_list.count


class CustomPagination(pagination.PageNumberPagination):
    """custom pagination to add page_size from api. For example:

    http://api.example.org/accounts/?page=4
    http://api.example.org/accounts/?page=4&page_size=100"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    django_paginator_class = CustomPaginator
