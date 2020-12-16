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
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from api import views
from snippets import views


docs_view = include_docs_urls( title='drf API', description='API document' )

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/admin', admin.site.urls),
    path('api/snippets/', include('snippets.urls')),
    path('api/cert/', include('cert.urls')),
    #path('api/', views.Article.as_view()),
    #path('api/', include(router.urls)),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/docs', docs_view),
]

urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)