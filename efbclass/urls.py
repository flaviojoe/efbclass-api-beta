from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from .routers import routerpatterns

urlpatterns = [
	# Django JET URLS

	path('admin/', admin.site.urls),

	# Api
	path('api/', include(routerpatterns)),
	path('api/auth/', include('contas.urls')),
	path('api/change_foto_perfil/<int:pk>/', include('alunos.urls')),
	path('api/aula/carregar_video/<int:pk>/', include('cursos.urls')),

	# re_path(r'^s3upload/', include('s3upload.urls')),
]

if settings.DEBUG:
	# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
	import debug_toolbar

	urlpatterns = [
					  path('__debug__/', include(debug_toolbar.urls)),
				  ] + urlpatterns

# Django Admin
admin.site.site_header = 'e-FB Class'
admin.site.index_title = 'e-FB Class Administração'
