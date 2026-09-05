from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
from .models import Service, Product, SocialMedia, SiteSettings, WhatsAppTemplate, ProductImage
from .forms import ServiceForm, ProductForm, SocialMediaForm, SiteSettingsForm, WhatsAppTemplateForm
import os
import uuid
import json
import logging
from PIL import Image
import io
import base64
import re

# Setup logger
logger = logging.getLogger(__name__)


def home(request):
    services = Service.objects.filter(is_active=True).order_by('order')
    products = Product.objects.filter(is_active=True).order_by('id')
    socials = SocialMedia.objects.filter(is_active=True).order_by('order')
    site_settings = SiteSettings.objects.first() or SiteSettings.objects.create()
    whatsapp_templates = WhatsAppTemplate.objects.filter(is_active=True).order_by('order')
    
    # No automatic sync in home view - data should be managed through admin settings only
    
    # Siapkan judul halaman
    title = site_settings.site_title or 'Link Bio'
    
    context = {
        'services': services,
        'products': products,
        'socials': socials,
        'site_settings': site_settings,
        'whatsapp_templates': whatsapp_templates,
        'title': title,
    }
    
    return render(request, 'core/user/home.html', context)


@login_required
def service_preview(request, service_id):
    """Preview endpoint for service"""
    try:
        service = Service.objects.get(id=service_id)
        data = {
            'id': service.id,
            'title': service.title,
            'description': service.description,
            'icon_url': service.icon.url if service.icon else '',
            'color': service.color,
            'gradient_color': service.gradient_color,
            'gradient_type': service.gradient_type,
            'gradient_direction': service.gradient_direction,
        }
        return JsonResponse({'success': True, 'data': data})
    except Service.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Service not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def product_preview(request, product_id):
    """Preview endpoint for product in admin"""
    try:
        product = Product.objects.get(id=product_id)
        
        # Get additional images
        additional_images = []
        for img in product.images.all().order_by('order'):
            additional_images.append({
                'id': img.id,
                'url': img.image.url,
                'order': img.order
            })
        
        # Pastikan nilai harga yang dikirim adalah nilai yang benar
        # Konversi Decimal ke float untuk menghindari masalah serialisasi JSON
        try:
            price = float(product.price) if product.price is not None else 0
            # Format harga dengan 2 desimal
            price = round(price, 2)
        except (ValueError, TypeError):
            price = 0
            
        try:
            discount_price = float(product.discount_price) if product.discount_price is not None else None
            # Format harga diskon dengan 2 desimal jika ada
            if discount_price is not None:
                discount_price = round(discount_price, 2)
        except (ValueError, TypeError):
            discount_price = None
            
        data = {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'image_url': product.image.url if product.image else '',
            'price': str(price),
            'discount_price': str(discount_price) if discount_price is not None else None,
            'link': product.link,
            'link_label': product.link_label,
            'additional_link': product.additional_link,
            'additional_link_label': product.additional_link_label,
            'images': additional_images
        }
        return JsonResponse({'success': True, 'data': data})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def product_detail(request, product_id):
    """Public endpoint for product detail"""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
        
        # Get additional images
        additional_images = []
        for img in product.images.all().order_by('order'):
            additional_images.append({
                'id': img.id,
                'url': img.image.url,
                'order': img.order
            })
        
        # Pastikan nilai harga yang dikirim adalah nilai yang benar
        # Konversi Decimal ke float untuk menghindari masalah serialisasi JSON
        try:
            price = float(product.price) if product.price is not None else 0
            # Format harga dengan 2 desimal
            price = round(price, 2)
        except (ValueError, TypeError):
            price = 0
            
        try:
            discount_price = float(product.discount_price) if product.discount_price is not None else None
            # Format harga diskon dengan 2 desimal jika ada
            if discount_price is not None:
                discount_price = round(discount_price, 2)
        except (ValueError, TypeError):
            discount_price = None
        
        data = {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'image_url': product.image.url if product.image else '',
            'price': str(price),
            'discount_price': str(discount_price) if discount_price is not None else None,
            'link': product.link,
            'link_label': product.link_label,
            'additional_link': product.additional_link,
            'additional_link_label': product.additional_link_label,
            'images': additional_images
        }
        return JsonResponse({'success': True, 'data': data})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def social_preview(request, social_id):
    """Preview endpoint for social media"""
    try:
        social = SocialMedia.objects.get(id=social_id)
        data = {
            'id': social.id,
            'platform': social.platform,
            'username': social.username,
            'link': social.link,
            'icon': social.icon,
        }
        return JsonResponse({'success': True, 'data': data})
    except SocialMedia.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Social media not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# Admin Login View
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Update login count
            from .models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.login_count += 1
            profile.save()
            
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Username atau password salah')
    
    return render(request, 'core/admin/login.html')

# Admin Logout View
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Admin Dashboard View
@login_required(login_url='admin_login')
def admin_dashboard(request):
    services_count = Service.objects.count()
    products_count = Product.objects.count()
    social_media_count = SocialMedia.objects.count()
    whatsapp_count = WhatsAppTemplate.objects.count()
    site_settings = SiteSettings.objects.first()
    
    context = {
        'services_count': services_count,
        'products_count': products_count,
        'social_media_count': social_media_count,
        'whatsapp_count': whatsapp_count,
        'site_settings': site_settings,
    }
    
    return render(request, 'core/admin/dashboard.html', context)

# Service Admin Views
@login_required(login_url='admin_login')
def admin_service_list(request):
    services = Service.objects.all().order_by('order')
    form = ServiceForm()
    
    context = {
        'services': services,
        'form': form,
    }
    
    return render(request, 'core/admin/service_list.html', context)

@login_required(login_url='admin_login')
def admin_service_add(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Layanan berhasil ditambahkan',
                    'service_id': service.id
                })
            else:
                messages.success(request, 'Layanan berhasil ditambahkan')
                return redirect('admin_service_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            else:
                messages.error(request, 'Terdapat kesalahan pada form')
                return redirect('admin_service_list')
    else:
        # GET request - redirect to list page since we use modal
        return redirect('admin_service_list')

@login_required(login_url='admin_login')
def admin_service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            updated_service = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Layanan berhasil diperbarui'
                })
            else:
                messages.success(request, 'Layanan berhasil diperbarui')
                return redirect('admin_service_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
            else:
                messages.error(request, 'Terdapat kesalahan pada form')
                return redirect('admin_service_list')
    else:
        # GET request - redirect to list page since we use modal
        return redirect('admin_service_list')

@login_required(login_url='admin_login')
def admin_service_preview(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    data = {
        'id': service.id,
        'title': service.title,
        'description': service.description,
        'link': service.link,
        'color': service.color,
        'gradient_color': service.gradient_color,
        'gradient_type': service.gradient_type,
        'gradient_direction': service.gradient_direction,
        'order': service.order,
        'is_active': service.is_active,
        'icon_url': service.icon.url if service.icon else None,
    }
    
    return JsonResponse({
        'success': True,
        'data': data
    })

@login_required(login_url='admin_login')
def admin_service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        service.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Layanan berhasil dihapus'
            })
        else:
            messages.success(request, 'Layanan berhasil dihapus')
            return redirect('admin_service_list')
    
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    })

# Product Admin Views
@login_required(login_url='admin_login')
def admin_product_list(request):
    products = Product.objects.all().order_by('id')
    form = ProductForm()
    
    context = {
        'products': products,
        'form': form,
    }
    
    return render(request, 'core/admin/product_list.html', context)

@login_required(login_url='admin_login')
def admin_product_add(request):
    if request.method == 'POST':
        try:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save()
                
                # Handle additional images
                if request.FILES.getlist('additional_images'):
                    for i, img_file in enumerate(request.FILES.getlist('additional_images')):
                        ProductImage.objects.create(
                            product=product,
                            image=img_file,
                            order=i+1
                        )
                        
                return JsonResponse({'success': True, 'message': 'Produk berhasil ditambahkan'})
            else:
                return JsonResponse({'success': False, 'message': 'Validasi gagal', 'errors': form.errors})
        except Exception as e:
            import traceback
            logger.error(f"Error adding product: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'message': 'Terjadi kesalahan saat menambahkan produk'})
    else:
        # For GET requests, redirect to product list since we're using modal
        return redirect('admin_product_list')

@login_required(login_url='admin_login')
def admin_product_edit(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        
        if request.method == 'POST':
            try:
                form = ProductForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    updated_product = form.save()
                    
                    # Handle additional images
                    if request.FILES.getlist('additional_images'):
                        for img_file in request.FILES.getlist('additional_images'):
                            ProductImage.objects.create(
                                product=product,
                                image=img_file,
                                order=product.images.count() + 1
                            )
                            
                    return JsonResponse({'success': True, 'message': 'Produk berhasil diperbarui'})
                else:
                    return JsonResponse({'success': False, 'message': 'Validasi gagal', 'errors': form.errors})
            except Exception as e:
                import traceback
                logger.error(f"Error updating product: {str(e)}", exc_info=True)
                return JsonResponse({'success': False, 'message': 'Terjadi kesalahan saat memperbarui produk'})
        
        # Check if request is AJAX (for both GET and POST)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Get additional images
            additional_images = []
            for img in product.images.all().order_by('order'):
                additional_images.append({
                    'id': img.id,
                    'url': img.image.url,
                    'order': img.order
                })
            
            # Format harga dengan benar untuk JSON response
            try:
                price = float(product.price) if product.price is not None else 0
                # Format harga dengan 2 desimal
                price = round(price, 2)
            except (ValueError, TypeError):
                price = 0
                
            try:
                discount_price = float(product.discount_price) if product.discount_price is not None else None
                # Format harga diskon dengan 2 desimal jika ada
                if discount_price is not None:
                    discount_price = round(discount_price, 2)
            except (ValueError, TypeError):
                discount_price = None
            
            data = {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': str(price),
                'discount_price': str(discount_price) if discount_price is not None else None,
                'link': product.link or '',
                'link_label': product.link_label or '',
                'additional_link': product.additional_link or '',
                'additional_link_label': product.additional_link_label or '',
                'is_active': product.is_active,
                'image_url': product.image.url if product.image else None,
                'additional_images': additional_images
            }
            
            return JsonResponse({'success': True, 'data': data})
        else:
            # For non-AJAX requests, redirect to product list since we're using modal
            return redirect('admin_product_list')
    except Exception as e:
        import traceback
        logger.error(f"Error in admin_product_edit: {str(e)}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Terjadi kesalahan saat mengedit produk'})


@login_required(login_url='admin_login')
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return JsonResponse({'success': True, 'message': 'Produk berhasil dihapus'})
    
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan'})

@login_required(login_url='admin_login')
def admin_product_image_delete(request, image_id):
    """Delete additional product image"""
    if request.method == 'POST':
        try:
            image = get_object_or_404(ProductImage, id=image_id)
            image.delete()
            return JsonResponse({'success': True, 'message': 'Gambar berhasil dihapus'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan'})

# Social Media Admin Views
@login_required(login_url='admin_login')
def admin_social_list(request):
    socials = SocialMedia.objects.all().order_by('order')
    form = SocialMediaForm()
    
    context = {
        'socials': socials,
        'social_media': socials,  # Keep for backward compatibility
        'form': form,
    }
    
    return render(request, 'core/admin/social_list.html', context)

@login_required(login_url='admin_login')
def admin_social_add(request):
    if request.method == 'POST':
        form = SocialMediaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Media sosial berhasil ditambahkan'})
        else:
            return JsonResponse({'success': False, 'message': 'Validasi gagal', 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan'})

@login_required(login_url='admin_login')
def admin_social_edit(request, pk):
    social = get_object_or_404(SocialMedia, pk=pk)
    
    if request.method == 'POST':
        form = SocialMediaForm(request.POST, instance=social)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Media sosial berhasil diperbarui'})
        else:
            return JsonResponse({'success': False, 'message': 'Validasi gagal', 'errors': form.errors})
    
    # Check if request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = SocialMediaForm(instance=social)
        data = {
            'id': social.id,
            'platform': social.platform,
            'username': social.username,
            'link': social.link,
            'icon': social.icon,
            'description': social.description or '',
            'order': social.order,
            'is_active': social.is_active,
        }
        
        return JsonResponse({'success': True, 'data': data})
    else:
        # For non-AJAX requests, render the form page
        form = SocialMediaForm(instance=social)
        context = {
            'form': form,
            'social': social,
            'is_edit': True
        }
        return render(request, 'core/admin/social_edit.html', context)

@login_required(login_url='admin_login')
def admin_social_delete(request, pk):
    if request.method == 'POST':
        social = get_object_or_404(SocialMedia, pk=pk)
        social.delete()
        return JsonResponse({'success': True, 'message': 'Media sosial berhasil dihapus'})
    
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan'})

@login_required(login_url='admin_login')
def admin_social_preview(request, pk):
    social = get_object_or_404(SocialMedia, pk=pk)
    
    data = {
        'id': social.id,
        'platform': social.get_platform_display(),
        'username': social.username,
        'link': social.link,
        'icon': social.icon,
        'description': social.description or '',
        'is_active': social.is_active,
        'order': social.order,
    }
    
    return JsonResponse({'success': True, 'data': data})

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_settings(request):
    settings = SiteSettings.get_settings()
    form = SiteSettingsForm(instance=settings)
    
    # Ensure user profile exists
    from .models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Sync profile data to site settings on initial load (only if not already set)
    user = request.user
    # Always sync photo (even if None to clear it)
    settings.admin_photo = profile.photo
    # Only set admin_name if it's empty, otherwise keep existing value
    if not settings.admin_name:
        settings.admin_name = f"{user.first_name} {user.last_name}".strip() or user.username
    # Always sync title/location
    settings.admin_title = profile.title or ''
    # Always sync description/bio
    settings.admin_description = profile.description or ''
    # Always sync whatsapp
    settings.admin_whatsapp = profile.whatsapp or ''
    settings.save()
    
    # Mendapatkan daftar superuser saja
    admins = User.objects.filter(is_superuser=True).order_by('username')
    
    context = {
        'settings': settings,
        'site_settings': settings,  # Alias untuk template compatibility
        'user': request.user,  # Current user data
        'profile': profile,  # User profile data
        'form': form,
        'admins': admins,
    }
    
    return render(request, 'core/admin/settings.html', context)

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_settings_update(request):
    if request.method == 'POST':
        try:
            # Import UserProfile
            from .models import UserProfile
            
            # Update user data
            user = request.user
            if 'first_name' in request.POST:
                user.first_name = request.POST.get('first_name', '')
            if 'last_name' in request.POST:
                user.last_name = request.POST.get('last_name', '')
            if 'email' in request.POST:
                user.email = request.POST.get('email', '')
            user.save()
            
            # Update or create user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            if 'bio' in request.POST:
                profile.description = request.POST.get('bio', '')  # Map bio to description
            if 'phone' in request.POST:
                profile.whatsapp = request.POST.get('phone', '')  # Map phone to whatsapp
            if 'location' in request.POST:
                profile.title = request.POST.get('location', '')  # Map location to title
            if 'profile_image' in request.FILES:
                profile.photo = request.FILES['profile_image']
            
            # Handle admin profile fields directly
            if 'admin_description' in request.POST:
                profile.description = request.POST.get('admin_description', '')
            if 'admin_whatsapp' in request.POST:
                profile.whatsapp = request.POST.get('admin_whatsapp', '')
            if 'admin_title' in request.POST:
                profile.title = request.POST.get('admin_title', '')
            if 'admin_photo' in request.FILES:
                profile.photo = request.FILES['admin_photo']
            
            profile.save()
            
            # Update site settings
            settings = SiteSettings.get_settings()
            
            # Update only fields that are provided in the request
            updated_fields = []
            
            # Profile fields
            if 'admin_name' in request.POST:
                settings.admin_name = request.POST.get('admin_name', '')
                updated_fields.append('admin_name')
            if 'admin_title' in request.POST:
                settings.admin_title = request.POST.get('admin_title', '')
                updated_fields.append('admin_title')
            if 'admin_description' in request.POST:
                settings.admin_description = request.POST.get('admin_description', '')
                updated_fields.append('admin_description')
            if 'admin_whatsapp' in request.POST:
                settings.admin_whatsapp = request.POST.get('admin_whatsapp', '')
                updated_fields.append('admin_whatsapp')
            if 'admin_photo' in request.FILES:
                settings.admin_photo = request.FILES['admin_photo']
                updated_fields.append('admin_photo')
            
            # Site settings fields
            if 'site_title' in request.POST:
                settings.site_title = request.POST.get('site_title', '')
                updated_fields.append('site_title')
            if 'site_description' in request.POST:
                settings.site_description = request.POST.get('site_description', '')
                updated_fields.append('site_description')
            if 'site_keywords' in request.POST:
                settings.site_keywords = request.POST.get('site_keywords', '')
                updated_fields.append('site_keywords')
            if 'site_favicon' in request.FILES:
                settings.site_favicon = request.FILES['site_favicon']
                updated_fields.append('site_favicon')
            
            # SEO fields
            if 'meta_author' in request.POST:
                settings.meta_author = request.POST.get('meta_author', '')
                updated_fields.append('meta_author')
            if 'meta_robots' in request.POST:
                settings.meta_robots = request.POST.get('meta_robots', '')
                updated_fields.append('meta_robots')
            if 'og_title' in request.POST:
                settings.og_title = request.POST.get('og_title', '')
                updated_fields.append('og_title')
            if 'og_description' in request.POST:
                settings.og_description = request.POST.get('og_description', '')
                updated_fields.append('og_description')
            if 'og_image' in request.FILES:
                settings.og_image = request.FILES['og_image']
                updated_fields.append('og_image')
            if 'twitter_card' in request.POST:
                settings.twitter_card = request.POST.get('twitter_card', '')
                updated_fields.append('twitter_card')
            if 'twitter_site' in request.POST:
                settings.twitter_site = request.POST.get('twitter_site', '')
                updated_fields.append('twitter_site')
            
            # Footer fields
            if 'footer_text' in request.POST:
                settings.footer_text = request.POST.get('footer_text', '')
                updated_fields.append('footer_text')
            if 'footer_copyright' in request.POST:
                settings.footer_copyright = request.POST.get('footer_copyright', '')
                updated_fields.append('footer_copyright')
            
            settings.save()
            
            messages.success(request, 'Pengaturan berhasil diperbarui')
            return JsonResponse({'success': True, 'message': f'Pengaturan berhasil diperbarui ({len(updated_fields)} field diupdate)'})
        except Exception as e:
            error_msg = f'Terjadi kesalahan: {str(e)}'
            messages.error(request, error_msg)
            return JsonResponse({'success': False, 'message': error_msg})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@login_required(login_url='admin_login')
def admin_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        photo = request.FILES.get('photo')
        
        # Cek apakah request adalah AJAX
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        # Validasi input
        if not username or not password:
            messages.error(request, 'Username dan password harus diisi')
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Username dan password harus diisi'})
            return redirect('admin_user')
        
        # Validasi password
        if len(password) < 8:
            messages.error(request, 'Password harus minimal 8 karakter')
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Password harus minimal 8 karakter'})
            return redirect('admin_user')
        
        # Cek apakah username sudah ada
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username {username} sudah digunakan')
            if is_ajax:
                return JsonResponse({'success': False, 'message': f'Username {username} sudah digunakan'})
            return redirect('admin_user')
        
        # Cek jumlah admin yang sudah ada
        # Komentar validasi ini agar bisa menambahkan lebih dari satu admin
        # admin_count = User.objects.filter(is_staff=True).count()
        # if admin_count >= 1:
        #     error_message = 'Hanya boleh ada satu admin dalam sistem'
        #     messages.error(request, error_message)
        #     if is_ajax:
        #         return JsonResponse({'status': 'error', 'message': error_message})
        #     return redirect('admin_user')
        
        try:
            # Buat superuser baru
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True
            )
            
            # Buat atau update UserProfile
            from .models import UserProfile
            profile = UserProfile.objects.create(
                user=user,
                created_by=request.user
            )
            
            # Simpan foto jika ada
            if photo:
                profile.photo = photo
                profile.save()
                
            success_message = f'Superuser {username} berhasil ditambahkan'
            
            messages.success(request, success_message)
            
            if is_ajax:
                return JsonResponse({'success': True, 'message': success_message})
            return redirect('admin_user')
        except Exception as e:
            error_message = f'Terjadi kesalahan: {str(e)}'
            messages.error(request, error_message)
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_message})
            return redirect('admin_user')
    
    # Jika bukan POST, redirect ke halaman user management
    return redirect('admin_user')

@login_required(login_url='admin_login')
def admin_delete(request, user_id):
    # Pastikan user yang akan dihapus ada
    user = get_object_or_404(User, id=user_id)
    
    # Cek apakah user mencoba menghapus dirinya sendiri
    if request.user.id == user.id:
        messages.error(request, 'Anda tidak dapat menghapus akun yang sedang digunakan')
        return redirect('admin_user')
    
    # Cek apakah ini adalah superuser terakhir
    admin_count = User.objects.filter(is_superuser=True).count()
    if admin_count <= 1:
        messages.error(request, 'Tidak dapat menghapus superuser terakhir dalam sistem')
        return redirect('admin_user')
    
    # Hapus user
    username = user.username
    user.delete()
    
    messages.success(request, f'Superuser {username} berhasil dihapus')
    return redirect('admin_user')

@login_required(login_url='admin_login')
def admin_user(request):
    # Mendapatkan daftar superuser saja
    admins = User.objects.filter(is_superuser=True).order_by('username')
    
    # Tambahkan user yang sedang login jika tidak termasuk dalam query di atas
    if request.user.is_superuser and not admins.filter(id=request.user.id).exists():
        admins = list(admins)
        admins.insert(0, request.user)
    
    context = {
        'admins': admins,
    }
    
    return render(request, 'core/admin/user.html', context)

@login_required(login_url='admin_login')
def admin_edit_password(request, user_id):
    # Pastikan user yang akan diedit ada
    user = get_object_or_404(User, id=user_id)
    
    # Cek apakah request adalah AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        # Coba parse data JSON jika Content-Type adalah application/json
        if request.headers.get('Content-Type') == 'application/json':
            import json
            try:
                data = json.loads(request.body)
                new_password = data.get('new_password')
                confirm_password = data.get('confirm_password')
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        else:
            # Jika bukan JSON, ambil dari POST
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
        
        # Validasi input
        errors = {}
        
        if not new_password:
            errors['new_password'] = 'Password baru harus diisi'
        elif len(new_password) < 8:
            errors['new_password'] = 'Password baru harus minimal 8 karakter'
        
        if not confirm_password:
            errors['confirm_password'] = 'Konfirmasi password harus diisi'
        elif new_password != confirm_password:
            errors['confirm_password'] = 'Konfirmasi password tidak sesuai'
        
        # Jika ada error validasi
        if errors:
            if is_ajax:
                return JsonResponse({'success': False, 'errors': errors})
            for field, error in errors.items():
                messages.error(request, error)
            return redirect('admin_user')
        
        try:
            # Update password
            user.set_password(new_password)
            user.save()
            
            success_message = 'Password berhasil diperbarui'
            
            # Jika user mengedit password sendiri, perlu login ulang
            if request.user.id == user.id:
                # Update session auth hash agar user tetap login
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)
            
            if is_ajax:
                return JsonResponse({'success': True, 'message': success_message})
            
            messages.success(request, success_message)
            return redirect('admin_user')
        except Exception as e:
            error_message = f'Terjadi kesalahan: {str(e)}'
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_message})
            
            messages.error(request, error_message)
            return redirect('admin_user')
    
    # Jika bukan POST, tampilkan form edit password
    context = {
        'user': user,
    }
    
    if is_ajax:
        data = {
            'id': user.id,
            'username': user.username,
        }
        return JsonResponse({'success': True, 'data': data})
    
    return render(request, 'core/admin/edit_password.html', context)

# WhatsApp Template Admin Views
@login_required(login_url='admin_login')
def admin_whatsapp_list(request):
    whatsapp_templates = WhatsAppTemplate.objects.all().order_by('order')
    form = WhatsAppTemplateForm()
    
    context = {
        'whatsapp_templates': whatsapp_templates,
        'form': form,
    }
    
    return render(request, 'core/admin/whatsapp_list.html', context)

@login_required(login_url='admin_login')
def admin_whatsapp_add(request):
    if request.method == 'POST':
        form = WhatsAppTemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Template WhatsApp berhasil ditambahkan'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan'})

@login_required(login_url='admin_login')
def admin_whatsapp_edit(request, pk):
    template = get_object_or_404(WhatsAppTemplate, pk=pk)
    
    if request.method == 'POST':
        form = WhatsAppTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Template WhatsApp berhasil diperbarui'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    # Check if request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = WhatsAppTemplateForm(instance=template)
        data = {
            'id': template.id,
            'title': template.title,
            'category': template.category,
            'message': template.message,
            'description': template.description,
            'order': template.order,
            'is_active': template.is_active,
        }
        
        return JsonResponse({'success': True, 'data': data})
    else:
        # For non-AJAX requests, render the form page
        form = WhatsAppTemplateForm(instance=template)
        context = {
            'form': form,
            'template': template,
            'is_edit': True
        }
        return render(request, 'core/admin/whatsapp_edit.html', context)

@login_required(login_url='admin_login')
def admin_whatsapp_delete(request, pk):
    template = get_object_or_404(WhatsAppTemplate, pk=pk)
    
    if request.method == 'POST':
        template.delete()
        return JsonResponse({'success': True, 'message': 'Template WhatsApp berhasil dihapus'})
    
    return JsonResponse({'success': False, 'message': 'Metode tidak diizinkan'})

@login_required(login_url='admin_login')
def admin_whatsapp_preview(request, pk):
    template = get_object_or_404(WhatsAppTemplate, pk=pk)
    
    data = {
        'id': template.id,
        'title': template.title,
        'category': template.category,
        'category_display': template.get_category_display(),
        'message': template.message,
        'description': template.description,
        'order': template.order,
        'is_active': template.is_active,
    }
    
    return JsonResponse({'success': True, 'data': data})

@login_required(login_url='admin_login')
def admin_whatsapp_test(request, pk):
    template = get_object_or_404(WhatsAppTemplate, pk=pk)
    
    # Get admin WhatsApp number from site settings
    site_settings = SiteSettings.get_settings()
    admin_whatsapp = site_settings.admin_whatsapp
    
    if not admin_whatsapp:
        return JsonResponse({'success': False, 'message': 'Nomor WhatsApp admin belum diatur di pengaturan situs'})
    
    # Format phone number
    phone = admin_whatsapp.replace(' ', '').replace('-', '').replace('+', '')
    if phone.startswith('0'):
        phone = '62' + phone[1:]
    elif not phone.startswith('62'):
        phone = '62' + phone
    
    # Create WhatsApp URL
    import urllib.parse
    encoded_message = urllib.parse.quote(template.message)
    whatsapp_url = f'https://wa.me/{phone}?text={encoded_message}'
    
    return JsonResponse({'success': True, 'whatsapp_url': whatsapp_url})

# Public WhatsApp Template endpoint
def get_whatsapp_templates(request):
    """Public endpoint to get active WhatsApp templates"""
    templates = WhatsAppTemplate.objects.filter(is_active=True).order_by('category', 'order')
    
    # Group templates by category
    categories = {}
    for template in templates:
        category = template.category
        if category not in categories:
            categories[category] = {
                'name': template.get_category_display(),
                'templates': []
            }
        
        categories[category]['templates'].append({
            'id': template.id,
            'title': template.title,
            'message': template.message,
            'description': template.description,
        })
    
    return JsonResponse({'success': True, 'categories': categories})

# Admin WhatsApp Template endpoint
@login_required(login_url='admin_login')
def get_admin_whatsapp_templates(request):
    """Admin endpoint to get all WhatsApp templates"""
    templates = WhatsAppTemplate.objects.all().order_by('category', 'order')
    
    data = []
    for template in templates:
        data.append({
            'id': template.id,
            'title': template.title,
            'category': template.category,
            'category_display': template.get_category_display(),
            'message': template.message,
            'description': template.description,
            'order': template.order,
            'is_active': template.is_active,
        })
    
    return JsonResponse({'success': True, 'templates': data})


# User Management Views
@login_required(login_url='admin_login')
def admin_user_list(request):
    """View untuk menampilkan daftar admin/user"""
    admins = User.objects.filter(is_superuser=True).order_by('username')
    
    # Tambahkan user yang sedang login jika tidak termasuk dalam query di atas
    if request.user.is_superuser and not admins.filter(id=request.user.id).exists():
        admins = list(admins)
        admins.insert(0, request.user)
    
    context = {
        'admins': admins,
    }
    
    return render(request, 'core/admin/user.html', context)


@login_required(login_url='admin_login')
def admin_profile(request):
    """Admin profile view"""
    from .models import UserProfile
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get site settings
    site_settings = SiteSettings.objects.first() or SiteSettings.objects.create()
    
    # Count statistics
    services_count = Service.objects.count()
    products_count = Product.objects.count()
    social_media_count = SocialMedia.objects.count()
    whatsapp_count = WhatsAppTemplate.objects.count()
    
    # Get all admin users
    admins = User.objects.filter(is_staff=True).select_related('profile').order_by('username')
    
    context = {
        'services_count': services_count,
        'products_count': products_count,
        'social_media_count': social_media_count,
        'whatsapp_count': whatsapp_count,
        'profile': profile,
        'site_settings': site_settings,
        'admins': admins,
    }
    
    return render(request, 'core/admin/profile.html', context)


@login_required(login_url='admin_login')
def admin_change_password(request):
    """Change admin password"""
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Validate new passwords
        if new_password1 != new_password2:
            return JsonResponse({
                'status': 'error',
                'errors': {'new_password2': ['Password baru tidak cocok']}
            })
        
        if len(new_password1) < 6:
            return JsonResponse({
                'status': 'error',
                'errors': {'new_password1': ['Password minimal 6 karakter']}
            })
        
        # Update password
        request.user.set_password(new_password1)
        request.user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, request.user)
        
        return JsonResponse({
            'status': 'success',
            'message': 'Password berhasil diubah'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})


@login_required(login_url='admin_login')
def admin_update_profile(request):
    """Update admin profile (username, email)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Validate username
        if username and username != request.user.username:
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'status': 'error',
                    'errors': {'username': ['Username sudah digunakan']}
                })
        
        # Validate email
        if email and email != request.user.email:
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'status': 'error',
                    'errors': {'email': ['Email sudah digunakan']}
                })
        
        # Update user data
        if username:
            request.user.username = username
        if email:
            request.user.email = email
        
        request.user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Profil berhasil diperbarui'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_change_admin_password(request):
    """Change password for another admin"""
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Validate admin_id
        try:
            admin_user = User.objects.get(id=admin_id, is_staff=True)
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Admin tidak ditemukan'
            })
        
        # Prevent changing own password through this method
        if admin_user.id == request.user.id:
            return JsonResponse({
                'status': 'error',
                'message': 'Gunakan menu ubah password untuk mengubah password Anda sendiri'
            })
        
        # Validate new passwords
        if new_password1 != new_password2:
            return JsonResponse({
                'status': 'error',
                'errors': {'new_password2': ['Password baru tidak cocok']}
            })
        
        if len(new_password1) < 6:
            return JsonResponse({
                'status': 'error',
                'errors': {'new_password1': ['Password minimal 6 karakter']}
            })
        
        # Change password
        admin_user.set_password(new_password1)
        admin_user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Password untuk {admin_user.username} berhasil diubah'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_delete_admin(request):
    """Delete another admin"""
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        
        # Validate admin_id
        try:
            admin_user = User.objects.get(id=admin_id, is_staff=True)
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Admin tidak ditemukan'
            })
        
        # Prevent deleting own account
        if admin_user.id == request.user.id:
            return JsonResponse({
                'status': 'error',
                'message': 'Anda tidak dapat menghapus akun Anda sendiri'
            })
        
        # Check if this is the last superuser
        if admin_user.is_superuser:
            superuser_count = User.objects.filter(is_superuser=True).count()
            if superuser_count <= 1:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Tidak dapat menghapus superuser terakhir'
                })
        
        # Delete the admin
        username = admin_user.username
        admin_user.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Admin {username} berhasil dihapus'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})


@login_required(login_url='admin_login')
def admin_settings_remove_photo(request):
    """Remove admin photo"""
    if request.method == 'POST':
        try:
            site_settings = SiteSettings.objects.first()
            if site_settings and site_settings.admin_photo:
                site_settings.admin_photo.delete()
                site_settings.admin_photo = None
                site_settings.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Foto berhasil dihapus'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Tidak ada foto untuk dihapus'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})


@login_required(login_url='admin_login')
def admin_product_image_delete(request, image_id):
    """Delete product additional image"""
    if request.method == 'POST':
        try:
            image = get_object_or_404(ProductImage, id=image_id)
            image.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Gambar berhasil dihapus'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

# Custom error handlers
def custom_404(request, exception):
    """Custom 404 error handler"""
    site_settings = SiteSettings.objects.first() or SiteSettings.objects.create()
    context = {
        'site_settings': site_settings,
        'title': 'Halaman Tidak Ditemukan - ' + (site_settings.site_title or 'Link Bio'),
    }
    return render(request, '404.html', context, status=404)

def custom_500(request):
    """Custom 500 error handler"""
    site_settings = SiteSettings.objects.first() or SiteSettings.objects.create()
    context = {
        'site_settings': site_settings,
        'title': 'Server Error - ' + (site_settings.site_title or 'Link Bio'),
    }
    return render(request, '500.html', context, status=500)

# User-related views have been removed
