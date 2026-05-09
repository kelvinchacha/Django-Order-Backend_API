from django.db import models

class Oda(models.Model):
    meza = models.CharField(max_length=20)
    chakula = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default= 'pending')
    muda = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chakula} - {self.meza}"
