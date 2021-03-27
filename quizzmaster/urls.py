from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import register,profile
from django.contrib.auth import views as auth_views
from quiz import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('', include('quiz.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)