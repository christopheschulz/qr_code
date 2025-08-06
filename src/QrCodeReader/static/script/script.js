/**
 * SCRIPTS COMMUNS À TOUTE L'APPLICATION QR CODE
 * Fonctions utilitaires et initialisations globales
 */

document.addEventListener("DOMContentLoaded", function () {
    // Initialisation globale de l'application
    console.log("Application QR Code - Scripts chargés");
    
    // Fonctions utilitaires globales disponibles
    window.QRCodeApp = {
        // Fonction utilitaire pour formater les dates
        formatDate: function(date) {
            return date.toLocaleDateString('fr-FR');
        },
        
        // Fonction utilitaire pour valider les URLs
        isValidUrl: function(string) {
            try {
                new URL(string);
                return true;
            } catch (_) {
                return false;
            }
        }
    };
});
