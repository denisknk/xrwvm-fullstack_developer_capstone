from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include Django app API routes
    path('djangoapp/', include('djangoapp.urls')),  # /djangoapp/login/ will work

    # Serve React Frontend Pages
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),  # Serve React login page
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),

    # Serve the main React app for all other routes
    path('', TemplateView.as_view(template_name="Home.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)