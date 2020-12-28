"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v1",
        description="API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="test", email="test@test.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# docs_view = include_docs_urls( title='drf API', description='API document' )

router = routers.DefaultRouter()

urlpatterns = [
    path('api/admin', admin.site.urls),
    path('api/snippets/', include('snippets.urls')),
    path('api/cert/', include('cert.urls')),
    path('api/cert/member/', include('knox.urls')),
    path('api/education/', include('education.urls')),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/docs', docs_view),
]

if settings.DEBUG:
    urlpatterns += [
        path('api/swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
# urlpatterns = format_suffix_patterns(urlpatterns)
