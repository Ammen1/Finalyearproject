from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls',namespace="base")),
    path('groupchat/', include('groupchat.urls' , namespace="groupchat")),
    path('account/', include('account.urls', namespace="account")),
    path('basket/', include('basket.urls', namespace="basket")),
    path('checkout/', include('checkout.urls', namespace="checkout")),
    path('privetchat/', include('privetchat.urls', namespace="privetchat")),
    path('promotion/', include('promotion.urls', namespace="promotion")),
    path('map/', include('map.urls', namespace="map")),
    path('api/', include('groupchat.api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)