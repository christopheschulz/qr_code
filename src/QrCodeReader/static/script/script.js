document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".navbar a");

    function setActiveLink() {
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            if (link.href.includes(currentPath)) {
                link.classList.add("active");
            } else {
                link.classList.remove("active");
            }
        });
    }

    // Appliquer la classe active en fonction de l'URL actuelle
    setActiveLink();

    // Ajouter un gestionnaire d'événements pour les clics sur les liens de navigation
    navLinks.forEach(link => {
        link.addEventListener("click", function () {
            navLinks.forEach(l => l.classList.remove("active"));
            this.classList.add("active");

            // Stocker la sélection dans le localStorage
            localStorage.setItem("activeNav", this.getAttribute("href"));
        });
    });

    // Récupérer la sélection sauvegardée après un rechargement de page
    const savedActiveNav = localStorage.getItem("activeNav");
    if (savedActiveNav) {
        navLinks.forEach(link => {
            if (link.getAttribute("href") === savedActiveNav) {
                link.classList.add("active");
            }
        });
    }
});


document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".qr-option-btn");
    const contentDivs = document.querySelectorAll(".qr-content");

    // Définir le bouton URL comme actif par défaut
    let activeButton = document.querySelector(".qr-option-btn[data-target='url-content']");
    let activeDiv = document.getElementById("url-content");

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            // Retirer la classe 'active' de tous les boutons
            buttons.forEach(btn => btn.classList.remove("bg-blue-800"));

            // Cacher toutes les divs de contenu
            contentDivs.forEach(div => div.classList.add("hidden"));

            // Ajouter la classe 'active' au bouton cliqué
            this.classList.add("bg-blue-800", "text-white");

            // Afficher la div correspondante
            const targetId = this.getAttribute("data-target");
            document.getElementById(targetId).classList.remove("hidden");
        });
    });

    // Assurer que le bouton URL est actif au démarrage
    activeButton.classList.add("bg-blue-800", "text-white");
    activeDiv.classList.remove("hidden");
});