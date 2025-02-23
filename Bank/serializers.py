from rest_framework import serializers
from .models import Facility,Bank

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ("__all__")

class FacilitySerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    class Meta:
        model = Facility
        fields = ("__all__")
