from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Paginator for most of the tasks of the application. It's a default paginator.
    """
    page_query_param = 'currentPage'
    page_size_query_param = 'limit'
    page_size = 20

    def get_paginated_response(self, data):
        """
        Modified method "get_paginated_response" to fit swagger requirements
        :param data:
        :return:
        """
        return Response({
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages
        })


class ProfilePagination(PageNumberPagination):
    """
    Paginator for user's profile data. It's the least intrusive way to fit swagger requirements.
    """
    page_query_param = 'currentPage'
    page_size_query_param = 'limit'
    page_size = 20

    def get_paginated_response(self, data):
        """
        Modified method "get_paginated_response" to fit swagger requirements
        :param data:
        :return:
        """
        if data:
            return Response(data[0])
        return Response(data)
