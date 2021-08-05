"""bookorbooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/book/', include('book.api.urls'), name="book"),
    path('api/country/', include('country.api.urls'), name="country"),
    path('api/account/', include('account.api.urls'), name="account"),
    path('api/school/', include('school.api.urls'), name="school"),
    path('api/quiz/', include('quiz.api.urls'), name="quiz"),
 ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/book/', include('book.api.urls'), name="book"),
#     path('api/country/', include('country.api.urls'), name="country"),
#     path('api/account/', include('account.api.urls'), name="account"),
#     path('api/school/', include('school.api.urls'), name="school"),
#     path('api/quiz/', include('quiz.api.urls'), name="quiz"),
#  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
