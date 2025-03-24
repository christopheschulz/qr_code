document.addEventListener("DOMContentLoaded", function () {
   // ================= NAVIGATION PRINCIPALE =================
   const navLinks = document.querySelectorAll(".navbar .nav-link");

   function setActiveNavLink() {
       const currentPath = window.location.pathname;
       const currentPage = currentPath.split('/').filter(Boolean).pop(); // Récupère qrgenerator ou qrreader
   
       navLinks.forEach(link => {
           const linkPath = new URL(link.href, window.location.origin).pathname;
           const linkPage = linkPath.split('/').filter(Boolean).pop();
   
           link.classList.remove("bg-blue-500", "text-white", "hover:bg-blue-600");
           link.classList.add("text-black-600", "hover:underline");
   
           if (currentPage === linkPage) {
               link.classList.add("bg-blue-500", "text-white", "hover:bg-blue-600");
               link.classList.remove("text-black-600");
           }
   
           // Cas spécifique : racine
           if (!currentPage && link.href.endsWith('/')) {
               link.classList.add("bg-blue-500", "text-white", "hover:bg-blue-600");
               link.classList.remove("text-black-600");
           }
       });
   }
   
   setActiveNavLink();


    // ================= GESTION DU GENERATEUR QR =================
    const qrButtons = document.querySelectorAll(".qr-option-btn");
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

    const defaultButton = document.querySelector(".qr-option-btn[data-target='url-content']");
    if (defaultButton) {
        defaultButton.classList.remove("bg-blue-500", "hover:bg-blue-600");
        defaultButton.classList.add("bg-blue-800", "text-white");
        document.getElementById("url-content").classList.remove("hidden");
    }

    // ================= FORMULAIRE - GESTION DES CHAMPS =================
    const form = document.querySelector("form");
    if (form) {
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
    const fileInput = document.getElementById('id_qr_img');
    const fileName = document.getElementById('file-name');

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
