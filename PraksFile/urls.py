from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drawer.views import index, logout_view
from django.contrib.auth import views as auth_views
from drawer.forms import DigiDrawerLoginForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path('drawer/', include('drawer.urls')),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="auth/login.html",
            authentication_form=DigiDrawerLoginForm,
        ),
        name="login",
    ),

    path("logout/", logout_view, name="logout"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
