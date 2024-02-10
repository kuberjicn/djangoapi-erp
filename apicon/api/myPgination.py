from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'  # URL query parameter to control page size
    max_page_size = 50  # Maximum number of items per page