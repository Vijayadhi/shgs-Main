from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
import os

# Utility function to validate file size and type
def validate_image(image):
    # file_size = image.file.size
    # limit_kb = 1024 * 1024  # 1 MB limit
    # if file_size > limit_kb:
    #     raise ValidationError("Max file size is 1MB")

    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif']
    if image.file.content_type not in valid_mime_types:
        raise ValidationError("Only JPEG, JPG,GIF, or PNG files are allowed.")


# Create your models here.

class Services(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_title = models.CharField(max_length=255, unique=True)
    short_description = models.TextField()
    image = models.ImageField(upload_to='services/', validators=[validate_image])  # Add validator for image

    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.service_title


class Blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='images/', validators=[validate_image])  # Add validator for image
    description = models.TextField()

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.title


# Adding Gallery models
# class GalleryCategory(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=255, unique=True)
#     description = models.TextField(blank=True, null=True)
#
#     class Meta:
#         db_table = 'gallery_category'
#         verbose_name = 'Gallery Category'
#         verbose_name_plural = 'Gallery Categories'
#
#     def __str__(self):
#         return self.name


class Gallery(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/', validators=[validate_image])  # Add validator for image
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
    """ Deletes the image file associated with a model instance when the instance is deleted. """
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


# Signal to delete old media files when the image is updated
@receiver(pre_save, sender=Services)
@receiver(pre_save, sender=Blog)
@receiver(pre_save, sender=Gallery)
def delete_old_media_on_change(sender, instance, **kwargs):
    """ Deletes the old image file when a new image is set. """
    if not instance.pk:
        return False  # Skip if instance is being created for the first time

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False  # Skip if old instance doesn't exist

    # Compare the old image with the new one
    if old_instance.image and old_instance.image != instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)
