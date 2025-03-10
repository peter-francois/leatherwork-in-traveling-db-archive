from django.db import models
import uuid
from cloudinary.models import CloudinaryField

class AllProducts(models.Model):

    CATEGORY_CHOICES = [
        ('Hybride', 'Hybride'),
        ('Macrame', 'Macrame'),
        ('Maroquinerie', 'Maroquinerie'),
    ]
    TYPE_CHOICES = [

        ('Blague à tabac', 'Blague à tabac'),
        ('Boucles d\'oreilles', 'Boucles d\'oreilles'),
        ('Bracelet', 'Bracelet'),
        ('Ceinture', 'Ceinture'),
        ('Chaine de corps', 'Chaine de corps'),
        ('Chevillère', 'Chevillère'),
        ('Collier', 'Collier'),
        ('Collier chien', 'Collier chien'),
        ('Divers', 'Divers'),
        ('Entretien', 'Entretien'),
        ('Murale', 'Murale'),
        ('Portefeuille, Porte carte', 'Portefeuille, Porte carte'),
        ('Sac divers', 'Sac divers'),
    ]
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.CharField(max_length=200, blank=True, null=True)
    prix = models.FloatField(default=0.0)
    image1 = CloudinaryField(default='', blank=True, null=True)
    image2 = CloudinaryField(default='', blank=True, null=True)
    image3 = CloudinaryField(default='', blank=True, null=True)
    image4 = CloudinaryField(default='', blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
    
class Cart(models.Model):
    session_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart {self.uuid}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(AllProducts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)