from django.shortcuts import render

# Create your views here.
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)

from rest_framework.viewsets import GenericViewSet, ModelViewSet


from .serializers import TranSerializer
from .models import TranDetail


class TranViewSet(GenericViewSet,  # generic view functionality 
                    CreateModelMixin,  # handles POSTs
                    RetrieveModelMixin,  # handles GETs 
                    UpdateModelMixin,  # handles PUTs and PATCHes
                    ListModelMixin): # handles GETs 

    queryset = TranDetail.objects.all().order_by('cardType')
    serializer_class = TranSerializer