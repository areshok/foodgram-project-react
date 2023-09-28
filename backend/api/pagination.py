from rest_framework.pagination import PageNumberPagination


class ReceiptPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 10000
    page_size_query_param = 'limit'
