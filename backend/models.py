from django.db import models

# Create your models here.

class Services(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_title = models.CharField(max_length=255, unique=True)
    short_description = models.TextField()

    class Meta:
        db_table = 'services'
    def __str__(self):
        return self.service_title

class Blog(models.Model):
    id = models.BigAutoField(primary_key=True)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='media/images/')
    description = models.TextField()

    class Meta:
        db_table = 'blog'
    def __str__(self):
        return self.title



