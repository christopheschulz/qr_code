document.addEventListener("DOMContentLoaded", function() {
// Gestion des liens de navigation
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
    link.addEventListener("click", function() {
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

// Gestion des boutons d'options QR Code
const buttons = document.querySelectorAll(".qr-option-btn");
const contentDivs = document.querySelectorAll(".qr-content");
const formTypeInput = document.getElementById("form_type");

// Fonction pour gérer l'état des champs dans les formulaires
function toggleFormFields() {
    contentDivs.forEach(div => {
        const isHidden = div.classList.contains("hidden");
        const fields = div.querySelectorAll("input, select, textarea");
        
        fields.forEach(field => {
            if (isHidden) {
                // Désactiver les champs dans les formulaires cachés
                field.setAttribute("disabled", "disabled");
            } else {
                // Activer les champs dans le formulaire visible
                field.removeAttribute("disabled");
                
                // Supprimer l'attribut required pour éviter la validation HTML5
                if (field.hasAttribute("required")) {
                    field.dataset.wasRequired = "true";
                    field.removeAttribute("required");
                }
            }
        });
    });
}

// Appliquer la configuration initiale
toggleFormFields();

// Gestionnaire d'événements pour les boutons d'options
buttons.forEach(button => {
    button.addEventListener("click", function() {
        // Retirer la classe active de tous les boutons
        buttons.forEach(btn => btn.classList.remove("bg-blue-800"));
        
        // Masquer tous les contenus de formulaire
        contentDivs.forEach(div => div.classList.add("hidden"));
        
        // Ajouter la classe active au bouton cliqué
        this.classList.add("bg-blue-800", "text-white");
        
        // Afficher le contenu correspondant
        const targetId = this.getAttribute("data-target");
        const targetDiv = document.getElementById(targetId);
        targetDiv.classList.remove("hidden");
        
        // Mettre à jour le champ hidden avec le type de formulaire
        const formType = targetId.split('-')[0];
        formTypeInput.value = formType;
        console.log("Type de formulaire mis à jour:", formType);
        
        // Mettre à jour l'état des champs de formulaire
        toggleFormFields();
    });
});

// Activer le bouton URL par défaut
const defaultButton = document.querySelector(".qr-option-btn[data-target='url-content']");
if (defaultButton) {
    defaultButton.classList.add("bg-blue-800", "text-white");
    document.getElementById("url-content").classList.remove("hidden");
}

// Gérer la soumission du formulaire
const form = document.querySelector("form");
if (form) {
    form.addEventListener("submit", function(e) {
        // Réactiver temporairement tous les champs du formulaire actif pour la soumission
        const activeDiv = document.querySelector(".qr-content:not(.hidden)");
        if (activeDiv) {
            const fields = activeDiv.querySelectorAll("input, select, textarea");
            fields.forEach(field => {
                field.removeAttribute("disabled");
                if (field.dataset.wasRequired === "true") {
                    field.setAttribute("required", "required");
                }
            });
        }
            
        console.log("Formulaire soumis:", formTypeInput.value);
        });
    }
});
const fileInput = document.getElementById('id_qr_img');
    const fileName = document.getElementById('file-name');

    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = 'Aucun fichier sélectionné';
        }
    });
