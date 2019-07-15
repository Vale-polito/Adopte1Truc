from django.conf.urls import url
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accueil/', include('appPrincipale.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
