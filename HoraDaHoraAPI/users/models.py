from django.db import models
from django.contrib.auth.models import User

# Create your models here.

HABILITIES_CHOICES = (
    (None, 'Null'),
    ('a', 'habilidade1'),
    ('b', 'habilidade2'),
    ('c', 'habilidade3'),
    ('d', 'habilidade4'),
    ('e', 'habilidade5')
)

class Profile(models.Model):
    hours = models.IntegerField()
    habilities = models.CharField(
        max_length = 2,
        choices = HABILITIES_CHOICES,
        default = None,
        null = True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField()
    photo = models.ImageField(upload_to='./media', blank=True)
    coins = models.IntegerField()
    # aulas que tem q dar
    # aulas que recebeu
