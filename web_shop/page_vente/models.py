from django.db import models


# Create your models here.
class Macrame(models.Model):
    TYPE_CHOICES = [
        ('Murale', 'Murale'),
        ('Collier', 'Collier'),
        ('Bracelet', 'Bracelet'),
        ('Boucles d\'oreilles', 'Boucles d\'oreilles'),
        ('Divers', 'Divers'),
    ]
    nom = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    ornement = models.CharField(max_length=200)
    prix = models.FloatField(default=0.0)
    disponible = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Maroquinerie (models.Model):
    TYPE_CHOICES = [
        ('Portefeuille, Porte carte', 'Portefeuille, Porte carte'),
        ('Blague à tabac', 'Blague à tabac'),
        ('Sac divers', 'Sac divers'),
        ('Ceinture', 'Ceinture'),
        ('Bijoux', 'Bijoux'),
        ('Collier chien', 'Collier chien'),
        ('Divers', 'Divers'),
    ]
    nom = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    ornement = models.CharField(max_length=200)
    prix = models.FloatField(default=0.0)
    disponible = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Together (models.Model):
    TYPE_CHOICES = [
        ('Murale', 'Murale'),
        ('Collier', 'Collier'),
        ('Bracelet', 'Bracelet'),
        ('Boucles d\'oreilles', 'Boucles d\'oreilles'),
        ('Portefeuille, Porte carte', 'Portefeuille, Porte carte'),
        ('Blague à tabac', 'Blague à tabac'),
        ('Sac divers', 'Sac divers'),
        ('Ceinture', 'Ceinture'),
        ('Bijoux', 'Bijoux'),
        ('Collier chien', 'Collier chien'),
        ('Divers', 'Divers'),
    ]
    nom = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    ornement = models.CharField(max_length=200)
    prix = models.FloatField(default=0.0)
    disponible = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
