# serializers.py

from rest_framework import serializers

from .models import TranDetail

class TranSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TranDetail
        fields = ('cardType', 'category', 'tran_date', 'desc', 'reward', 'status')