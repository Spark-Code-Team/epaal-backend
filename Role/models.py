from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'
        db_table = 'role'

    def __str__(self):
        return self.name