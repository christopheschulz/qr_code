document.addEventListener("DOMContentLoaded", function() {

    // ================= NAVIGATION PRINCIPALE =================
    const navLinks = document.querySelectorAll(".navbar .nav-link");

    // Met la nav active selon l'URL
    function setActiveNavLink() {
        const currentPath = window.location.pathname;
        navLinks.forEach(link => {
            if (link.href.includes(currentPath)) {
                link.classList.add("bg-blue-500", "text-white", "hover:bg-blue-600");
                link.classList.remove("text-black-600");
            } else {
                link.classList.remove("bg-blue-500", "text-white", "hover:bg-blue-600");
                link.classList.add("text-black-600");
            }
        });
    }
    setActiveNavLink();

    // Clic sur la nav : applique la classe active et sauvegarde
    navLinks.forEach(link => {
        link.addEventListener("click", function() {
            navLinks.forEach(l => {
                l.classList.remove("bg-blue-500", "text-white", "hover:bg-blue-600");
                l.classList.add("text-black-600");
            });
            this.classList.add("bg-blue-500", "text-white", "hover:bg-blue-600");
            this.classList.remove("text-black-600");
            localStorage.setItem("activeNav", this.getAttribute("href"));
        });
    });

    // Récupère la nav active depuis le localStorage
    const savedActiveNav = localStorage.getItem("activeNav");
    if (savedActiveNav) {
        navLinks.forEach(link => {
            if (link.getAttribute("href") === savedActiveNav) {
                link.classList.add("bg-blue-500", "text-white", "hover:bg-blue-600");
                link.classList.remove("text-black-600");
            }
        });
    }

    // ================= GESTION DU GENERATEUR QR =================
    const qrButtons = document.querySelectorAll(".qr-option-btn");
    const contentDivs = document.querySelectorAll(".qr-content");
    const formTypeInput = document.getElementById("form_type");

    // Fonction pour activer/désactiver les champs en fonction du bloc visible
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

    // Clic sur une option QR : change la couleur et le formulaire actif
    qrButtons.forEach(button => {
        button.addEventListener("click", function() {
            // Reset toutes les options
            qrButtons.forEach(btn => {
                btn.classList.remove("bg-blue-800", "text-white");
                btn.classList.add("bg-blue-500", "text-white", "hover:bg-blue-600");
            });

            // Active l'option cliquée
            this.classList.remove("bg-blue-500", "hover:bg-blue-600");
            this.classList.add("bg-blue-800", "text-white");

            // Affiche le bon formulaire
            contentDivs.forEach(div => div.classList.add("hidden"));
            const targetId = this.getAttribute("data-target");
            const targetDiv = document.getElementById(targetId);
            targetDiv.classList.remove("hidden");

            // Met à jour le champ caché du type de formulaire
            const formType = targetId.split('-')[0];
            formTypeInput.value = formType;
            console.log("Type de formulaire mis à jour:", formType);

            // Met à jour les champs
            toggleFormFields();
        });
    });

    // Active l'option URL par défaut au chargement
    const defaultButton = document.querySelector(".qr-option-btn[data-target='url-content']");
    if (defaultButton) {
        defaultButton.classList.remove("bg-blue-500", "hover:bg-blue-600");
        defaultButton.classList.add("bg-blue-800", "text-white");
        document.getElementById("url-content").classList.remove("hidden");
    }

    // ================= FORMULAIRE QR =================
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function(e) {
            // Avant la soumission, réactive les champs du bloc actif
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
    const fileInput = document.getElementById('id_qr_img');
    const fileName = document.getElementById('file-name');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileName.textContent = this.files[0].name;
            } else {
                fileName.textContent = 'Aucun fichier sélectionné';
            }
        });
    }
});
