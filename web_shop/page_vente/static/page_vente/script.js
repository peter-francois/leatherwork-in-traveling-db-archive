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
                'no_products':translations.no_products,
                'title_cart':translations.title_cart,
                'empty_cart':translations.empty_cart,
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
                'expiration_soon':translations.expiration_soon,
                'footer_about':translations.footer_about,
                'footer_history':translations.footer_history,
                'footer_legal':translations.footer_legal,
                'footer_mention':translations.footer_mention,
                'footer_cgv':translations.footer_cgv,
                'footer_policy':translations.footer_policy,
                'footer_cookie':translations.footer_cookie,
                'footer_social':translations.footer_social,
                'footer_payment':translations.footer_payment,
                'footer_payment_description':translations.footer_payment_description,
                'footer_copyright':translations.footer_copyright,
                'contact_title':translations.contact_title,
                'contact_description1':translations.contact_description1,
                'contact_description2':translations.contact_description2,
                'contact_description3':translations.contact_description3,
                'contact_description4':translations.contact_description4,
                'contact_description5':translations.contact_description5,
                'contact_description6':translations.contact_description6,
                'payment_title':translations.payment_title,
                'shipping_cost':translations.shipping_cost,
                'insurance_25_euros':translations.insurance_25_euros,
                'with_our_partner_mondial_relay':translations.with_our_partner_mondial_relay,
                'mandatory_insurance_2':translations.mandatory_insurance_2,
                'mandatory_insurance_3':translations.mandatory_insurance_3,
                'mandatory_insurance_4':translations.mandatory_insurance_4,
                'total_articles_title':translations.total_articles_title,
                'shipping_cost_short':translations.shipping_cost_short,
                'insurance_cost':translations.insurance_cost,
                'insurance_25_euros_2':translations.insurance_25_euros_2,
                'add-insurance-label':translations.add_insurance_label,
                'total_amount_title':translations.total_amount_title,
                'accept-cgv-label':translations.accept_cgv_label,
                'checkout':translations.checkout,
                'error-message':translations.error_message,
                'clear_cart':translations.clear_cart,
                'info-price':translations.info_price,
                
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
    const contactButton = document.querySelector('#contact_button');
    
    // Si le clic n'est ni sur le bouton du menu ni sur le contenu du menu et que le menu est actif
    if (contactButton.contains(event.target) || !menuButton.contains(event.target) && !menuContent.contains(event.target) && menuContent.classList.contains('active')) {
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

//fonction pour afficher le contact
function displayContact(event) {

    const ContactDiv = document.querySelector('#contact-form');
    const overlay = document.querySelector('#overlay');
    ContactDiv.style.display = 'block';
    overlay.style.display = 'block'; // Affiche l'overlay
}

// Fonction pour masquer le contact
function hideContact() {
    const ContactDiv = document.querySelector('#contact-form');
    const overlay = document.querySelector('#overlay');
    overlay.style.display = 'none'; // Masque l'overlay
    ContactDiv.style.display = 'none';
}
// Fonction pour fermer le contact et le modal si on clique sur l'overlay
document.addEventListener('click', function(event) {
    const overlay = document.querySelector('#overlay');
    if (overlay.contains(event.target)) {
        hideContact();
        closeModal();
    }
});

// Fontion au chargement de la page
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
    displayCart();
    initCart();
    updateTextCartButton(); 
    if (window.location.pathname.includes('panier')){
        if(document.getElementById('order-total')){
            updateInsurance();
            updateTotal();
            updateCartVisibility();
            
        }
    }
});

// Fonction pour afficher les articles du panier
function displayCart() {
    fetch('/cart_detail/')
        .then(response => response.json())
        .then(data => {

            let listeArticles = document.getElementById('liste-articles');
            if (listeArticles) {
            listeArticles.innerHTML = ''; 
            data.cart.forEach(article => {
                let li = document.createElement('li');
                let img = document.createElement('img');
                let p = document.createElement('p');
                let span = document.createElement('span');
                let span2 = document.createElement('span');
                span.classList.add('price_article');
                span.textContent = `${article.prix.toFixed(2)}`;
                span2.textContent = `€ (x${article.quantity})`;
                p.appendChild(span);
                p.appendChild(span2);
                img.onclick = () => displayProductImages(article.id);
                let button = document.createElement('button');
                button.textContent = 'Supprimer';
                button.onclick = () => remove_from_cart(article.id);
                button.classList.add('page-button', 'delete_button');
                li.textContent = `${article.nom}`;
                li.appendChild(p);
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

                li.appendChild(button);
                listeArticles.appendChild(li);
            });
        }
    }).catch(error => console.error('Erreur lors de la récupération du panier:', error));
}

// Fonction pour récupérer le token CSRF depuis le meta tag
function getCSRFTokenFromMeta() {
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
    return csrfTokenMeta ? csrfTokenMeta.getAttribute('content') : '';
}
function initCart() {
    if (!localStorage.getItem('cart')) {
        localStorage.setItem('cart', JSON.stringify([]));
    }
}
// Ajouter un produit au panier
function addToCart(articleId) {
    fetch(`/add_to_cart/${articleId}/`, { 
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFTokenFromMeta(),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Sauvegarde dans le localStorage pour qu'il persiste entre les sessions
                localStorage.setItem('cart_uuid', data.cart_uuid);
                let cart = JSON.parse(localStorage.getItem('cart')) || [];
                cart.push({ id: articleId});
                localStorage.setItem('cart', JSON.stringify(cart));
                alert(data.message);
                updateTextCartButton(); 
                updateProductList(articleId);  // Met à jour la liste des produits en retirant celui qui a été ajouté
            } else {
                alert("Erreur : " + data.message);
            }
        }).catch(error => {
            console.error('Erreur lors de l\'ajout au panier:', error);
        });
}
function updateProductList(articleId) {
    // Trouver l'élément HTML représentant cet article et le supprimer
    const allProducts = Array.from(document.querySelectorAll('.produit')); 
    const productElement = allProducts.find(product => product.getAttribute('data-product-id') === articleId);
    
    if (productElement) {
        productElement.style.display = 'none';  // Masquer l'élément du DOM
    }
}

// Fonction pour obtenir le nombre d'articles dans le panier
async function getNumberOfProductsInCart() {
    const response = await fetch(`/get_number_of_products_in_cart/`, { 
        method: 'GET',
        headers: {
            'X-CSRFToken': getCSRFTokenFromMeta(),
            'Content-Type': 'application/json'
        }
    });

    const data = await response.json();
    // Retourne directement le nombre d'articles
    if (data.success) {
        console.log("data success", data.number_of_products);
        return data.number_of_products;
    } else {
        console.log("data error", data);
        return 0; // Retourne 0 si il y a une erreur
    }
}

// Fonction pour mettre à jour l'affichage du nombre d'articles dans le panier
async function updateTextCartButton() {
    const textCartButton = document.getElementById('text-cart-button');
    if (!textCartButton) return;

    // Récupérer le nombre d'articles dans le panier
    const numberOfProducts = await getNumberOfProductsInCart();
    
    // Mettre à jour l'affichage du bouton
    textCartButton.textContent = numberOfProducts;

}

// Au chargement de la page, vérifier si l'UUID du panier est dans localStorage
window.onload = function() {
    const cart_uuid = localStorage.getItem('cart_uuid'); // Récupère l'UUID depuis localStorage
    if (cart_uuid) {
        window.cart_uuid = cart_uuid; // Assigner à la variable globale pour usage ultérieur
        console.log("UUID du panier récupéré depuis localStorage:", window.cart_uuid);
    } else {
        console.log("Aucun UUID trouvé dans localStorage.");
    }
};
// Fonction pour mettre à jour l'affichage du panier
function updateCartVisibility() {
    const orderTotal = parseFloat(document.getElementById('order-total').textContent.replace(',', '.'));
    const cartSection = document.querySelector('.cart-container');
    const emptyCartMessage = document.querySelector('#empty-section');

    // Si le total est 0 ou indéfini, on considère le panier vide
    if (orderTotal <= 0 || isNaN(orderTotal)) {
        cartSection.style.display = 'none';
        emptyCartMessage.style.display = 'block'; // Affiche le message "Votre panier est vide"
    } else {
        cartSection.style.display = 'block';
        emptyCartMessage.style.display = 'none'; // Cache le message si le panier n'est pas vide
    }
}
// Fonction pour vider le panier
function clearCart() {
    fetch('/vider_panier/', { 
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFTokenFromMeta(),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Réinitialise le localStorage
                localStorage.removeItem('cart');
                const addInsurance = document.getElementById('add-insurance');
                addInsurance.checked = false;
                alert(data.message);
                document.getElementById('order-total').textContent = '0.00';
                document.getElementById('total-amount').textContent = '0.00';
                updateCartVisibility();
                initCart();
                updateTextCartButton();
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
            'X-CSRFToken': getCSRFTokenFromMeta(),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let cart = JSON.parse(localStorage.getItem('cart')) || [];                
                cart = cart.filter(item => parseInt(item.id) !== parseInt(articleId));
                localStorage.setItem('cart', JSON.stringify(cart));
                const addInsurance = document.getElementById('add-insurance');
                let orderTotal = parseFloat(document.getElementById('order-total').textContent.replace(',', '.'));
                const priceArticle = parseFloat(data.article.prix.toFixed(2));
                orderTotal -= priceArticle;
                document.getElementById('order-total').textContent = orderTotal.toFixed(2);
                if (orderTotal<25) {
                    addInsurance.checked = false;
                }
                updateInsurance();
                updateTotal();
                updateTextCartButton();
                alert(data.message);
                
            } else {
                alert("Erreur lors de la suppression de l'article.");
            }
        
        }).finally(()=>{
            displayCart();
            updateCartVisibility();
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
            if (data.description){
            document.getElementById('description-article').textContent = data.description;
            }else{
                if (currentLanguage == 'en')
                document.getElementById('description-article').textContent = 'No description available';
                else
                document.getElementById('description-article').textContent = 'Aucune description disponible';
            }
            document.getElementById('prix-article').textContent = data.prix.toFixed(2).replace('.', ',') + ' €';
            images = data.images; // Charger les images dans le tableau
            currentImageIndex = 0; // Réinitialiser l'index
            document.getElementById('current-image').src = images[currentImageIndex]; // Afficher la première image
            const modal = document.getElementById('modal');
            const overlay = document.getElementById('overlay');
            overlay.style.display = 'block'; // Affiche l'overlay
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
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'none'; // Masque l'overlay
    modal.style.display = 'none';
}
// Fonction pour mettre à jour l'assurance

function updateInsurance() {
    const orderTotal = parseFloat(document.getElementById('order-total').textContent.replace(',', '.'));
    const insuranceOption = document.getElementById('insurance-option'); // Checkbox assurance optionnelle
    const mandatoryInsurance = document.getElementById('mandatory-insurance'); // Assurance obligatoire
    const insuranceCostSpan = document.getElementById('insurance-cost'); // Prix assurance optionnelle
    const mandatoryInsuranceCostSpan = document.getElementById('mandatory-insurance-cost'); // Prix assurance obligatoire
    const insurance25Euros = document.getElementById('insurance_25_euros'); // Message pour 25€ d'assurance incluse
    const insurance25Euros2 = document.getElementById('insurance_25_euros_2'); // Message pour 25€ d'assurance incluse
    const insurance = document.getElementById('insurance');
    const upTo500 = document.getElementById('mandatory_insurance_4');

    // Cacher toutes les options par défaut
    insuranceOption.classList.add('hidden');
    mandatoryInsurance.classList.add('hidden');
    insurance25Euros.classList.remove('hidden');
    insurance25Euros2.classList.remove('hidden');
    insurance.classList.remove('hidden');
    upTo500.classList.add('hidden');
    insuranceCostSpan.textContent = "0,00";
    mandatoryInsuranceCostSpan.textContent = "0,00";


    // 1. Gestion de l'assurance optionnelle entre 25 € et 50 €
    if (orderTotal > 25 && orderTotal <= 50) {
        insuranceOption.classList.remove('hidden'); // Afficher l'option d'assurance
        insurance.classList.add('hidden');
        if (insuranceOption.checked){
        insuranceCostSpan.textContent = "2,00"; // Coût fixe pour cette tranche
        }
    }

    // 2. Gestion de l'assurance obligatoire au-delà de 50 €
    if (orderTotal > 50) {
        insurance25Euros.classList.add('hidden');
        insurance25Euros2.classList.add('hidden');
        mandatoryInsurance.classList.remove('hidden');

        // Définir le coût de l'assurance obligatoire en fonction du total
        if (orderTotal > 500) {
            upTo500.classList.remove('hidden');
            mandatoryInsuranceCostSpan.textContent = "8.00";
            insuranceCostSpan.textContent = "8.00";
        } else if (orderTotal > 375) {
            mandatoryInsuranceCostSpan.textContent = "8.00";
            insuranceCostSpan.textContent = "8.00";
        } else if (orderTotal > 250) {
            mandatoryInsuranceCostSpan.textContent = "6.50";
            insuranceCostSpan.textContent = "6.50";
        } else if (orderTotal > 125) {
            mandatoryInsuranceCostSpan.textContent = "5.00";
            insuranceCostSpan.textContent = "5.00";
        } else {
            mandatoryInsuranceCostSpan.textContent = "3.50";
            insuranceCostSpan.textContent = "3.50";
        }
    }

}
// Fonction pour mettre à jour le total
function updateTotal() {
    const orderTotal = parseFloat(document.getElementById('order-total').textContent.replace(',', '.'));
    const insuranceCost = parseFloat(document.getElementById('insurance-cost').textContent.replace(',', '.'))|| 0;

    // Checkbox assurance optionnelle
    const addInsurance = document.getElementById('add-insurance').checked;
    let totalAmount = orderTotal + 5.00 + insuranceCost;
    if (addInsurance) {
        totalAmount += 2.00;
    }
    

    document.getElementById('total-amount').textContent = totalAmount.toFixed(2);

}

// Fonction pour gérer le checkout
function handleCheckout() {
    const acceptCGV = document.getElementById('accept-cgv').checked;
    const addInsurance = document.getElementById('add-insurance').checked;
    const errorMessage = document.getElementById('error-message');
    const orderTotal = document.getElementById('total-amount').textContent;

    if (!acceptCGV) {
      errorMessage.classList.remove('hidden');
      return;
    }

    errorMessage.classList.add('hidden');

    // Récupérer l'UUID du panier depuis le localStorage
    const cart_uuid = localStorage.getItem('cart_uuid');


    if (!cart_uuid) {
        console.error("L'UUID du panier est introuvable.");
        return;
    }
    // Redirige vers Stripe avec le montant total
    window.location.href = `/checkout/?front_total=${orderTotal}&cart_uuid=${cart_uuid}&insurance=${addInsurance ? 1 : 0}&acceptCGV=${acceptCGV ? 1 : 0}`;
  }
// débug
  function debugElements() {
    console.log("🔍 Debug des éléments DOM :");
    console.log("order-total :", document.getElementById('order-total'));
    console.log("insurance-cost :", document.getElementById('insurance-cost'));
    console.log("add-insurance :", document.getElementById('add-insurance'));
    console.log("total-amount :", document.getElementById('total-amount'));
}