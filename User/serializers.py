from rest_framework import serializers
from Role.models import Role
from Role.serializers import RoleSerializer
from .models import Address, CustomUser,TempAddress
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation

class UserRegisterSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    class Meta:
        model = CustomUser
        fields = ('id','first_name', 'last_name', 'national_code', 'phone_number','is_man', 'password','has_two_factor','role')
        extra_kwargs = {
            'password': {'write_only': True,
                         'required':False
                         },
            'first_name':{'default':None},
            'last_name':{'default':None},
            'national_code':{'default':None},
            'is_man':{'default':True},
            

        }

    def create(self, validated_data, referrer_code=None, role=None):

        if referrer_code:
            inviter_id = CustomUser.objects.filter(referrer_code=referrer_code).values_list('id', flat=True).first()
            if inviter_id is not None:
                inviter_id = int(inviter_id)
            else:
                raise serializers.ValidationError("There isn't any user with this referrer code")

        else:
            inviter_id = None
        
        if role:
            print("1111111111111111111111111111111111")
            if role["name"] in ["shop_admin", "user"]:
                user_role = Role.objects.get(name=role["name"])
        else:
            print("2222222222222222222222222222222222")
            user_role=Role.objects.get(name="user")
        if validated_data.get('password') and validated_data['password']:
            return CustomUser.objects.create_user(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                national_code=validated_data['national_code'],
                phone_number=validated_data['phone_number'],
                is_man=validated_data['is_man'],
                password=validated_data['password'],
                has_two_factor=True,
                inviter=inviter_id,
                role=user_role
            )
        else:
            return CustomUser.objects.create_user(
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    national_code=validated_data['national_code'],
                    phone_number=validated_data['phone_number'],
                    is_man=validated_data['is_man'],
                    inviter=inviter_id,
                    role=user_role
                )
            
    
    def update(self, instance, validated_data):
        if validated_data.get("role"):
            role=Role.objects.get(name=validated_data.get("role")["name"])
            instance.role = role
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.is_man = validated_data.get('is_man', instance.is_man)
        if validated_data.get('password') and validated_data['password']:
            instance.password = make_password(validated_data.get('password', instance.password))
            instance.has_two_factor=True
        instance.save()
        return instance

    def validate_first_name(self, value):
        if value == 'admin':
            raise serializers.ValidationError('first name can not be admin')
        return value

    def validate_last_name(self, value):
        if value == 'admin':
            raise serializers.ValidationError('last name can not be admin')
        return value
    
    def validate_national_code(self, value):
        if not value:
            return value

        if len(value) != 10:
            raise serializers.ValidationError('national code must be 10 characters')
        
        check = int(value[9])
        sum = 0

        for i in range(9):
            sum += int(value[i]) * (10 - i)

        remainder = sum % 11


        if remainder < 2:
            
            if check != remainder:
                raise serializers.ValidationError('national code is not correct')
        else:
            if check != 11 - remainder:
                raise serializers.ValidationError('national code is not correct')   
            
        return value
    
    def validate_phone_number(self, value):
        if  len(value) !=11:
            raise serializers.ValidationError('phone number must be 11 characters')
        return value
    
    def validate_password(self, value):
        if password_validation.validate_password(value):
            raise serializers.ValidationError('the password is easy please use another')
        return value


class HomeSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    class Meta:
            model = CustomUser
            fields = ('id','first_name','last_name','phone_number','role',)


class ConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
            model = CustomUser
            fields = ('id','first_name','last_name','phone_number',"national_code",'birthday_date','second_phone_number',"confirmed_data","confirmed_address")

class TempAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempAddress
        fields = ("__all__")

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("__all__")