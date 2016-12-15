from rest_framework import serializers


class LeaseResourceSerializer(serializers.Serializer):
    duration = serializers.IntegerField()
