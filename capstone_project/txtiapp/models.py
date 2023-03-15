from django.db import models

# Create your models here.

class Image(models.Model):
    text = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    

