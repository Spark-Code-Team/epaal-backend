from rest_framework import serializers
from .models import Facility,Bank, FacilityDocument,FacilityInstallmentNumber, UserDocumetn, UserFacility

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
    

class FacilityDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityDocument
        fields = ("__all__")

class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocumetn
        fields = ("__all__")


class FacilityUseerSerialiser(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField()
    class Meta:
        model = UserFacility
        fields = ("id","user_name","status","level","level_number","given_value","created_at","facility")

    def get_user_name(self,obj):
        return f'{obj.user.first_name} {obj.user.last_name}'
