document.addEventListener("DOMContentLoaded", function () {

    // ================= NAVIGATION PRINCIPALE =================
    const navLinks = document.querySelectorAll(".navbar .nav-link");
    const currentPath = window.location.pathname;

    // Fonction pour nettoyer et normaliser un chemin
    function normalizePath(path) {
        // Supprimer les slashes au début et à la fin
        path = path.replace(/^\/+|\/+$/g, '');
        // Supprimer les paramètres de requête s'il y en a
        path = path.split('?')[0];
        return path;
    }

    // Fonction pour vérifier si un lien est actif
    function isLinkActive(linkPath, currentPath) {
        const normalizedLinkPath = normalizePath(linkPath);
        const normalizedCurrentPath = normalizePath(currentPath);

        // Cas spécial pour la page d'accueil
        if (normalizedLinkPath === '' && (normalizedCurrentPath === '' || normalizedCurrentPath === 'index')) {
            return true;
        }

        // Pour les autres pages
        return normalizedCurrentPath === normalizedLinkPath;
    }

    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        
        if (isLinkActive(linkPath, currentPath)) {
            link.classList.add("bg-blue-500", "text-white", "hover:bg-blue-600");
            link.classList.remove("text-black-600", "hover:underline");
        } else {
            link.classList.remove("bg-blue-500", "text-white", "hover:bg-blue-600");
            link.classList.add("text-black-600", "hover:underline");
        }
    });

    // ================= GESTION DU GENERATEUR QR =================
    const qrButtons = document.querySelectorAll(".qr-option-btn");
    const contentDivs = document.querySelectorAll(".qr-content");
    const formTypeInput = document.getElementById("form_type");

    // Fonction pour télécharger le QR code
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

    // Appeler la fonction de téléchargement
    setupQrCodeDownload();

    function toggleFormFields() {
        contentDivs.forEach(div => {
            const isHidden = div.classList.contains("hidden");
            const fields = div.querySelectorAll("input, select, textarea");
            fields.forEach(field => {
                if (isHidden) {
                    if (field.hasAttribute("required")) {
                        field.dataset.wasRequired = "true";
                        field.removeAttribute("required");
                    }
                    field.setAttribute("disabled", "disabled");
                } else {
                    field.removeAttribute("disabled");
                    if (field.dataset.wasRequired === "true") {
                        field.setAttribute("required", "required");
                    }
                }
            });
        });
    }

    toggleFormFields();

    qrButtons.forEach(button => {
        button.addEventListener("click", function () {
            qrButtons.forEach(btn => {
                btn.classList.remove("bg-blue-800", "text-white");
                btn.classList.add("bg-blue-500", "text-white", "hover:bg-blue-600");
            });

            this.classList.remove("bg-blue-500", "hover:bg-blue-600");
            this.classList.add("bg-blue-800", "text-white");

            contentDivs.forEach(div => div.classList.add("hidden"));
            const targetId = this.getAttribute("data-target");
            const targetDiv = document.getElementById(targetId);
            targetDiv.classList.remove("hidden");

            const formType = targetId.split('-')[0];
            formTypeInput.value = formType;
            console.log("Type de formulaire mis à jour:", formType);

            toggleFormFields();
        });
    });

    // Active l'option URL par défaut
    const defaultButton = document.querySelector(".qr-option-btn[data-target='url-content']");
    if (defaultButton) {
        defaultButton.click();
    }

    // ================= FORMULAIRE - GESTION DES CHAMPS =================
    const form = document.querySelector("form");
    const fileInput = document.getElementById('id_qr_img');
    const fileName = document.getElementById('file-name');

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                const file = this.files[0];
                const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
                const maxSize = 2 * 1024 * 1024; // 2 Mo

                if (!validTypes.includes(file.type)) {
                    alert('Le fichier doit être une image (png, jpg, jpeg, webp)');
                    this.value = '';
                    fileName.textContent = 'Aucun fichier sélectionné';
                    return;
                }

                if (file.size > maxSize) {
                    alert('Le fichier est trop volumineux (max 2 Mo)');
                    this.value = '';
                    fileName.textContent = 'Aucun fichier sélectionné';
                    return;
                }

                fileName.textContent = file.name;
            } else {
                fileName.textContent = 'Aucun fichier sélectionné';
            }
        });
    }

    if (form) {
        form.addEventListener("submit", function (e) {
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

    // ================= UPLOAD - NOM DU FICHIER =================
    if (fileInput) {
        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                fileName.textContent = this.files[0].name;
            } else {
                fileName.textContent = 'Aucun fichier sélectionné';
            }
        });
    }

});
