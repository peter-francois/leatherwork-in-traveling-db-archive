from django.db import models
import uuid

class AllProducts(models.Model):

    CATEGORY_CHOICES = [
        ('Macrame', 'Macrame'),
        ('Maroquinerie', 'Maroquinerie'),
        ('Hybride', 'Hybride'),
        ('Entretien', 'Entretien')
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
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    ornement = models.CharField(max_length=200, blank=True, null=True)
    prix = models.FloatField(default=0.0)
    lien_image1 = models.URLField(default='', max_length=20000, blank=True, null=True)
    lien_image2 = models.URLField(default='', max_length=20000, blank=True, null=True)
    lien_image3 = models.URLField(default='', max_length=20000, blank=True, null=True)
    lien_image4 = models.URLField(default='', max_length=20000, blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
    
class Cart(models.Model):
    section_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(AllProducts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)