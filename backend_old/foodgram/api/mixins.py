from rest_framework import  mixins


class ViewOnly(mixins.ListModelMixin):
    pass
