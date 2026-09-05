from django import forms
from .models import Service, Product, SocialMedia, SiteSettings, WhatsAppTemplate
import re

class ServiceForm(forms.ModelForm):
    icon = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    link = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan link layanan (opsional)'}))
    gradient_direction = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Service
        fields = ['title', 'description', 'icon', 'link', 'color', 'gradient_color', 'gradient_type', 'gradient_direction', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul layanan'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Masukkan deskripsi layanan'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan warna (contoh: blue)'}),
            'gradient_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Warna kedua untuk gradasi (opsional)'}),
            'gradient_type': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Urutan tampil'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set choices for gradient_direction
        self.fields['gradient_direction'].choices = [
            ('', '-- Pilih Arah Gradasi --'),
            ('to right', 'Kanan'),
            ('to left', 'Kiri'),
            ('to bottom', 'Bawah'),
            ('to top', 'Atas'),
            ('to bottom right', 'Kanan Bawah'),
            ('to bottom left', 'Kiri Bawah'),
            ('to top right', 'Kanan Atas'),
            ('to top left', 'Kiri Atas'),
        ]
    
    def clean_link(self):
        link = self.cleaned_data.get('link')
        if link and link.strip():
            link = link.strip()
            # Allow empty or valid URLs
            if not link.startswith(('http://', 'https://')):
                link = 'https://' + link
            # Basic URL validation - more permissive for WhatsApp links and query parameters
            import re
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain...
                r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # host...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/[^\s]*)?$', re.IGNORECASE)  # path and query parameters
            if not url_pattern.match(link):
                raise forms.ValidationError('Masukkan URL yang valid (contoh: https://example.com)')
            return link
        return ''
    
    def clean_gradient_direction(self):
        gradient_direction = self.cleaned_data.get('gradient_direction')
        # If no gradient direction is selected, use default
        if not gradient_direction:
            return 'to right'
        return gradient_direction



class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    link_label = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan label link (opsional)'}))
    additional_link_label = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan label link tambahan (opsional)'}))
    
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'price', 'discount_price', 'link', 'link_label', 'additional_link', 'additional_link_label', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul produk', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Masukkan deskripsi produk', 'required': True}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan harga (contoh: 100000)', 'required': True}),
            'discount_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan harga diskon (opsional)'}),
            'link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan link produk (opsional)'}),
            'additional_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan link tambahan (opsional)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError('Nama produk harus diisi')
        return title.strip()
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description or not description.strip():
            raise forms.ValidationError('Deskripsi produk harus diisi')
        return description.strip()

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price:
            raise forms.ValidationError('Harga harus diisi')
        
        # Remove any non-digit characters except decimal point
        price_str = re.sub(r'[^\d.]', '', str(price))
        if not price_str:
            raise forms.ValidationError('Harga harus berupa angka yang valid')
        
        try:
            price_value = float(price_str)
            if price_value <= 0:
                raise forms.ValidationError('Harga harus lebih dari 0')
            return price_value
        except ValueError:
            raise forms.ValidationError('Harga harus berupa angka yang valid')

    def clean_discount_price(self):
        discount_price = self.cleaned_data.get('discount_price')
        if discount_price:
            # Remove any non-digit characters except decimal point
            price_str = re.sub(r'[^\d.]', '', str(discount_price))
            try:
                return float(price_str)
            except ValueError:
                raise forms.ValidationError('Harga diskon harus berupa angka yang valid')
        return discount_price

    def clean_link(self):
        link = self.cleaned_data.get('link')
        if link:
            # Auto-add https:// if it looks like a domain
            if not link.startswith(('http://', 'https://')) and '.' in link:
                link = 'https://' + link
        return link

    def clean_additional_link(self):
        additional_link = self.cleaned_data.get('additional_link')
        if additional_link:
            # Auto-add https:// if it looks like a domain
            if not additional_link.startswith(('http://', 'https://')) and '.' in additional_link:
                additional_link = 'https://' + additional_link
        return additional_link



class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['platform', 'username', 'link', 'icon', 'description', 'is_active', 'order']
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan username'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan URL lengkap'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Font Awesome class name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Keterangan tambahan (opsional)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Urutan tampil'}),
        }

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['admin_photo', 'admin_name', 'admin_title', 'admin_description', 'admin_whatsapp', 'footer_text', 'footer_show_social', 'site_title', 'site_description', 'site_keywords']
        widgets = {
            'admin_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'admin_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama admin'}),
            'admin_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan jabatan admin'}),
            'admin_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Masukkan deskripsi admin'}),
            'admin_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor WhatsApp (628xxxxxxxxxx)'}),
            'footer_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teks footer'}),
            'footer_show_social': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'site_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul situs'}),
            'site_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Masukkan deskripsi situs'}),
            'site_keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Keywords dipisahkan koma'}),
        }

class WhatsAppTemplateForm(forms.ModelForm):
    class Meta:
        model = WhatsAppTemplate
        fields = ['title', 'category', 'message', 'description', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul template'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Masukkan isi pesan template'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deskripsi singkat template (opsional)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Urutan tampil'}),
        }