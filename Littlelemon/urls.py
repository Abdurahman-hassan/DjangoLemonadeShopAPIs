"""
URL configuration for Littlelemon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('LittlelemonAPI.urls')),

    # djoser urls
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # rest_framework_simplejwt urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist')

]

# there are a lot of djosers urls that we can use

# auth/users/ - list of all users, create new user if i do a post request with username, email, password
# auth/users/me/ - details of the currently logged in user
# auth/users/confirms/ - confirm email
# auth/users/resend_activation/ - resend activation email
# auth/users/set_password/ - set new password
# auth/users/reset_password/ - reset password
# auth/users/reset_password_confirm/ - confirm reset password
# auth/users/set_username/ - set new username
# auth/users/reset_username/ - reset username
# auth/users/reset_username_confirm/ - confirm reset username
# auth/token/login/ - login ------- i should add user, password of admin through postman or insomnia
# auth/token/logout/ - logout

