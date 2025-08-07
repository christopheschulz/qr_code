/**
 * GESTION DE LA NAVIGATION PRINCIPALE
 * Gère uniquement le menu mobile (l'état actif est géré côté serveur)
 */

// TEST URGENT : Vérifier si le script se charge
console.log("🚨 NAVIGATION JS CHARGÉ - Version de test");

document.addEventListener("DOMContentLoaded", function () {
    console.log("🔍 Navigation script - DOM Ready");
    
    // Gestion du menu mobile uniquement
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    console.log("📱 Mobile button found:", !!mobileMenuButton);
    console.log("📱 Mobile menu found:", !!mobileMenu);
    
    if (mobileMenuButton && mobileMenu) {
        console.log("✅ Ajout du listener sur le bouton mobile");
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