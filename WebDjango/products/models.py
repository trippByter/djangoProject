from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(
        upload_to='media/',
        null=False,
        blank=False,)
    slug = models.SlugField(
        max_length=200,
        null=False,
        blank=False,
        unique=True,) 

    def __str__(self):
        return self.title
    
def new_slug(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)
        while Product.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:4])
            )
        instance.slug = slug

pre_save.connect(new_slug, sender=Product)