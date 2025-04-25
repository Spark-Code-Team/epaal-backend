from rest_framework import serializers
from .models import Facility,Bank, FacilityDocument,FacilityInstallmentNumber, UserDocumetn, UserFacility, UserInstallment

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ("nickname","name")

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



class GetUserDocumentSerializer(serializers.ModelSerializer):
    document=FacilityDocumentSerializer()
    class Meta:
        model = UserDocumetn
        fields = ("id","document","value","file","status")


class UserInstallmentSerialiser(serializers.ModelSerializer):

    class Meta:
        model=UserInstallment
        fields=("id","is_paid","status","installment_number","paid_date","created_at","amount","final_amount","installment_number","due_date")


class FacilityUserSideSerializer(serializers.ModelSerializer):
    bank=BankSerializer()
    class Meta:
        model=Facility
        fields=("id","name","bank","max_value")


class CancledFacilityUseerSerialiser(serializers.ModelSerializer):
        num_of_installment=serializers.SerializerMethodField()
        facility=FacilityUserSideSerializer()
        class Meta:
            model = UserFacility
            fields = ("id","reject_reason_text","facility","num_of_installment")

        def get_num_of_installment(self,obj):
            return obj.choosen_facility_installment_number.number_of_installment


class InstallmentFacilityUseerSerialiser(serializers.ModelSerializer):

        num_of_installment=serializers.SerializerMethodField()
        facility=FacilityUserSideSerializer()
        price_of_every_installment=serializers.SerializerMethodField() 
        num_of_paid_installment=serializers.SerializerMethodField() 
        num_of_unpaid_installment=serializers.SerializerMethodField()   

        class Meta:
            model = UserFacility
            fields = ("id","facility","num_of_installment","choosen_value","price_of_every_installment","num_of_paid_installment","num_of_unpaid_installment")

        def get_num_of_installment(self,obj):
            return obj.choosen_facility_installment_number.number_of_installment
        
        def get_num_of_paid_installment(self,obj):
            if UserInstallment.objects.filter(user_facility=obj.id,is_paid=True).exists():
                return UserInstallment.objects.filter(user_facility=obj.id,is_paid=True).count()   
            return 0 
        def get_num_of_unpaid_installment(self,obj):
            if UserInstallment.objects.filter(user_facility=obj.id,is_paid=False).exists():
                return UserInstallment.objects.filter(user_facility=obj.id,is_paid=False).count()   
            return 0         
        def get_price_of_every_installment(self,obj):
            return UserInstallment.objects.filter(user_facility=obj.id,is_paid=False).last().amount

class FacilityUseerSerialiser(serializers.ModelSerializer):
    user_name=serializers.SerializerMethodField()
    facility=FacilityUserSideSerializer()
    class Meta:
        model = UserFacility
        fields = ("id","user_name","status","level","level_number","given_value","created_at","facility")

    def get_user_name(self,obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

class DoneFacilityUseerSerialiser(serializers.ModelSerializer):

        num_of_installment=serializers.SerializerMethodField()
        facility=FacilityUserSideSerializer()
        last_paid_date=serializers.SerializerMethodField()
        class Meta:
            model = UserFacility
            fields = ("id","facility","num_of_installment","given_value","last_paid_date")

        def get_num_of_installment(self,obj):
            return obj.choosen_facility_installment_number.number_of_installment
        

        def get_last_paid_date(self,obj):
            if  UserInstallment.objects.filter(id=obj.id).exists():
                return UserInstallment.objects.filter(id=obj.id).last().paid_date
            return None
