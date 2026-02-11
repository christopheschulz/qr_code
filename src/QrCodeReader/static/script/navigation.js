/**
 * GESTION DE LA NAVIGATION PRINCIPALE
 * Menu mobile avec animation slide-down + gestion accordeon guide
 */

document.addEventListener("DOMContentLoaded", function () {
    // --- Menu mobile ---
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const isOpen = mobileMenu.style.maxHeight && mobileMenu.style.maxHeight !== '0px';
            if (isOpen) {
                // Fermer
                mobileMenu.style.maxHeight = '0px';
                mobileMenuButton.querySelector('svg:first-child').classList.remove('hidden');
                mobileMenuButton.querySelector('svg:last-child').classList.add('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
            } else {
                // Ouvrir
                mobileMenu.style.maxHeight = mobileMenu.scrollHeight + 'px';
                mobileMenuButton.querySelector('svg:first-child').classList.add('hidden');
                mobileMenuButton.querySelector('svg:last-child').classList.remove('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'true');
            }
        });
    }

    // --- Accordeon guide d'utilisation ---
    const guideToggle = document.querySelector('.guide-accordion-toggle');
    const guideContent = document.querySelector('.guide-accordion-content');

    if (guideToggle && guideContent) {
        guideToggle.addEventListener('click', function() {
            const isOpen = guideContent.classList.contains('open');
            if (isOpen) {
                guideContent.classList.remove('open');
                guideContent.style.maxHeight = '0px';
                guideToggle.classList.remove('open');
            } else {
                guideContent.classList.add('open');
                guideContent.style.maxHeight = guideContent.scrollHeight + 'px';
                guideToggle.classList.add('open');
            }
        });
    }
});
