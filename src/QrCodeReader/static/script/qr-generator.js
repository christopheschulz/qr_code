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
    
    // Fonction pour cacher tous les formulaires et désactiver leurs champs
    function hideAllForms() {
        formIds.forEach(id => {
            const element = document.getElementById(id);
            if (element) {
                element.classList.add('hidden');
                // Désactiver tous les champs requis dans ce formulaire
                const requiredFields = element.querySelectorAll('input, textarea, select');
                requiredFields.forEach(field => {
                    field.removeAttribute('required');
                    field.disabled = true;
                });
            }
        });
        console.log("👁️ Tous les formulaires cachés");
    }
    
    // Fonction pour afficher un formulaire spécifique et activer ses champs
    function showForm(targetId) {
        const element = document.getElementById(targetId);
        if (element) {
            element.classList.remove('hidden');
            // Réactiver les champs requis dans ce formulaire
            const requiredFields = element.querySelectorAll('input, textarea, select');
            requiredFields.forEach(field => {
                field.disabled = false;
                // Ajouter l'attribut required seulement pour les champs principaux
                const fieldName = field.name;
                if (shouldBeRequired(fieldName, targetId)) {
                    field.setAttribute('required', 'required');
                }
            });
            console.log(`✅ Formulaire affiché: ${targetId}`);
            return true;
        }
        console.log(`❌ Formulaire non trouvé: ${targetId}`);
        return false;
    }
    
    // Fonction pour déterminer quels champs doivent être requis
    function shouldBeRequired(fieldName, formType) {
        const requiredFields = {
            'url-content': ['url_to_convert'],
            'text-content': ['text_to_convert'],
            'email-content': ['email'],
            'phone-content': ['phone'],
            'sms-content': ['phone', 'message'],
            'wifi-content': ['ssid', 'password'],
            'vcard-content': ['name'],
            'location-content': ['latitude', 'longitude'],
            'event-content': ['title', 'date']
        };
        
        const required = requiredFields[formType] || [];
        return required.includes(fieldName);
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
        console.log(`🔍 Classes du bouton:`, button.className);
        console.log(`🎨 Style background:`, getComputedStyle(button).backgroundColor);
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
    
    // Initialisation selon le type de formulaire actuel
    console.log("🏁 Initialisation...");
    hideAllForms();
    
    // Récupérer le type de formulaire actuel depuis le champ hidden
    const currentFormType = formTypeInput ? formTypeInput.value : 'url';
    const targetId = currentFormType + '-content';
    const activeButton = document.querySelector(`[data-target="${targetId}"]`);
    
    if (activeButton) {
        activateButton(activeButton);
        showForm(targetId);
        console.log(`✅ Initialisation terminée - ${currentFormType} actif`);
    } else {
        // Fallback sur URL si le bouton n'est pas trouvé
        const urlButton = document.querySelector('[data-target="url-content"]');
        if (urlButton) {
            activateButton(urlButton);
            showForm('url-content');
            if (formTypeInput) {
                formTypeInput.value = 'url';
            }
            console.log("✅ Fallback sur URL");
        }
    }
    
    // Gestion AJAX du formulaire pour éviter le rechargement de page
    if (form) {
        form.addEventListener('submit', handleFormSubmission);
    }
    
    // Configuration du compteur de caractères
    setupCharacterCounters();
    
    // Configuration de l'infobulle pour le taux de correction d'erreur
    
    // Mettre à jour les compteurs quand le niveau de correction change
    const errorCorrectionSelect = document.querySelector('select[name="qr_error_correction_form"]');
    if (errorCorrectionSelect) {
        errorCorrectionSelect.addEventListener('change', function() {
            // Reconfigurer tous les compteurs avec le nouveau niveau
            setupCharacterCounters();
        });
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
        // Configurer le téléchargement pour tous les appareils
        downloadButton.addEventListener('click', function() {
            downloadQrCodeWithDialog(qrImage);
        });
        
        // Masquer le texte d'aide mobile car nous utilisons maintenant une solution universelle
        if (mobileHelpText) {
            mobileHelpText.style.display = 'none';
        }
    }
}

/**
 * Télécharge le QR code en déclenchant la boîte de dialogue native du système
 */
async function downloadQrCodeWithDialog(qrImage) {
    try {
        // Obtenir l'URL de l'image
        const imageUrl = qrImage.getAttribute('data-download-url') || qrImage.src;
        
        // Créer un nom de fichier avec timestamp
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `qr_code_${timestamp}.png`;
        
        // Vérifier si le navigateur supporte l'API File System Access (Chrome/Edge moderne)
        if ('showSaveFilePicker' in window) {
            try {
                // Utiliser l'API moderne pour ouvrir le dialogue de sauvegarde natif
                const fileHandle = await window.showSaveFilePicker({
                    suggestedName: filename,
                    types: [{
                        description: 'Images PNG',
                        accept: { 'image/png': ['.png'] }
                    }]
                });
                
                // Récupérer les données de l'image
                const response = await fetch(imageUrl);
                const blob = await response.blob();
                
                // Écrire le fichier
                const writableStream = await fileHandle.createWritable();
                await writableStream.write(blob);
                await writableStream.close();
                
                console.log('✅ QR code sauvegardé avec succès');
                return;
            } catch (error) {
                // L'utilisateur a annulé ou erreur, utiliser la méthode de fallback
                if (error.name !== 'AbortError') {
                    console.warn('Erreur avec showSaveFilePicker:', error);
                }
            }
        }
        
        // Fallback standard pour tous les autres navigateurs
        const response = await fetch(imageUrl);
        const blob = await response.blob();
        
        // Créer un URL pour le blob
        const blobUrl = URL.createObjectURL(blob);
        
        // Créer un lien temporaire et le cliquer
        const link = document.createElement('a');
        link.href = blobUrl;
        link.download = filename;
        link.style.display = 'none';
        
        // Ajouter au DOM, cliquer, puis nettoyer
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Nettoyer l'URL du blob après un délai
        setTimeout(() => {
            URL.revokeObjectURL(blobUrl);
        }, 1000);
        
        console.log('✅ QR code téléchargé');
        
    } catch (error) {
        console.error('❌ Erreur lors du téléchargement:', error);
        // En dernier recours, ouvrir l'image dans un nouvel onglet
        window.open(qrImage.src, '_blank');
    }
}

/**
 * Gestion de la soumission AJAX du formulaire
 */
function handleFormSubmission(event) {
    event.preventDefault(); // Empêcher la soumission normale
    
    const form = event.target;
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Indication visuelle de chargement
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Génération en cours...';
    submitButton.disabled = true;
    
    console.log('📤 Envoi AJAX du formulaire...');
    
    fetch(form.action || window.location.pathname, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('✅ Réponse AJAX reçue:', data);
        
        if (data.success) {
            // Mettre à jour l'aperçu avec le QR code
            updatePreview(data.image_url, data.download_url);
        } else {
            // Afficher les erreurs
            displayErrors(data.errors);
        }
    })
    .catch(error => {
        console.error('❌ Erreur AJAX:', error);
        // En cas d'erreur, faire une soumission normale
        form.submit();
    })
    .finally(() => {
        // Restaurer le bouton
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    });
}

/**
 * Met à jour l'aperçu avec le nouveau QR code
 */
function updatePreview(imageUrl, downloadUrl) {
    const previewContainer = document.querySelector('.bg-white.rounded-2xl.shadow-lg.border.border-gray-100:last-child');
    const previewContent = previewContainer.querySelector('.p-6.text-center');
    
    if (imageUrl) {
        previewContent.innerHTML = `
            <div class="bg-gray-50 rounded-xl p-6 mb-6">
                <img src="${imageUrl}" alt="QR Code généré" class="mx-auto w-64 h-64 object-contain" id="qr-code-image" data-download-url="${downloadUrl || imageUrl}">
            </div>
            <button id="download-qr" class="w-full bg-gray-900 text-white py-3 px-6 rounded-xl font-medium hover:bg-gray-800 transition-colors duration-200">
                Télécharger
            </button>
        `;
        
        // Réinitialiser le système de téléchargement
        setupQrCodeDownload();
    }
}

/**
 * Affiche les erreurs de validation
 */
function displayErrors(errors) {
    console.log('Affichage des erreurs:', errors);
    // TODO: Implémenter l'affichage des erreurs
}

/**
 * Configuration des compteurs de caractères pour les champs de texte
 */
function setupCharacterCounters() {
    // Capacités par niveau de correction d'erreur (texte byte)
    const capacities = {
        0: 2953, // L (7%)
        1: 2331, // M (15%) - défaut
        2: 1663, // Q (25%)
        3: 1273  // H (30%)
    };
    
    // Sélectionner tous les champs de texte et textarea
    const textInputs = document.querySelectorAll('input[type="text"], input[type="url"], input[type="email"], textarea');
    
    textInputs.forEach(input => {
        // Ajouter un événement pour compter les caractères
        input.addEventListener('input', function() {
            updateCharacterCount(this);
        });
        
        // Initialiser le compteur
        updateCharacterCount(input);
    });
    
    function updateCharacterCount(input) {
        const currentLength = input.value.length;
        const errorCorrectionSelect = document.querySelector('select[name="qr_error_correction_form"]');
        const errorLevel = errorCorrectionSelect ? parseInt(errorCorrectionSelect.value) : 1;
        const maxCapacity = capacities[errorLevel] || capacities[1];
        
        // Créer ou mettre à jour le compteur
        let counter = input.parentNode.querySelector('.character-counter');
        if (!counter) {
            counter = document.createElement('div');
            counter.className = 'character-counter text-xs mt-1 text-right';
            input.parentNode.appendChild(counter);
        }
        
        // Déterminer la couleur selon le pourcentage utilisé
        const percentage = (currentLength / maxCapacity) * 100;
        let colorClass = 'text-gray-500';
        if (percentage > 90) {
            colorClass = 'text-red-600 font-medium';
        } else if (percentage > 75) {
            colorClass = 'text-orange-600';
        } else if (percentage > 50) {
            colorClass = 'text-yellow-600';
        }
        
        counter.className = `character-counter text-xs mt-1 text-right ${colorClass}`;
        counter.textContent = `${currentLength} / ${maxCapacity} caractères`;
    }
}

