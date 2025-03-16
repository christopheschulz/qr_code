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
