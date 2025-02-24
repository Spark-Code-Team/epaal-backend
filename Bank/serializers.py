from rest_framework import serializers
from .models import Facility,Bank,FacilityInstallmentNumber

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ("__all__")

class FacilityInstallmentNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityInstallmentNumber
        fields = ('id',"number_of_installment")


class FacilitySerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    insatllments=serializers.SerializerMethodField()
    class Meta:
        model = Facility
        fields = ("id","name","bank","bank_interest_percent","evaam_subscripton_percent","pre_payment_percent","max_value","insatllments")

    def get_insatllments(self,obj):
        insatllments=FacilityInstallmentNumber.objects.filter(facility=obj)
        return FacilityInstallmentNumberSerializer(insatllments,many=True).data
    