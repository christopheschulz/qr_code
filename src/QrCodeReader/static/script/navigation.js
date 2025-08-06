/**
 * GESTION DE LA NAVIGATION PRINCIPALE
 * Gère l'état actif des liens de navigation
 */

document.addEventListener("DOMContentLoaded", function () {
    console.log("🔍 Navigation script chargé");
    
    const navLinks = document.querySelectorAll("nav .nav-link");
    const currentPath = window.location.pathname;
    
    console.log("📍 Chemin actuel:", currentPath);
    console.log("🔗 Liens trouvés:", navLinks.length);

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

        console.log("🔍 Comparaison:", normalizedLinkPath, "vs", normalizedCurrentPath);

        // Cas spécial pour la page d'accueil
        if (normalizedLinkPath === '' && (normalizedCurrentPath === '' || normalizedCurrentPath === 'index')) {
            return true;
        }

        // Pour les autres pages
        return normalizedCurrentPath === normalizedLinkPath;
    }

    navLinks.forEach((link, index) => {
        const linkPath = new URL(link.href).pathname;
        const isActive = isLinkActive(linkPath, currentPath);
        
        console.log(`🔗 Lien ${index + 1}: ${link.textContent.trim()} - ${linkPath} - Actif: ${isActive}`);
        
        if (isActive) {
            // Ajouter les classes pour l'état actif
            link.classList.add("bg-blue-500", "text-white");
            link.classList.remove("text-gray-600", "hover:underline");
            // Forcer les styles directement pour s'assurer qu'ils sont appliqués
            link.style.backgroundColor = "#3b82f6";
            link.style.color = "white";
            console.log("✅ Classes et styles ajoutés pour lien actif");
        } else {
            // Retirer les classes d'état actif et remettre les classes normales
            link.classList.remove("bg-blue-500", "text-white");
            link.classList.add("text-gray-600", "hover:underline");
            // Retirer les styles forcés
            link.style.backgroundColor = "";
            link.style.color = "";
        }
    });
});