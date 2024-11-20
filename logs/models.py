from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Log(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     action = models.CharField(max_length=255)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     photo = models.ImageField(upload_to='photos/', null=True, blank=True)

#     def __str__(self):
#         return f'{self.user} - {self.action}'
