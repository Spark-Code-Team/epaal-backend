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
    def create_user(self,phone_number,first_name=None,last_name=None, national_code=None,password=None,is_man=None,inviter=None,role=None):

        if not phone_number:
            raise ValueError("Users must have an phone number")


        user = self.model(
            national_code=national_code,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            is_man=is_man,
            inviter=inviter,
            role=role,
        )
        if password is not None:
            user.set_password(password)
            user.has_two_factor=True
        user.save(using=self._db)
        user.referrer_code = int_to_unique_string(user.id)
        user.save(using=self._db)
        return user

    
    def create_superuser(self,phone_number, national_code=None, password=None,role=None):
        user = self.create_user(
            first_name="admin",
            last_name="admin",
            is_man=True,
            phone_number=phone_number,
            national_code=national_code,
            password=password,
            role=Role.objects.get(name="admin")
        )
        user.is_admin = True
        user.is_superuser = True
        user.has_two_factor = True


        user.save(using=self._db)
        return user