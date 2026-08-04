from django.conf import settings
from django.http import FileResponse, Http404


def spa_view(request, path=""):
    index_path = settings.WHITENOISE_ROOT / "index.html"
    if not index_path.exists():
        raise Http404("Frontend not built yet")
    return FileResponse(open(index_path, "rb"))
