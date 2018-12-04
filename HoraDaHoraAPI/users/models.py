from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = (
    (1, 'Aguardando resposta'),
    (2, 'Recusada'),
    (3, 'Aceita'),
    (4, 'Concluida')
)

class Abilities(models.Model):
    name = models.CharField(max_length = 20)

class Profile(models.Model):
    abilities = models.ManyToManyField(Abilities)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True)
    photo = models.ImageField(upload_to='./media', null=True)
    coins = models.IntegerField(default = 0)
    points = models.IntegerField(default = 0)
    # aulas que tem q dar
    # aulas que recebeu

class Availability(models.Model):
    user = models.ForeignKey(User, related_name='availability', on_delete=models.CASCADE)
    date = models.DateTimeField()

    class Meta:
        unique_together = ('id', 'date')
        ordering = ['date']

    def __unicode__(self):
        return '%d: %s' % (str(self.date))

class Notification(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    interested = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interested')
    date = models.ForeignKey(Availability, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    hours = models.IntegerField(default=0)
