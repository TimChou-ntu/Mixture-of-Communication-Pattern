from rest_framework import serializers
from .models import FibReqItem, FibResItem

class FibReqItemSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(default=1)

    class Meta:
        model = FibReqItem
        fields = ('__all__')

class FibResItemSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(default=1)
    value = serializers.IntegerField(default=1)

    class Meta:
        model = FibResItem
        fields = ('__all__')