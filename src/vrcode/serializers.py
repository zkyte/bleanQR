from rest_framework import serializers
from .models import QRCode


class InputSerializer(serializers.Serializer):
    fname = serializers.CharField(required=True, allow_blank=False, max_length=100)
    mname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    lname = serializers.CharField(required=True, allow_blank=False, max_length=100)
    email = serializers.EmailField(required=True, allow_blank=False, max_length=250)
    image = serializers.CharField(required=True, allow_blank=False, max_length=None)
    phone = serializers.CharField(required=True, allow_blank=False, max_length=100)
    url = serializers.URLField(required=False,  allow_blank=True, min_length=None, max_length=None)
    role    = serializers.CharField(required=False, allow_blank=True, max_length=100)
    company = serializers.CharField(required=False, allow_blank=True, max_length=100)
    remark  = serializers.CharField(required=False, allow_blank=True, max_length=None)



class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        order_by = ['name']
        fields = (  "id", "user_id", "name", "get_image")
