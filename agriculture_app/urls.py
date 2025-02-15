from django.urls import path
from django.contrib.auth import views as auth_views
from agriculture_app import views  
from .views import add_to_cart,view_cart, update_cart, remove_from_cart
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Core Pages
    path('', views.home, name='home'),  # Homepage
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('projects/', views.projects, name='projects'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('upload-product/', views.upload_product, name='upload_product'), 
    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('update-cart/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),

    path('farm-dashboard/', views.farm_dashboard, name='farm_dashboard'),
    path('record-produce/', views.record_produce, name='record_produce'),
    path('poultry-management/', views.poultry_management, name='poultry_management'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)