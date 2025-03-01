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
                'any_question':translations.any_question,
                'title_page_all_products':translations.title_page_all_products,
                'title_all_products':translations.title_all_products,
                'description_all_products':translations.description_all_products,
                'filter_button':translations.filter_button,
                'contact_link':translations.contact_link,     
                'of':translations.of,
                'of2':translations.of,
                'no_image':translations.no_image,
                'title_cart':translations.title_cart,
                'empty_cart':translations.empty_cart,
                'checkout':translations.checkout,
                'clear_cart':translations.clear_cart,
                'title_page_leathercraft':translations.title_page_leathercraft,
                'title_leathercraft':translations.title_leathercraft,
                'description_leathercraft':translations.description_leathercraft,
                'title_page_macrame':translations.title_page_macrame,
                'title_macrame':translations.title_macrame,
                'description_macrame':translations.description_macrame,
                'title_page_hybride':translations.title_page_hybride,
                'title_hybride':translations.title_hybride,
                'description_hybride':translations.description_hybride,
                'expiration_date':translations.expiration_date,
                'expiration_soon':translations.expiration_soon
            };

            // Mettre à jour chaque élément s'il existe
            for (const [id, text] of Object.entries(elementsToTranslate)) {
                const element = document.getElementById(id);
                if (element) {
                    element.innerHTML = text;
                }
            }
            // Met à jour le placeholder du champ de recherche
            const searchField = document.getElementById('search_field');
            if (searchField) {
                searchField.placeholder = translations.search_field;
            }
            // Met à jour le label du champ de recherche
            const searchLabel = document.querySelector('label[for="search_field"]');
            if (searchLabel) {
                searchLabel.innerHTML = translations.search_label;
            }
            const minPriceLabel = document.querySelector('label[for="id_min_price"]');
            if (minPriceLabel) {
                minPriceLabel.innerHTML = translations.min_price;
            }
            const maxPriceLabel = document.querySelector('label[for="id_max_price"]');
            if (maxPriceLabel) {
                maxPriceLabel.innerHTML = translations.max_price;
            }
            const price = document.querySelectorAll('.prices');
            if (price) {
                price.forEach(element => {
                    element.innerHTML = translations.price;
                });
            }
            const add_to_cart_button = document.querySelectorAll('.add_to_cart_button');
            if (add_to_cart_button) {
                add_to_cart_button.forEach(element => {
                    element.innerHTML = translations.add_to_cart_button;
                });
            }
            const previous_button = document.querySelectorAll('.prev-button');
            if (previous_button) {
                previous_button.forEach(element => {
                    element.innerHTML = translations.previous_button;
                });
            }
            const next_button = document.querySelectorAll('.next-button');
            if (next_button) {
                next_button.forEach(element => {
                    element.innerHTML = translations.next_button;
                });
            }
            const first_button = document.querySelectorAll('.first-button');
            if (first_button) {
                first_button.forEach(element => {
                    element.innerHTML = translations.first_button;
                });
            }
            const last_button = document.querySelectorAll('.last-button');
            if (last_button) {
                last_button.forEach(element => {
                    element.innerHTML = translations.last_button;
                });
            }
            const delete_button = document.querySelectorAll('.delete_button');
            if (delete_button) {
                delete_button.forEach(element => {
                    element.innerHTML = translations.delete_button;
                });
            }
            const no_image = document.querySelectorAll('.no-image');
            if (no_image) {
                no_image.forEach(element => {
                    element.innerHTML = translations.no_image;
                });
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
                displayProductImages(articleId);
            });
        }
    });
    displayCart();  // Charger les articles du panier au démarrage
});



// Fonction pour afficher les articles du panier
function displayCart() {
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
                img.onclick = () => displayProductImages(article.id);
                let button = document.createElement('button');
                button.classList.add('page-button', 'delete_button');
                li.textContent = `${article.nom} - ${article.prix.toFixed(2)} € (x${article.quantity})`;
                if (article.image1) {
                    img.src = `${article.image1}`;
                    img.alt = `${article.nom}`;
                    li.appendChild(img);
                }
                else if (article.image2) {
                    img.src = `${article.image2}`;
                    img.alt = `${article.nom}`;
                    li.appendChild(img);
                }
                else if (article.image3) {
                    img.src = `${article.image3}`;
                    img.alt = `${article.nom}`;
                    li.appendChild(img);
                }
                else if (article.image4) {
                    img.src = `${article.image4}`;
                    img.alt = `${article.nom}`;
                    li.appendChild(img);
                }
                else {
                    img.src = ''; // Aucune image disponible
                    let p = document.createElement('p');
                    p.classList.add('no-image');
                    p.textContent = 'Aucune image disponible';
                    li.appendChild(p);
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
function addToCart(articleId) {
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
                displayCart(); // Mettre à jour l'affichage du panier
                location.reload(); // Rafraîchir pour mettre à jour la disponibilité
            } else {
                alert("Erreur : " + data.message);
            }
        });
}

// Fonction pour vider le panier
function clearCart() {
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
                displayCart();
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
                displayCart();
                location.reload();
            } else {
                alert("Erreur lors de la suppression de l'article.");
            }
        });
}

let currentImageIndex = 0; // Index de l'image actuelle
let images = []; // Tableau pour stocker les images


// Fonction pour afficher les images d'un article avec le nom de l'article
function displayProductImages(articleId) {
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
function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}