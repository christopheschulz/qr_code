/**
 * GESTION DU LECTEUR DE QR CODE
 * Gère les onglets fichier/webcam, le scan QR via webcam (jsQR),
 * la génération d'un QR code propre du contenu scanné,
 * le téléchargement et la copie dans le presse-papier.
 */

document.addEventListener("DOMContentLoaded", function () {

    // === Éléments DOM ===
    const tabFile = document.getElementById('tab-file');
    const tabCamera = document.getElementById('tab-camera');
    const fileContent = document.getElementById('file-content');
    const cameraContent = document.getElementById('camera-content');

    const startCameraBtn = document.getElementById('start-camera');
    const stopCameraBtn = document.getElementById('stop-camera');
    const video = document.getElementById('camera-video');
    const canvas = document.getElementById('camera-canvas');
    const cameraContainer = document.getElementById('camera-container');
    const cameraStatus = document.getElementById('camera-status');
    const cameraError = document.getElementById('camera-error');
    const resultsSection = document.getElementById('results-section');

    let stream = null;
    let isScanning = false;
    let animationFrame = null;

    // === Gestion des onglets ===

    function restoreActiveTab() {
        const savedTab = localStorage.getItem('qr-reader-active-tab');
        if (savedTab && (savedTab === 'file' || savedTab === 'camera')) {
            switchTab(savedTab);
        } else {
            switchTab('file');
        }
    }

    function switchTab(tabName) {
        localStorage.setItem('qr-reader-active-tab', tabName);

        // Réinitialiser tous les onglets
        document.querySelectorAll('.tab-button').forEach(function (btn) {
            btn.classList.remove('active', 'text-blue-600', 'border-blue-500');
            btn.classList.add('text-gray-500', 'border-transparent');
            btn.setAttribute('aria-selected', 'false');
        });

        // Cacher tout le contenu des onglets
        document.querySelectorAll('.tab-content').forEach(function (content) {
            content.classList.add('hidden');
            content.style.display = 'none';
        });

        if (tabName === 'file') {
            tabFile.classList.add('active', 'text-blue-600', 'border-blue-500');
            tabFile.classList.remove('text-gray-500', 'border-transparent');
            tabFile.setAttribute('aria-selected', 'true');
            fileContent.classList.remove('hidden');
            fileContent.style.display = 'block';
            resetPreviewCard();
        } else if (tabName === 'camera') {
            tabCamera.classList.add('active', 'text-blue-600', 'border-blue-500');
            tabCamera.classList.remove('text-gray-500', 'border-transparent');
            tabCamera.setAttribute('aria-selected', 'true');
            cameraContent.classList.remove('hidden');
            cameraContent.style.display = 'block';
            resetPreviewCard();
        }
    }

    function resetPreviewCard() {
        var previewTitle = document.getElementById('preview-title');
        var previewContent = previewTitle ? previewTitle.parentElement.nextElementSibling : null;

        if (previewTitle) {
            previewTitle.textContent = 'Image téléchargée';
        }

        if (previewContent) {
            previewContent.innerHTML =
                '<div class="bg-gray-50 rounded-xl p-12">' +
                    '<div class="w-32 h-32 bg-gray-200 rounded-lg mx-auto mb-4 flex items-center justify-center">' +
                        '<svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
                            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>' +
                        '</svg>' +
                    '</div>' +
                    '<p class="text-gray-500">Votre image QR code apparaîtra ici</p>' +
                '</div>';
        }

        if (resultsSection) {
            resultsSection.classList.add('hidden');
            resultsSection.innerHTML = '';
        }
    }

    if (tabFile) {
        tabFile.addEventListener('click', function (e) {
            e.preventDefault();
            switchTab('file');
        });
    }

    if (tabCamera) {
        tabCamera.addEventListener('click', function (e) {
            e.preventDefault();
            switchTab('camera');
        });
    }

    restoreActiveTab();

    // === Gestion de la caméra ===

    function updateStatus(message) {
        if (cameraStatus) {
            cameraStatus.textContent = message;
        }
    }

    function showError(message) {
        if (cameraError) {
            cameraError.classList.remove('hidden');
            cameraError.querySelector('p').textContent = message;
        }
    }

    function hideError() {
        if (cameraError) {
            cameraError.classList.add('hidden');
        }
    }

    function stopCamera() {
        isScanning = false;

        if (animationFrame) {
            cancelAnimationFrame(animationFrame);
            animationFrame = null;
        }

        if (stream) {
            stream.getTracks().forEach(function (track) { track.stop(); });
            stream = null;
        }

        if (video) {
            video.srcObject = null;
        }

        if (cameraContainer) cameraContainer.classList.add('hidden');
        if (startCameraBtn) startCameraBtn.classList.remove('hidden');
        if (stopCameraBtn) stopCameraBtn.classList.add('hidden');
        hideError();
    }

    function scanQRCode() {
        if (!isScanning || !video || !canvas) {
            return;
        }

        var context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        if (canvas.width > 0 && canvas.height > 0) {
            try {
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                var imageData = context.getImageData(0, 0, canvas.width, canvas.height);

                if (typeof jsQR !== 'undefined') {
                    var code = jsQR(imageData.data, imageData.width, imageData.height);
                    if (code) {
                        handleQRCodeDetected(code.data);
                        return;
                    }
                }
            } catch (error) {
                console.error('Erreur lors du scan:', error);
            }
        }

        animationFrame = requestAnimationFrame(scanQRCode);
    }

    function handleQRCodeDetected(data) {
        isScanning = false;
        updateStatus('QR Code détecté ! Arrêt de la caméra...');
        stopCamera();
        generateQRCodeFromData(data);
        displayResult(data);
    }

    // === Génération de QR code du contenu scanné ===

    function generateQRCodeFromData(data) {
        try {
            var qrCanvas = document.createElement('canvas');
            var qrContext = qrCanvas.getContext('2d');
            var qrSize = 300;
            qrCanvas.width = qrSize;
            qrCanvas.height = qrSize;

            var qrCodeUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=' + qrSize + 'x' + qrSize + '&data=' + encodeURIComponent(data) + '&format=PNG&margin=10';

            var qrImage = new Image();
            qrImage.crossOrigin = 'anonymous';

            qrImage.onload = function () {
                qrContext.drawImage(qrImage, 0, 0, qrSize, qrSize);
                var qrDataUrl = qrCanvas.toDataURL('image/png');
                displayGeneratedQRCode(qrDataUrl, data);
            };

            qrImage.onerror = function () {
                generateSimpleQRCode(data);
            };

            qrImage.src = qrCodeUrl;
        } catch (error) {
            console.error('Erreur lors de la génération du QR code:', error);
            generateSimpleQRCode(data);
        }
    }

    function generateSimpleQRCode(data) {
        var cvs = document.createElement('canvas');
        var ctx = cvs.getContext('2d');
        var size = 300;
        cvs.width = size;
        cvs.height = size;

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, size, size);
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2;
        ctx.strokeRect(10, 10, size - 20, size - 20);

        ctx.fillStyle = '#000000';
        ctx.font = '16px monospace';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        var maxCharsPerLine = 25;
        var lines = [];
        for (var i = 0; i < data.length; i += maxCharsPerLine) {
            lines.push(data.substring(i, i + maxCharsPerLine));
        }

        var lineHeight = 20;
        var startY = (size / 2) - ((lines.length - 1) * lineHeight / 2);
        lines.forEach(function (line, index) {
            ctx.fillText(line, size / 2, startY + (index * lineHeight));
        });

        var qrDataUrl = cvs.toDataURL('image/png');
        displayGeneratedQRCode(qrDataUrl, data);
    }

    function displayGeneratedQRCode(qrDataUrl, originalData) {
        if (!qrDataUrl) return;

        var previewTitle = document.getElementById('preview-title');
        if (previewTitle) {
            previewTitle.innerHTML =
                '<div class="flex items-center">' +
                    '<svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11a9 9 0 11-18 0 9 9 0 0118 0z"></path>' +
                        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v4l3 2"></path>' +
                    '</svg>' +
                    'QR Code généré' +
                '</div>';
        }

        var previewContent = previewTitle ? previewTitle.parentElement.nextElementSibling : null;
        if (!previewContent) return;

        // Build DOM elements instead of innerHTML with user data
        var wrapper = document.createElement('div');
        wrapper.className = 'bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200';

        var badge = document.createElement('div');
        badge.className = 'mb-4';
        badge.innerHTML =
            '<div class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-blue-100 text-blue-800 shadow-sm">' +
                '<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11a9 9 0 11-18 0 9 9 0 0118 0z"></path>' +
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v4l3 2"></path>' +
                '</svg>' +
                'QR Code régénéré' +
            '</div>';

        var imgContainer = document.createElement('div');
        imgContainer.className = 'bg-white p-4 rounded-xl shadow-sm border border-blue-100';
        var img = document.createElement('img');
        img.src = qrDataUrl;
        img.alt = 'QR Code généré du contenu scanné';
        img.className = 'mx-auto max-w-full h-auto rounded-lg shadow-lg border-2 border-blue-200 animate-fade-in';
        img.style.maxHeight = '400px';
        imgContainer.appendChild(img);

        var info = document.createElement('div');
        info.className = 'mt-4 space-y-2';

        var infoText = document.createElement('p');
        infoText.className = 'text-sm font-medium text-blue-800';
        infoText.textContent = 'QR Code propre généré du contenu scanné';
        info.appendChild(infoText);

        var infoSubtext = document.createElement('p');
        infoSubtext.className = 'text-xs text-gray-600';
        infoSubtext.textContent = 'QR Code optimisé et téléchargeable';
        info.appendChild(infoSubtext);

        var buttons = document.createElement('div');
        buttons.className = 'flex flex-wrap gap-3';

        var dlBtn = document.createElement('button');
        dlBtn.className = 'inline-flex items-center px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700 transition-colors duration-200';
        dlBtn.innerHTML =
            '<svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
                '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>' +
            '</svg>' +
            'Télécharger QR';
        dlBtn.addEventListener('click', function () {
            downloadImage(qrDataUrl, 'qr-code-generated.png');
        });
        buttons.appendChild(dlBtn);

        var cpBtn = document.createElement('button');
        cpBtn.className = 'inline-flex items-center px-3 py-1.5 bg-gray-600 text-white text-xs font-medium rounded-lg hover:bg-gray-700 transition-colors duration-200';
        cpBtn.innerHTML =
            '<svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
                '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>' +
            '</svg>' +
            'Copier contenu';
        cpBtn.addEventListener('click', function () {
            copyToClipboard(originalData);
        });
        buttons.appendChild(cpBtn);

        info.appendChild(buttons);
        wrapper.appendChild(badge);
        wrapper.appendChild(imgContainer);
        wrapper.appendChild(info);

        previewContent.innerHTML = '';
        previewContent.appendChild(wrapper);
    }

    // === Fonctions utilitaires ===

    function downloadImage(dataUrl, filename) {
        var link = document.createElement('a');
        link.download = filename;
        link.href = dataUrl;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    function copyToClipboard(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function () {
                showCopySuccess();
            }).catch(function () {
                fallbackCopyToClipboard(text);
            });
        } else {
            fallbackCopyToClipboard(text);
        }
    }

    function fallbackCopyToClipboard(text) {
        var textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-9999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            if (document.execCommand('copy')) {
                showCopySuccess();
            }
        } catch (err) {
            console.error('Erreur fallback copie:', err);
        }
        document.body.removeChild(textArea);
    }

    function showCopySuccess() {
        var notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 animate-fade-in';
        notification.innerHTML =
            '<div class="flex items-center">' +
                '<svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>' +
                '</svg>' +
                'Texte copié !' +
            '</div>';
        document.body.appendChild(notification);
        setTimeout(function () {
            notification.remove();
        }, 2000);
    }

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function displayResult(data) {
        if (!resultsSection) return;

        resultsSection.classList.remove('hidden');

        var isLink = data.startsWith('https://') || data.startsWith('http://');

        // Build DOM elements (avoid innerHTML with user data)
        var resultContainer = document.createElement('div');
        resultContainer.className = 'mt-6 p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl shadow-lg';

        // Header
        var header = document.createElement('div');
        header.className = 'flex items-center mb-4';
        header.innerHTML =
            '<div class="flex-shrink-0 w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">' +
                '<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>' +
                '</svg>' +
            '</div>' +
            '<div class="ml-4">' +
                '<h3 class="text-xl font-bold text-green-800">QR Code scanné avec succès !</h3>' +
                '<p class="text-sm text-green-600">Contenu décodé via webcam</p>' +
            '</div>';

        // Content (safe: textContent)
        var content = document.createElement('div');
        content.className = 'bg-white p-6 rounded-xl border border-green-100 shadow-sm';
        var contentText = document.createElement('p');
        contentText.className = 'text-gray-900 break-all font-medium text-lg leading-relaxed';
        contentText.textContent = data;
        content.appendChild(contentText);

        // Action buttons
        var buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'mt-4 flex flex-wrap gap-4';

        if (isLink) {
            var linkButton = document.createElement('a');
            linkButton.href = data;
            linkButton.target = '_blank';
            linkButton.rel = 'noopener noreferrer';
            linkButton.className = 'result-button-link';
            linkButton.innerHTML =
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor">' +
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>' +
                '</svg>' +
                'Ouvrir le lien';
            buttonsContainer.appendChild(linkButton);
        }

        var copyButton = document.createElement('button');
        copyButton.className = 'result-button-copy';
        copyButton.innerHTML =
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor">' +
                '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path>' +
            '</svg>' +
            'Copier le texte';
        copyButton.addEventListener('click', function () {
            copyToClipboard(data);
        });
        buttonsContainer.appendChild(copyButton);

        resultContainer.appendChild(header);
        resultContainer.appendChild(content);
        resultContainer.appendChild(buttonsContainer);

        resultsSection.innerHTML = '';
        resultsSection.appendChild(resultContainer);
    }

    // === Événements caméra ===

    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', async function () {
            try {
                hideError();
                updateStatus('Demande d\'accès à la caméra...');

                var constraints = {
                    video: {
                        facingMode: 'environment',
                        width: { ideal: 640 },
                        height: { ideal: 480 }
                    }
                };

                stream = await navigator.mediaDevices.getUserMedia(constraints);
                video.srcObject = stream;

                await new Promise(function (resolve) {
                    video.onloadedmetadata = resolve;
                });

                cameraContainer.classList.remove('hidden');
                startCameraBtn.classList.add('hidden');
                stopCameraBtn.classList.remove('hidden');

                isScanning = true;
                updateStatus('Caméra active - Positionnez le QR code devant la caméra');
                scanQRCode();
            } catch (error) {
                console.error('Erreur caméra:', error);
                var errorMessage = 'Impossible d\'accéder à la caméra. ';

                if (error.name === 'NotAllowedError') {
                    errorMessage += 'Veuillez autoriser l\'accès à la caméra dans votre navigateur.';
                } else if (error.name === 'NotFoundError') {
                    errorMessage += 'Aucune caméra détectée sur cet appareil.';
                } else {
                    errorMessage += 'Vérifiez que votre caméra est connectée et accessible.';
                }

                showError(errorMessage);
            }
        });
    }

    if (stopCameraBtn) {
        stopCameraBtn.addEventListener('click', stopCamera);
    }

    // === Afficher les résultats si pré-remplis (upload fichier) ===
    if (resultsSection) {
        var hasResult = resultsSection.querySelector('.bg-green-50');
        if (hasResult) {
            resultsSection.classList.remove('hidden');
        }
    }
});
