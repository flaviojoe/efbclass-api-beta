from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from .routers import routerpatterns

urlpatterns = [
    # Modulo Instrutor Django Template
    path('', include("core.urls")),
    path('cursos/', include("cursos.urls")),

    # Admin Django
    path('admin/', admin.site.urls),

    # Api
    path('api/', include(routerpatterns)),
    path('api/auth/', include('contas.urls')),
    path('api/change_foto_perfil/<int:pk>/', include('alunos.urls')),
    path('api/aula/carregar_video/<int:pk>/', include('cursos.api.urls')),

    # re_path(r'^s3upload/', include('s3upload.urls')),
    path('entrar/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

# Django Admin
admin.site.site_header = 'e-FB Class'
admin.site.index_title = 'e-FB Class Administração'
