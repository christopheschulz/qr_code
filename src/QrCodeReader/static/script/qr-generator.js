/**
 * GESTION DU GÉNÉRATEUR DE QR CODE
 * Système complètement refait
 */

document.addEventListener("DOMContentLoaded", function () {
    console.log("🔄 Initialisation du générateur QR...");
    
    // Éléments DOM
    const buttons = document.querySelectorAll(".qr-option-btn");
    const formTypeInput = document.getElementById("form_type");
    const form = document.querySelector("form");
    
    console.log(`📋 Boutons trouvés: ${buttons.length}`);
    
    // Liste de tous les formulaires possibles
    const formIds = [
        'url-content', 'text-content', 'email-content', 'phone-content',
        'sms-content', 'wifi-content', 'vcard-content', 'location-content', 'event-content'
    ];
    
    // Fonction pour cacher tous les formulaires
    function hideAllForms() {
        formIds.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.classList.add('hidden');
            }
        });
        console.log("👁️ Tous les formulaires cachés");
    }
    
    // Fonction pour afficher un formulaire spécifique
    function showForm(targetId) {
        const element = document.getElementById(targetId);
        if (element) {
            element.classList.remove('hidden');
            console.log(`✅ Formulaire affiché: ${targetId}`);
            return true;
        }
        console.log(`❌ Formulaire non trouvé: ${targetId}`);
        return false;
    }
    
    // Fonction pour réinitialiser tous les boutons
    function resetAllButtons() {
        buttons.forEach(btn => {
            btn.classList.remove('active');
        });
    }
    
    // Fonction pour activer un bouton
    function activateButton(button) {
        button.classList.add('active');
        console.log(`🔵 Bouton activé: ${button.textContent.trim()}`);
    }
    
    // Gestion des clics sur les boutons
    buttons.forEach((button, index) => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            console.log(`🖱️ Clic sur bouton ${index + 1}: ${this.textContent.trim()}`);
            
            const targetId = this.getAttribute('data-target');
            if (!targetId) {
                console.log("❌ Pas de data-target sur ce bouton");
                return;
            }
            
            // 1. Cacher tous les formulaires
            hideAllForms();
            
            // 2. Réinitialiser tous les boutons
            resetAllButtons();
            
            // 3. Activer ce bouton
            activateButton(this);
            
            // 4. Afficher le bon formulaire
            const success = showForm(targetId);
            
            // 5. Mettre à jour le type de formulaire
            if (success && formTypeInput) {
                const formType = targetId.replace('-content', '');
                formTypeInput.value = formType;
                console.log(`📝 Type de formulaire: ${formType}`);
            }
        });
    });
    
    // Initialisation par défaut - URL
    console.log("🏁 Initialisation par défaut...");
    hideAllForms();
    
    const urlButton = document.querySelector('[data-target="url-content"]');
    if (urlButton) {
        activateButton(urlButton);
        showForm('url-content');
        if (formTypeInput) {
            formTypeInput.value = 'url';
        }
        console.log("✅ Initialisation terminée - URL par défaut");
    } else {
        console.log("❌ Bouton URL non trouvé pour l'initialisation");
    }
    
    // Configuration du téléchargement de QR code
    setupQrCodeDownload();
});

/**
 * Configuration du système de téléchargement du QR code
 */
function setupQrCodeDownload() {
    const downloadButton = document.getElementById('download-qr');
    const qrImage = document.getElementById('qr-code-image');
    const mobileHelpText = document.getElementById('mobile-download-help');

    if (downloadButton && qrImage) {
        // Détecter si c'est un appareil mobile
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        
        // Gérer l'affichage des éléments selon le type d'appareil
        if (isMobile) {
            downloadButton.style.display = 'none';
            if (mobileHelpText) {
                mobileHelpText.style.display = 'block';
            }
        } else {
            if (mobileHelpText) {
                mobileHelpText.style.display = 'none';
            }
            // Sur desktop, configurer le téléchargement
            downloadButton.addEventListener('click', function() {
                const link = document.createElement('a');
                link.href = qrImage.src;
                link.download = 'qr_code.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            });
        }
    }
}