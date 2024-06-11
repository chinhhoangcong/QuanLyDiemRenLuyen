from rest_framework.pagination import PageNumberPagination


class ActivityPaginator(PageNumberPagination):
    page_size = 2


class ScorePaginator(PageNumberPagination):
    page_size = 2