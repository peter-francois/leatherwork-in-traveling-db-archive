const flags = document.querySelectorAll('.flag');

// Fonction pour changer la langue
function changeLanguage(lang) {
    // Mettre à jour le contenu de la page grace au fichier translations.JSON
    fetch('translations.json')
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
                'description': translations.description,

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

// Définir la langue par défaut au chargement
document.addEventListener('DOMContentLoaded', () => {
    changeLanguage('en'); // Langue par défaut
});

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
    menuContent.classList.toggle('active');
    menuButton.classList.toggle('active');
}

// Fermer le menu si on clique en dehors
document.addEventListener('click', function(event) {
    const menuButton = document.querySelector('.menu button');
    const menuContent = document.querySelector('.menu-content');
    
    // Si le clic n'est ni sur le bouton du menu ni sur le contenu du menu et que le manu est actif
    if (!menuButton.contains(event.target) && !menuContent.contains(event.target) && menuContent.classList.contains('active')) {
        menuContent.classList.remove('active');
        menuButton.classList.remove('active');
    }
});
// Pour que le menu modifie son style en fonction de la scroll
window.addEventListener('scroll', function() {
    const menuContent = document.querySelector('.menu-content');
    const menuButton = document.querySelector('.menu button');
    const headerDiv = document.querySelector('div.header');
    const headerBottom = headerDiv.offsetTop + headerDiv.offsetHeight -30;
    if (window.scrollY >= headerBottom) { // quand on dépasse la div.header
        menuContent.classList.add('scrolled');
        menuButton.classList.add('scrolled');
    } else {
        menuContent.classList.remove('scrolled');
        menuButton.classList.remove('scrolled');
    }
});
