from rest_framework import serializers

class BatchSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, blank=False)
    email = serializers.EmailField(max_length=50)
    phone = serializers.CharField(max_length=50, blank=False)
    address = serializers.CharField(max_length=50)
