from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class CacheBustingStorage(ManifestStaticFilesStorage):
    """Hash les noms de fichiers statiques pour le cache-busting,
    sans essayer de remplacer les references url() dans le CSS
    (ce qui plante sur le CSS minifie de Tailwind)."""
    # Desactive le post-traitement des url() dans les fichiers
    patterns = ()
