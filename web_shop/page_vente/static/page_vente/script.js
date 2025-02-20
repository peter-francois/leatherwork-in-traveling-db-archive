const flags = document.querySelectorAll('.flag');

// Initialisation de la langue par défaut
let currentLanguage = localStorage.getItem('language') || 'fr';
changeLanguage(currentLanguage);

// Fonction pour changer la langue
function changeLanguage(lang) {
    currentLanguage = lang;
    localStorage.setItem('language', currentLanguage); // Mettre à jour la langue dans le stockage local

    // Mettre à jour le contenu de la page grace au fichier translations.JSON
    fetch('/static/page_vente/translations.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data[lang]) {
                console.error(`Language ${lang} not found in translations`);
                return;
            }
            const translations = data[lang];
            
            // Liste des éléments à traduire
            const elementsToTranslate = {
                'title_page_index': translations.title_page_index,
                'title_index': translations.title_index,
                'menu_button_home':translations.menu_button_home,
                'menu_button_produit':translations.menu_button_produit,
                'menu_button_panier':translations.menu_button_panier,
                'menu_button_a_propos':translations.menu_button_a_propos,
                'menu_button_tous_les_produits':translations.menu_button_tous_les_produits,
                'menu_button_maroquinerie':translations.menu_button_maroquinerie,
                'menu_button_macrames':translations.menu_button_macrames,
                'menu_button_hybride':translations.menu_button_hybride,
                'menu_button_creation_sur_mesure':translations.menu_button_creation_sur_mesure,
                'macrames_title':translations.macrames_title,
                'macrames_description':translations.macrames_description,
                'creation_sur_mesure_title':translations.creation_sur_mesure_title,
                'creation_sur_mesure_description':translations.creation_sur_mesure_description,
                'maroquinerie_title':translations.maroquinerie_title,
                'maroquinerie_description':translations.maroquinerie_description,
                'hybride_title':translations.hybride_title,
                'autres_produits_description':translations.autres_produits_description,
                'title_page_cart':translations.title_page_cart,
                'title_panier':translations.title_panier,
                'vider_panier':translations.vider_panier,
                'panier_vide':translations.panier_vide,
                'title_page_all_products':translations.title_page_all_products,
                'title_all_products':translations.title_all_products

            };

            // Mettre à jour chaque élément s'il existe
            for (const [id, text] of Object.entries(elementsToTranslate)) {
                const element = document.getElementById(id);
                if (element) {
                    element.innerHTML = text;
                }
            }
            
            // Met à jour l'état actif des drapeaux
            flags.forEach(flag => {
                flag.classList.toggle('active', flag.getAttribute('data-lang') === lang);
            });
        })
        .catch(error => {
            console.error('Error fetching translations:', error);
        });
}


// Écouteurs d'événements pour les clics sur les drapeaux
flags.forEach(flag => {
    flag.addEventListener('click', () => {
        const selectedLang = flag.getAttribute('data-lang');
        changeLanguage(selectedLang);
    });
});

// Fonction pour afficher le menu
function toggleMenu() {
    const menuContent = document.querySelector('.menu-content');
    const menuButton = document.querySelector('.menu button');
    const menuContentProduit = document.querySelector('.menu-content-produit');
    menuContent.classList.toggle('active');
    menuButton.classList.toggle('active');
    if (menuContentProduit.classList.contains('active')) {
        menuContentProduit.classList.remove('active');
    }
}

// Fermer le menu si on clique en dehors
document.addEventListener('click', function(event) {
    const menuButton = document.querySelector('.menu button');
    const menuContent = document.querySelector('.menu-content');
    const menuContentProduit = document.querySelector('.menu-content-produit');
    
    // Si le clic n'est ni sur le bouton du menu ni sur le contenu du menu et que le manu est actif
    if (!menuButton.contains(event.target) && !menuContent.contains(event.target) && menuContent.classList.contains('active')) {
        menuContent.classList.remove('active');
        menuButton.classList.remove('active');
        if (menuContentProduit.classList.contains('active')) {
            menuContentProduit.classList.remove('active');
        }
    }
});

// Fonction pour afficher le sous-menu "Produit"
function toggleMenuProduit(event){
    event.preventDefault();
    const menuContentProduit = document.querySelector('.menu-content-produit');
    menuContentProduit.classList.toggle('active');
}

// Pour que le menu modifie son style en fonction de la scroll
window.addEventListener('scroll', function() {
    const menuContent = document.querySelector('.menu-content');
    const menuButton = document.querySelector('.menu button');
    const headerDiv = document.querySelector('div.header');
    const headerTop = headerDiv.offsetTop + 40;
    if (window.scrollY >= headerTop) { // quand on dépasse la div.header
        menuContent.classList.add('scrolled');
        menuButton.classList.add('scrolled');
    } else {
        menuContent.classList.remove('scrolled');
        menuButton.classList.remove('scrolled');
    }
});



document.addEventListener('DOMContentLoaded', function () {
    // Ecouteur d'evenement sur les images pour afficher une div avec toute les images
    const produits = document.querySelectorAll('.produit');
    produits.forEach(produit => {
        const img = produit.querySelector('img'); // Sélectionner l'image principale
        if (img) {
            img.addEventListener('click', () => {
                const articleId = produit.getAttribute('data-product-id');
                if (!articleId) return;
                afficherImages(articleId);
            });
        }
    });
    afficherPanier();  // Charger les articles du panier au démarrage
});



// Fonction pour afficher les articles du panier
function afficherPanier() {
    fetch('/cart_detail/')
        .then(response => response.json())
        .then(data => {
            let listeArticles = document.getElementById('liste-articles');
            const textCartButton = document.getElementById('text-cart-button');
            if (listeArticles) {
            listeArticles.innerHTML = ''; 
            data.cart.forEach(article => {
                let li = document.createElement('li');
                let img = document.createElement('img');
                let button = document.createElement('button');
                li.textContent = `${article.nom} - ${article.prix} € (x${article.quantity})`;
                if (article.lien_image1) {
                    img.src = `${article.lien_image1}`;
                    li.appendChild(img);
                }
                button.textContent = 'Supprimer';
                button.onclick = () => remove_from_cart(article.id);
                li.appendChild(button);
                listeArticles.appendChild(li);
                textCartButton.textContent = data.cart.length;
            });
        } else {
            return;
        }
        })
        .catch(error => console.error('Erreur lors de la récupération du panier:', error));
}

// Helper function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Ajouter un produit au panier
function ajouterAuPanier(articleId) {
    fetch(`/add_to_cart/${articleId}/`, { 
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                afficherPanier(); // Mettre à jour l'affichage du panier
                location.reload(); // Rafraîchir pour mettre à jour la disponibilité
            } else {
                alert("Erreur : " + data.message);
            }
        });
}

// Fonction pour vider le panier
function viderPanier() {
    fetch('/vider_panier/', { 
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                afficherPanier();
                location.reload();
            } else {
                alert("Erreur lors de la suppression du panier.");
            }
        });
}

// Fonction pour supprimer un article du panier
function remove_from_cart(articleId) {
    fetch(`/remove_from_cart/${articleId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                afficherPanier();
                location.reload();
            } else {
                alert("Erreur lors de la suppression de l'article.");
            }
        });
}

let currentImageIndex = 0; // Index de l'image actuelle
let images = []; // Tableau pour stocker les images


// Fonction pour afficher les images d'un article avec le nom de l'article
function afficherImages(articleId) {
    fetch(`/get_product_images/${articleId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json()
        })
        .then(data => {
            document.getElementById('nom-article').textContent = data.nom;
            images = data.images; // Charger les images dans le tableau
            currentImageIndex = 0; // Réinitialiser l'index
            document.getElementById('current-image').src = images[currentImageIndex]; // Afficher la première image
            const modal = document.getElementById('modal');
            modal.style.display = 'block'; // Afficher la modale
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
// Fonction pour changer d'image
function changeImage(direction) {
    currentImageIndex += direction; // Changer l'index
    if (currentImageIndex < 0) {
        currentImageIndex = images.length - 1; // Revenir à la dernière image
    } else if (currentImageIndex >= images.length) {
        currentImageIndex = 0; // Revenir à la première image
    }
    document.getElementById('current-image').src = images[currentImageIndex]; // Mettre à jour l'image affichée
}

// Fonction pour fermer la modale
function fermerModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}