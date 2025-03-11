from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    types = models.CharField(max_length=200)  # Se guardarán como cadena separada por comas
    image = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.poke_id:03d} - {self.name}"
