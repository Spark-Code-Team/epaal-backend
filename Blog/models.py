from django.db import models
from User.models import CustomUser
from EvaamBack import settings
from django.template.defaultfilters import filesizeformat
from django.core.validators import ValidationError, FileExtensionValidator
# Create your models here.


def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))
    
def blog_image_directory_path(instance, filename):
    return 'Media/blog/{0}/pictures/{1}'.format(str(instance.id), filename) 

class BlogTopic(models.Model):
    name=models.CharField(max_length=100)

    class Meta:
        verbose_name = 'blog_topic'
        verbose_name_plural = 'blog_topics'
        db_table = 'blog_topic'

class BlogPicture(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']   
    blog_pic= models.ImageField(upload_to=blog_image_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True, max_length=1000)
    class Meta:
        verbose_name = 'blog_picture'
        verbose_name_plural = 'blog_pictures'
        db_table = 'blog_picture'



class Blog(models.Model):
    text=models.CharField(max_length=1000)
    admin=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="admin_id_blog")
    title=models.CharField(max_length=100)
    blog_picture=models.ManyToManyField(BlogPicture,null=True,blank=True,related_name="pictures_ids_blog")
    topic=models.ForeignKey(BlogTopic,on_delete=models.CASCADE,related_name="topic_id_blog")
    is_show=models.BooleanField(default=False)
    is_top=models.BooleanField(default=False)
    num_of_like=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
        db_table = 'blog'

class BlogUser(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_id_userblog")
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="blog_id_userblog")

    class Meta:
        verbose_name = 'blog_user'
        verbose_name_plural = 'blog_users'
        db_table = 'blog_user'


class BlogComment(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="user_id_blog_comment")
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name="blog_id_blog_comment")
    parent=models.ForeignKey('self',on_delete=models.CASCADE,related_name="parent_id_blog_comment",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'blog_comment'
        verbose_name_plural = 'blog_comments'
        db_table = 'blog_comment'