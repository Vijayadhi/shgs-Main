from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os
import mimetypes
from ckeditor.fields import RichTextField

from backend.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    # last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Add any additional fields if needed

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'custom_user'

# Utility function to validate image type
def validate_image(image):
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
    content_type, _ = mimetypes.guess_type(image.name)

    if content_type not in valid_mime_types:
        raise ValidationError("Only JPEG, JPG, GIF, or PNG files are allowed.")

# Services Model
class Services(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_title = models.CharField(max_length=255, unique=True)
    short_description = RichTextField(blank=True, null=True)
    about = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='services/', validators=[validate_image])
    footer_image = models.ImageField(blank=True, null=True)
    location = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    business_num1 = models.CharField(max_length=15, blank=True, null=True)
    business_num2 = models.CharField(max_length=15, blank=True, null=True)
    bussiness_email = models.EmailField(blank=True, null=True)
    address1 = models.CharField(null=True, max_length=200)
    address2 = models.CharField(null=True, max_length=200)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.service_title


# Blog Model
class Blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='images/', validators=[validate_image])
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.title


# Gallery Model
class Gallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='galleries')
    title = models.CharField(max_length=255)  # Added title field for Gallery
    image = models.ImageField(upload_to='gallery/', validators=[validate_image])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery'
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title

# Signal to delete media files when objects are deleted
@receiver(pre_delete, sender=Services)
@receiver(pre_delete, sender=Blog)
@receiver(pre_delete, sender=Gallery)
def delete_media_on_delete(sender, instance, **kwargs):
    """Deletes the image file associated with a model instance when the instance is deleted."""
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

# Signal to delete old media files when the image is updated
@receiver(pre_save, sender=Services)
@receiver(pre_save, sender=Blog)
@receiver(pre_save, sender=Gallery)
def delete_old_media_on_change(sender, instance, **kwargs):
    """Deletes the old image file when a new image is set."""
    if not instance.pk:
        return  # Skip if instance is being created for the first time

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return  # Skip if old instance doesn't exist

    # Compare the old image with the new one
    if old_instance.image and old_instance.image != instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)

    if old_instance.footer_image and old_instance.footer_image != instance.footer_image:
        if os.path.isfile(old_instance.footer_image.path):
            os.remove(old_instance.footer_image.path)