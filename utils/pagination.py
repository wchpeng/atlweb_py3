from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    """分页专用"""
    page_size = 16
    max_page_size = 50
    page_query_param = "page"
    page_size_query_param = "page_size"
