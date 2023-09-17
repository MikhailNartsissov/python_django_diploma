from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_query_param = 'currentPage'
    page_size_query_param = 'limit'
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages
        })


class ProfilePagination(PageNumberPagination):
    page_query_param = 'currentPage'
    page_size_query_param = 'limit'
    page_size = 20

    def get_paginated_response(self, data):
        if data:
            return Response(data[0])
        return Response(data)
