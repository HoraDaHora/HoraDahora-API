from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Abilities(models.Model):
    name = models.CharField(max_length = 20)

class Profile(models.Model):
    hours = models.IntegerField(default = 0)
    abilities = models.ManyToManyField(Abilities)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True)
    photo = models.ImageField(upload_to='./media', null=True)
    coins = models.IntegerField(default = 0)
    # aulas que tem q dar
    # aulas que recebeu
