/**
 * GESTION DU LECTEUR DE QR CODE
 * Gère l'upload et la validation des fichiers image
 */

document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById('id_qr_img');
    const fileName = document.getElementById('file-name');

    if (fileInput) {
        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                const file = this.files[0];
                const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
                const maxSize = 2 * 1024 * 1024; // 2 Mo

                // Validation du type de fichier
                if (!validTypes.includes(file.type)) {
                    alert('Le fichier doit être une image (png, jpg, jpeg, webp)');
                    this.value = '';
                    if (fileName) fileName.textContent = 'Aucun fichier sélectionné';
                    return;
                }

                // Validation de la taille du fichier
                if (file.size > maxSize) {
                    alert('Le fichier est trop volumineux (max 2 Mo)');
                    this.value = '';
                    if (fileName) fileName.textContent = 'Aucun fichier sélectionné';
                    return;
                }

                // Affichage du nom du fichier
                if (fileName) {
                    fileName.textContent = file.name;
                }
            } else {
                if (fileName) {
                    fileName.textContent = 'Aucun fichier sélectionné';
                }
            }
        });
    }
});