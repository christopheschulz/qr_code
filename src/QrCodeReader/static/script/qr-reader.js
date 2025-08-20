/**
 * GESTION DU LECTEUR DE QR CODE
 * Gère l'upload et la validation des fichiers image, ainsi que la lecture via webcam
 */

class QRCodeReader {
    constructor() {
        this.video = null;
        this.canvas = null;
        this.context = null;
        this.stream = null;
        this.animationFrame = null;
        this.isScanning = false;
        
        this.initElements();
        this.initTabs();
        this.initFileUpload();
        this.initCamera();
    }

    initElements() {
        console.log('Initialisation des éléments...');
        
        // Éléments des onglets
        this.tabFile = document.getElementById('tab-file');
        this.tabCamera = document.getElementById('tab-camera');
        this.fileContent = document.getElementById('file-content');
        this.cameraContent = document.getElementById('camera-content');
        
        console.log('Éléments onglets:', {
            tabFile: !!this.tabFile,
            tabCamera: !!this.tabCamera,
            fileContent: !!this.fileContent,
            cameraContent: !!this.cameraContent
        });
        
        // Éléments de la caméra
        this.video = document.getElementById('camera-video');
        this.canvas = document.getElementById('camera-canvas');
        this.startCameraBtn = document.getElementById('start-camera');
        this.stopCameraBtn = document.getElementById('stop-camera');
        this.cameraContainer = document.getElementById('camera-container');
        this.cameraStatus = document.getElementById('camera-status');
        this.cameraError = document.getElementById('camera-error');
        
        console.log('Éléments caméra:', {
            video: !!this.video,
            canvas: !!this.canvas,
            startCameraBtn: !!this.startCameraBtn,
            stopCameraBtn: !!this.stopCameraBtn,
            cameraContainer: !!this.cameraContainer,
            cameraStatus: !!this.cameraStatus,
            cameraError: !!this.cameraError
        });
        
        // Éléments des résultats
        this.resultsSection = document.getElementById('results-section');
        this.decodedResult = document.getElementById('decoded-result');
        this.resultLink = document.getElementById('result-link');
        
        // Éléments du formulaire
        this.fileInput = document.getElementById('id_qr_img');
        this.fileName = document.getElementById('file-name');
        
        if (this.canvas) {
            this.context = this.canvas.getContext('2d');
        }
    }

    initTabs() {
        if (this.tabFile) {
            this.tabFile.addEventListener('click', () => this.switchTab('file'));
        }
        if (this.tabCamera) {
            this.tabCamera.addEventListener('click', () => this.switchTab('camera'));
        }
    }

    switchTab(tabName) {
        console.log('switchTab appelé avec:', tabName);
        
        // Mettre à jour les classes des onglets
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active', 'text-blue-600', 'border-blue-500');
            btn.classList.add('text-gray-500', 'border-transparent');
        });
        
        // Cacher tout le contenu
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.add('hidden');
        });
        
        // Activer l'onglet sélectionné
        if (tabName === 'file') {
            console.log('Activation onglet fichier');
            if (this.tabFile) {
                this.tabFile.classList.add('active', 'text-blue-600', 'border-blue-500');
                this.tabFile.classList.remove('text-gray-500', 'border-transparent');
            }
            if (this.fileContent) {
                this.fileContent.classList.remove('hidden');
            }
            this.stopCamera();
        } else if (tabName === 'camera') {
            console.log('Activation onglet camera');
            if (this.tabCamera) {
                this.tabCamera.classList.add('active', 'text-blue-600', 'border-blue-500');
                this.tabCamera.classList.remove('text-gray-500', 'border-transparent');
            }
            if (this.cameraContent) {
                this.cameraContent.classList.remove('hidden');
                console.log('Contenu camera affiché');
            } else {
                console.error('Élément cameraContent non trouvé');
            }
        }
    }

    initFileUpload() {
        if (this.fileInput) {
            this.fileInput.addEventListener('change', () => {
                if (this.fileInput.files.length > 0) {
                    const file = this.fileInput.files[0];
                    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
                    const maxSize = 4 * 1024 * 1024; // 4 Mo

                    // Validation du type de fichier
                    if (!validTypes.includes(file.type)) {
                        alert('Le fichier doit être une image (png, jpg, jpeg, webp)');
                        this.fileInput.value = '';
                        if (this.fileName) this.fileName.textContent = 'Aucun fichier sélectionné';
                        return;
                    }

                    // Validation de la taille du fichier
                    if (file.size > maxSize) {
                        alert('Le fichier est trop volumineux (max 4 Mo)');
                        this.fileInput.value = '';
                        if (this.fileName) this.fileName.textContent = 'Aucun fichier sélectionné';
                        return;
                    }

                    // Affichage du nom du fichier
                    if (this.fileName) {
                        this.fileName.textContent = file.name;
                    }
                } else {
                    if (this.fileName) {
                        this.fileName.textContent = 'Aucun fichier sélectionné';
                    }
                }
            });
        }
    }

    initCamera() {
        if (this.startCameraBtn) {
            this.startCameraBtn.addEventListener('click', () => this.startCamera());
        }
        if (this.stopCameraBtn) {
            this.stopCameraBtn.addEventListener('click', () => this.stopCamera());
        }
    }

    async startCamera() {
        try {
            this.hideError();
            this.updateStatus('Demande d\'accès à la caméra...');
            
            const constraints = {
                video: {
                    facingMode: 'environment', // Caméra arrière si disponible
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                }
            };

            this.stream = await navigator.mediaDevices.getUserMedia(constraints);
            this.video.srcObject = this.stream;
            
            await new Promise((resolve) => {
                this.video.onloadedmetadata = resolve;
            });

            this.cameraContainer.classList.remove('hidden');
            this.startCameraBtn.classList.add('hidden');
            this.stopCameraBtn.classList.remove('hidden');
            
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
            
            this.isScanning = true;
            this.updateStatus('Caméra active - Positionnez le QR code devant la caméra');
            this.scanQRCode();
            
        } catch (error) {
            console.error('Erreur lors de l\'accès à la caméra:', error);
            let errorMessage = 'Impossible d\'accéder à la caméra. ';
            
            if (error.name === 'NotAllowedError') {
                errorMessage += 'Veuillez autoriser l\'accès à la caméra dans votre navigateur.';
            } else if (error.name === 'NotFoundError') {
                errorMessage += 'Aucune caméra détectée sur cet appareil.';
            } else {
                errorMessage += 'Vérifiez que votre caméra est connectée et accessible.';
            }
            
            this.showError(errorMessage);
        }
    }

    stopCamera() {
        this.isScanning = false;
        
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        if (this.video) {
            this.video.srcObject = null;
        }
        
        this.cameraContainer.classList.add('hidden');
        this.startCameraBtn.classList.remove('hidden');
        this.stopCameraBtn.classList.add('hidden');
        this.hideError();
    }

    scanQRCode() {
        if (!this.isScanning || !this.video || !this.context) {
            return;
        }

        try {
            this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            const imageData = this.context.getImageData(0, 0, this.canvas.width, this.canvas.height);
            
            // Utiliser la bibliothèque jsQR pour décoder le QR code
            const code = jsQR(imageData.data, imageData.width, imageData.height);
            
            if (code) {
                this.handleQRCodeDetected(code.data);
                return;
            }
        } catch (error) {
            console.error('Erreur lors du scan:', error);
        }

        this.animationFrame = requestAnimationFrame(() => this.scanQRCode());
    }

    handleQRCodeDetected(data) {
        this.isScanning = false;
        this.updateStatus('QR Code détecté ! Arrêt de la caméra...');
        
        // Arrêter la caméra
        this.stopCamera();
        
        // Afficher le résultat
        this.displayResult(data);
        
        // Faire défiler vers les résultats
        if (this.resultsSection) {
            this.resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    displayResult(data) {
        if (this.resultsSection) {
            this.resultsSection.classList.remove('hidden');
            
            // Créer le HTML du résultat
            const isLink = data.startsWith('http');
            const resultHTML = `
                <div class="mt-6 p-4 bg-green-50 border border-green-200 rounded-xl">
                    <h3 class="text-lg font-semibold text-green-800 mb-3">
                        <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        Contenu décodé
                    </h3>
                    <div class="bg-white p-4 rounded-lg border">
                        <p class="text-gray-900 break-all">${this.escapeHtml(data)}</p>
                    </div>
                    ${isLink ? `
                        <a href="${this.escapeHtml(data)}" target="_blank" class="inline-flex items-center mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200">
                            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                            </svg>
                            Ouvrir le lien
                        </a>
                    ` : ''}
                </div>
            `;
            
            this.resultsSection.innerHTML = resultHTML;
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    updateStatus(message) {
        if (this.cameraStatus) {
            this.cameraStatus.textContent = message;
        }
    }

    showError(message) {
        if (this.cameraError) {
            this.cameraError.classList.remove('hidden');
            this.cameraError.querySelector('p').textContent = message;
        }
    }

    hideError() {
        if (this.cameraError) {
            this.cameraError.classList.add('hidden');
        }
    }
}

// Initialiser le lecteur QR quand le DOM est chargé
document.addEventListener("DOMContentLoaded", function () {
    console.log('DOM chargé, initialisation du QRCodeReader...');
    try {
        const reader = new QRCodeReader();
        console.log('QRCodeReader initialisé avec succès');
    } catch (error) {
        console.error('Erreur lors de l\'initialisation du QRCodeReader:', error);
    }
});