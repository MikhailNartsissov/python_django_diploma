from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages
        })
