/**
 * GESTION DE LA NAVIGATION PRINCIPALE
 * Gère l'état actif des liens de navigation et le menu mobile
 */

document.addEventListener("DOMContentLoaded", function () {
    console.log("🔍 Navigation script chargé");
    
    // Gestion du menu mobile
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const isHidden = mobileMenu.classList.contains('hidden');
            if (isHidden) {
                mobileMenu.classList.remove('hidden');
                // Changer l'icône du bouton (hamburger → croix)
                mobileMenuButton.querySelector('svg:first-child').classList.add('hidden');
                mobileMenuButton.querySelector('svg:last-child').classList.remove('hidden');
            } else {
                mobileMenu.classList.add('hidden');
                // Changer l'icône du bouton (croix → hamburger)
                mobileMenuButton.querySelector('svg:first-child').classList.remove('hidden');
                mobileMenuButton.querySelector('svg:last-child').classList.add('hidden');
            }
        });
    }
    
    // Gestion des liens actifs
    const navLinks = document.querySelectorAll(".nav-link");
    const currentPath = window.location.pathname;
    
    console.log("📍 Chemin actuel:", currentPath);
    console.log("🔗 Liens trouvés:", navLinks.length);

    // Fonction pour nettoyer et normaliser un chemin
    function normalizePath(path) {
        path = path.replace(/^\/+|\/+$/g, '');
        path = path.split('?')[0];
        return path;
    }

    // Fonction pour vérifier si un lien est actif
    function isLinkActive(linkPath, currentPath) {
        const normalizedLinkPath = normalizePath(linkPath);
        const normalizedCurrentPath = normalizePath(currentPath);

        console.log("🔍 Comparaison:", normalizedLinkPath, "vs", normalizedCurrentPath);

        // Cas spécial pour la page d'accueil
        if (normalizedLinkPath === '' && (normalizedCurrentPath === '' || normalizedCurrentPath === 'index')) {
            return true;
        }

        return normalizedCurrentPath === normalizedLinkPath;
    }

    navLinks.forEach((link, index) => {
        const linkPath = new URL(link.href).pathname;
        const isActive = isLinkActive(linkPath, currentPath);
        
        console.log(`🔗 Lien ${index + 1}: ${link.textContent.trim()} - ${linkPath} - Actif: ${isActive}`);
        
        if (isActive) {
            link.classList.add("active");
            console.log("✅ Classe active ajoutée pour lien actif");
        } else {
            link.classList.remove("active");
        }
    });
});