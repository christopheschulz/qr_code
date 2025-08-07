/**
 * GESTION DE LA NAVIGATION PRINCIPALE
 * Gère uniquement le menu mobile (l'état actif est géré côté serveur)
 */

document.addEventListener("DOMContentLoaded", function () {
    console.log("🔍 Navigation script chargé");
    
    // Gestion du menu mobile uniquement
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
    
    console.log("✅ Menu mobile configuré");
});