from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('eka/', views.admin_login, name='admin_login'),
    path('eka/logout/', views.admin_logout, name='admin_logout'),
    path('eka/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('eka/service/', views.admin_service_list, name='admin_service_list'),
    path('eka/service/add/', views.admin_service_add, name='admin_service_add'),
    path('eka/service/edit/<int:pk>/', views.admin_service_edit, name='admin_service_edit'),
    path('eka/service/delete/<int:pk>/', views.admin_service_delete, name='admin_service_delete'),
    path('eka/service/preview/<int:pk>/', views.admin_service_preview, name='admin_service_preview'),
    path('eka/product/', views.admin_product_list, name='admin_product_list'),
    path('eka/product/edit/<int:pk>/', views.admin_product_edit, name='admin_product_edit'),
    path('eka/product/add/', views.admin_product_add, name='admin_product_add'),
    path('eka/product/delete/<int:pk>/', views.admin_product_delete, name='admin_product_delete'),
    path('eka/social/', views.admin_social_list, name='admin_social_list'),
    path('eka/social/<int:pk>/', views.admin_social_edit, name='admin_social_edit'),
    path('eka/social/add/', views.admin_social_add, name='admin_social_add'),
    path('eka/social/delete/<int:pk>/', views.admin_social_delete, name='admin_social_delete'),
    path('eka/social/preview/<int:pk>/', views.admin_social_preview, name='admin_social_preview'),
    
    # Site Settings URLs
    path('eka/settings/', views.admin_settings, name='admin_settings'),
    path('eka/settings/update/', views.admin_settings_update, name='admin_settings_update'),
    
    # Admin Management URLs
    path('eka/user/', views.admin_user, name='admin_user'),
    path('eka/users/', views.admin_user_list, name='admin_user_list'),
    path('eka/settings/admin/add/', views.admin_add, name='admin_add'),
    path('eka/settings/admin/delete/<int:user_id>/', views.admin_delete, name='admin_delete'),
    path('eka/settings/admin/edit-password/<int:user_id>/', views.admin_edit_password, name='admin_edit_password'),
    
    # WhatsApp Template URLs
    path('eka/whatsapp/', views.admin_whatsapp_list, name='admin_whatsapp_list'),
    path('eka/whatsapp/edit/<int:pk>/', views.admin_whatsapp_edit, name='admin_whatsapp_edit'),
    path('eka/whatsapp/add/', views.admin_whatsapp_add, name='admin_whatsapp_add'),
    path('eka/whatsapp/delete/<int:pk>/', views.admin_whatsapp_delete, name='admin_whatsapp_delete'),
    path('eka/whatsapp/preview/<int:pk>/', views.admin_whatsapp_preview, name='admin_whatsapp_preview'),
    path('eka/whatsapp/test/<int:pk>/', views.admin_whatsapp_test, name='admin_whatsapp_test'),
    
    # Preview URLs
    path('eka/service/preview/<int:service_id>/', views.service_preview, name='service_preview'),
    path('eka/product/preview/<int:product_id>/', views.product_preview, name='product_preview'),
    path('eka/social/preview/<int:social_id>/', views.social_preview, name='social_preview'),
    
    # Public detail endpoints
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Public WhatsApp Templates
    path('api/whatsapp-templates/', views.get_whatsapp_templates, name='get_whatsapp_templates'),
    
    # Admin WhatsApp Templates API
    path('api/admin/whatsapp-templates/', views.get_admin_whatsapp_templates, name='get_admin_whatsapp_templates'),
    
    # Profile and password change URLs
    path('eka/profile/', views.admin_profile, name='admin_profile'),
    path('eka/change-password/', views.admin_change_password, name='admin_change_password'),
    path('eka/update-profile/', views.admin_update_profile, name='admin_update_profile'),
    path('eka/admin-change-password/', views.admin_change_admin_password, name='admin_change_admin_password'),
    path('eka/admin-delete/', views.admin_delete_admin, name='admin_delete_admin'),
    
    # Additional Admin URLs
    path('eka/settings/remove-photo/', views.admin_settings_remove_photo, name='admin_settings_remove_photo'),
    path('eka/product/image/delete/<int:image_id>/', views.admin_product_image_delete, name='admin_product_image_delete'),
    
    # User URLs telah dihapus
]