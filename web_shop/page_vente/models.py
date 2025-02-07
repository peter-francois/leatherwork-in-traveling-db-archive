from django.db import models

class AllProducts(models.Model):

    CATEGORY_CHOICES = [
        ('Macrame', 'Macrame'),
        ('Maroquinerie', 'Maroquinerie'),
        ('hybride', 'hybride'),
        ('entretien', 'entretien')
    ]
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
    categorie = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    ornement = models.CharField(max_length=200, blank=True, null=True)
    prix = models.FloatField(default=0.0)
    lien_image1 = models.URLField(default='', max_length=20000, blank=True, null=True)
    lien_image2 = models.URLField(default='', max_length=20000, blank=True, null=True)
    lien_image3 = models.URLField(default='', max_length=20000, blank=True, null=True)
    lien_image4 = models.URLField(default='', max_length=20000, blank=True, null=True)
    disponible = models.BooleanField(default=False)

    def __str__(self):
        return self.nom
    
""" Create your models here.
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
    lien_image1 = models.URLField(default='', max_length=20000)
    lien_image2 = models.URLField(default='', max_length=20000)
    lien_image3 = models.URLField(default='', max_length=20000)
    lien_image4 = models.URLField(default='', max_length=20000)
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
    lien_image1 = models.URLField(default='', max_length=20000)
    lien_image2 = models.URLField(default='', max_length=20000)
    lien_image3 = models.URLField(default='', max_length=20000)
    lien_image4 = models.URLField(default='', max_length=20000)

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
    lien_image1 = models.URLField(default='', max_length=20000)
    lien_image2 = models.URLField(default='', max_length=20000)
    lien_image3 = models.URLField(default='', max_length=20000)
    lien_image4 = models.URLField(default='', max_length=20000)

    def __str__(self):
        return self.nom"""
