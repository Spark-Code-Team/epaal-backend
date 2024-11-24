from django.contrib.auth.models import BaseUserManager
from Role.models import Role
def int_to_unique_string(num):
    """
    Hashes an integer and returns a unique string representation.
    """
    hash_val = hash(num+100000000)
    hex_str = hex(hash_val)[2:]  # Remove "0x" prefix
    return hex_str

class UserManager(BaseUserManager):
    def create_user(self,phone_number,first_name=None,last_name=None, national_code=None,password=None,gender=None,inviter_id=None,role=None):

        if not phone_number:
            raise ValueError("Users must have an phone number")


        user = self.model(
            national_code=national_code,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            inviter_id=inviter_id,
            role=role,
        )
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        user.referrer_code = int_to_unique_string(user.id)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, national_code, password,phone_number,gender,first_name,last_name, role):
        user = self.create_user(
            first_name="admin",
            last_name="admin",
            gender=gender,
            phone_number=phone_number,
            national_code=national_code,
            password=password,
            inviter_id=None,
            role=Role.objects.get(name="admin"),
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user