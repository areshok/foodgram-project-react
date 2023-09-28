from rest_framework.pagination import PageNumberPagination


class ReceiptPagination(PageNumberPagination):
    page_size_query_param = 'limit'
