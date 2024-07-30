from django.db import models

class Movie(models.Model):
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    studios = models.CharField(max_length=255)
    producers = models.CharField(max_length=255)
    winner = models.BooleanField(null=True)  # Permitir valores nulos

    class Meta:
        db_table = 'filmes'  # Nome da coleção no MongoDB
        managed = True