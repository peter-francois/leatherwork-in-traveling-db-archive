import os
import requests
from django.conf import settings

def get_cached_image(cloudinary_url, filename):
    # Ajoute transformation f_auto si pas déjà présente
    if '/upload/' in cloudinary_url and 'f_auto' not in cloudinary_url:
        cloudinary_url = cloudinary_url.replace('/upload/', '/upload/f_auto/')

    cache_dir = os.path.join(settings.MEDIA_ROOT, "cache")
    os.makedirs(cache_dir, exist_ok=True)

    local_path = os.path.join(cache_dir, filename)

    if not os.path.exists(local_path):
        response = requests.get(cloudinary_url, stream=True)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

    return f"{settings.MEDIA_URL}cache/{filename}"
    
def get_cached_images_for_product(product):
    """
    Retourne un dict des URLs d'images en cache pour un produit donné.
    """
    def cache_img_field(image_field, suffix):
        if not image_field:
            return ""
        filename = f"{product.id}_{suffix}_{int(product.updated_at.timestamp())}.jpg"
        return get_cached_image(image_field.url, filename)

    return {
        'image1': cache_img_field(product.image1, "img1"),
        'image2': cache_img_field(product.image2, "img2"),
        'image3': cache_img_field(product.image3, "img3"),
        'image4': cache_img_field(product.image4, "img4"),
        'image5': cache_img_field(product.image5, "img5"),
        'image6': cache_img_field(product.image6, "img6"),
    }