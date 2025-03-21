document.addEventListener("DOMContentLoaded", function() {
    // Gestion des liens de navigation
    const navLinks = document.querySelectorAll(".navbar a");

    function setActiveLink() {
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            if (link.href.includes(currentPath)) {
                link.classList.add("qr-option-btn", "bg-blue-500", "text-white", "py-2", "px-4", "rounded-lg", "hover:bg-blue-600");
            } else {
                link.classList.remove("qr-option-btn", "bg-blue-500", "text-white", "py-2", "px-4", "rounded-lg", "hover:bg-blue-600");
            }
        });
    }

    // Appliquer la classe active en fonction de l'URL actuelle
    setActiveLink();

    // Ajouter un gestionnaire d'événements pour les clics sur les liens de navigation
    navLinks.forEach(link => {
        link.addEventListener("click", function() {
            navLinks.forEach(l => l.classList.remove("qr-option-btn", "bg-blue-500", "text-white", "py-2", "px-4", "rounded-lg", "hover:bg-blue-600"));
            this.classList.add("qr-option-btn", "bg-blue-500", "text-white", "py-2", "px-4", "rounded-lg", "hover:bg-blue-600");

            // Stocker la sélection dans le localStorage
            localStorage.setItem("activeNav", this.getAttribute("href"));
        });
    });

    // Récupérer la sélection sauvegardée après un rechargement de page
    const savedActiveNav = localStorage.getItem("activeNav");
    if (savedActiveNav) {
        navLinks.forEach(link => {
            if (link.getAttribute("href") === savedActiveNav) {
                link.classList.add("qr-option-btn", "bg-blue-500", "text-white", "py-2", "px-4", "rounded-lg", "hover:bg-blue-600");
            }
        });
    }

    // Gestion des boutons d'options QR Code
    const buttons = document.querySelectorAll(".qr-option-btn");
    const contentDivs = document.querySelectorAll(".qr-content");
    const formTypeInput = document.getElementById("form_type");

    function toggleFormFields() {
        contentDivs.forEach(div => {
            const isHidden = div.classList.contains("hidden");
            const fields = div.querySelectorAll("input, select, textarea");

            fields.forEach(field => {
                if (isHidden) {
                    field.setAttribute("disabled", "disabled");
                } else {
                    field.removeAttribute("disabled");
                    if (field.hasAttribute("required")) {
                        field.dataset.wasRequired = "true";
                        field.removeAttribute("required");
                    }
                }
            });
        });
    }

    toggleFormFields();

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            buttons.forEach(btn => btn.classList.remove("bg-blue-800", "text-white"));
            contentDivs.forEach(div => div.classList.add("hidden"));

            this.classList.add("bg-blue-800", "text-white");
            const targetId = this.getAttribute("data-target");
            const targetDiv = document.getElementById(targetId);
            targetDiv.classList.remove("hidden");

            const formType = targetId.split('-')[0];
            formTypeInput.value = formType;
            console.log("Type de formulaire mis à jour:", formType);

            toggleFormFields();
        });
    });

    // Activer le bouton URL par défaut
    const defaultButton = document.querySelector(".qr-option-btn[data-target='url-content']");
    if (defaultButton) {
        defaultButton.classList.add("bg-blue-800", "text-white");
        document.getElementById("url-content").classList.remove("hidden");
    }

    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function(e) {
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

    // Gestion de l'affichage du nom du fichier uploadé
    const fileInput = document.getElementById('id_qr_img');
    const fileName = document.getElementById('file-name');

    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            fileName.textContent = this.files[0].name;
        } else {
            fileName.textContent = 'Aucun fichier sélectionné';
        }
    });
});
