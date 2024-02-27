from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 50  # Number of items per page
    page_size_query_param = 'page_size'  # URL query parameter to control page size
    max_page_size = 50  # Maximum number of items per page


class LeavePageNumberPagination(PageNumberPagination):
    page_size = 6  # Number of items per page
    page_size_query_param = 'page_size'  # URL query parameter to control page size
    max_page_size = 18  # Maximum number of items per page