from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # Model untuk profil pengguna yang menampilkan informasi di halaman bio link
    # Setiap User Django memiliki satu UserProfile
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Relasi ke User Django
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')  # Admin yang membuat profil ini
    display_name = models.CharField(max_length=100, blank=True, null=True)  # Nama yang ditampilkan di halaman
    title = models.CharField(max_length=100, blank=True, null=True, help_text='Jabatan atau deskripsi singkat')  # Jabatan/posisi
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)  # Foto profil (disimpan di folder media/profiles/)
    description = models.TextField(blank=True, null=True)  # Deskripsi lengkap tentang pengguna
    whatsapp = models.CharField(max_length=20, blank=True, null=True, help_text='Nomor WhatsApp (format: 628xxxxxxxxxx)')  # Nomor WhatsApp untuk kontak
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Slug untuk URL profil (harus unik)
    is_active = models.BooleanField(default=True)  # Status aktif profil
    login_count = models.IntegerField(default=0, help_text='Jumlah kali login')  # Statistik login
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Waktu pembuatan (otomatis)
    updated_at = models.DateTimeField(auto_now=True, null=True)  # Waktu update terakhir (otomatis)
    
    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.user.username
            
        # Tentukan base slug
        if not self.slug:
            base_slug = slugify(self.user.username) or 'user'
        else:
            base_slug = slugify(self.slug) or 'user'
            
        slug = base_slug
        counter = 1
        # Cari slug yang unik jika sudah ada yang menggunakan profil lain
        while UserProfile.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('home')
    
    @classmethod
    def create_for_user(cls, user):
        profile, created = cls.objects.get_or_create(
            user=user,
            defaults={
                'display_name': user.get_full_name() or user.username,
                'slug': slugify(user.username)
            }
        )
        return profile

class WhatsAppTemplate(models.Model):
    # Model untuk template pesan WhatsApp yang dapat digunakan pengguna
    # Template dikelompokkan berdasarkan kategori untuk memudahkan pencarian
    
    CATEGORY_CHOICES = (
        ('greeting', 'Salam & Sapaan'),
        ('business', 'Bisnis & Promosi'),
        ('invitation', 'Undangan'),
        ('thank_you', 'Ucapan Terima Kasih'),
        ('apology', 'Permintaan Maaf'),
        ('reminder', 'Pengingat'),
        ('congratulation', 'Ucapan Selamat'),
        ('holiday', 'Hari Raya & Libur'),
        ('birthday', 'Ulang Tahun'),
        ('motivational', 'Motivasi & Inspirasi'),
        ('announcement', 'Pengumuman'),
        ('follow_up', 'Follow Up'),
        ('other', 'Lainnya'),
    )
    
    title = models.CharField(max_length=100, help_text='Judul template untuk referensi')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other', help_text='Kategori template')
    message = models.TextField(help_text='Isi pesan template')
    description = models.CharField(max_length=200, blank=True, null=True, help_text='Deskripsi singkat tentang template')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    class Meta:
        ordering = ['category', 'order']
        verbose_name = 'WhatsApp Template'
        verbose_name_plural = 'WhatsApp Templates'

# Model UserWhatsAppTemplate telah dihapus

class Service(models.Model):
    # Model untuk layanan yang ditawarkan dan ditampilkan di halaman bio link
    # Setiap layanan memiliki tampilan visual yang dapat dikustomisasi
    
    title = models.CharField(max_length=100)  # Judul layanan
    description = models.TextField()  # Deskripsi detail layanan
    icon = models.ImageField(upload_to='services/')  # Ikon layanan (disimpan di folder media/services/)
    link = models.URLField(blank=True, null=True, help_text='Link untuk layanan ini')  # URL untuk informasi lebih lanjut
    color = models.CharField(max_length=50, default='blue')  # Warna utama layanan
    gradient_color = models.CharField(max_length=50, blank=True, null=True, help_text='Warna kedua untuk gradasi')  # Warna gradien
    gradient_type = models.CharField(max_length=20, default='linear', choices=[
        ('linear', 'Linear Gradient'),  # Gradien linear (dari satu sisi ke sisi lain)
        ('radial', 'Radial Gradient'),  # Gradien radial (dari tengah ke luar)
    ])
    gradient_direction = models.CharField(max_length=20, default='to right', choices=[
        ('to right', 'Kanan'),
        ('to left', 'Kiri'),
        ('to bottom', 'Bawah'),
        ('to top', 'Atas'),
        ('to bottom right', 'Kanan Bawah'),
        ('to bottom left', 'Kiri Bawah'),
        ('to top right', 'Kanan Atas'),
        ('to top left', 'Kiri Atas'),
    ])
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

# Model UserService telah dihapus

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', help_text='Gambar utama produk (akan tetap digunakan untuk kompatibilitas)')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    link = models.CharField(max_length=255, blank=True, null=True, help_text='Link produk')
    link_label = models.CharField(max_length=50, default='Link Produk', help_text='Label untuk link produk (misalnya: Link Demo, Link Lainnya)')
    additional_link = models.CharField(max_length=255, blank=True, null=True, help_text='Link tambahan untuk produk')
    additional_link_label = models.CharField(max_length=50, default='Link Lainnya', blank=True, null=True, help_text='Label untuk link tambahan')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

# Model UserProduct telah dihapus

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image {self.order} for {self.product.title}"
    
    class Meta:
        ordering = ['order']

# Model UserProductImage telah dihapus

class SocialMedia(models.Model):
    PLATFORM_CHOICES = (
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('github', 'GitHub'),
        ('saweria', 'Saweria'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('telegram', 'Telegram'),
        ('discord', 'Discord'),
        ('pinterest', 'Pinterest'),
        ('snapchat', 'Snapchat'),
        ('twitch', 'Twitch'),
        ('reddit', 'Reddit'),
        ('medium', 'Medium'),
        ('behance', 'Behance'),
        ('dribbble', 'Dribbble'),
        ('website', 'Website'),
        ('other', 'Other'),
    )
    platform = models.CharField(max_length=30, choices=PLATFORM_CHOICES)
    username = models.CharField(max_length=100)
    link = models.URLField()
    icon = models.CharField(max_length=50, help_text='Font Awesome class name')
    description = models.TextField(blank=True, null=True, help_text='Keterangan tambahan untuk media sosial')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.platform} - {self.username}'
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Social Media'

# Model UserSocialMedia telah dihapus

# Definisi kedua UserProfile telah dihapus dan digabungkan dengan definisi pertama

class SiteSettings(models.Model):
    # Admin Profile
    admin_photo = models.ImageField(upload_to='site/', blank=True, null=True)
    admin_name = models.CharField(max_length=100, blank=True, null=True)
    admin_title = models.CharField(max_length=100, blank=True, null=True)
    admin_description = models.TextField(blank=True, null=True)
    admin_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    
    # Footer
    footer_text = models.CharField(max_length=255, blank=True, null=True)
    footer_show_social = models.BooleanField(default=True)
    
    # Site
    site_title = models.CharField(max_length=100, blank=True, null=True)
    site_description = models.TextField(blank=True, null=True)
    site_keywords = models.TextField(blank=True, null=True, help_text='Comma separated keywords')
    site_favicon = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Main favicon image')
    favicon_16 = models.ImageField(upload_to='site/favicon/', blank=True, null=True, help_text='16x16 favicon')
    favicon_32 = models.ImageField(upload_to='site/favicon/', blank=True, null=True, help_text='32x32 favicon')
    favicon_apple_touch = models.ImageField(upload_to='site/favicon/', blank=True, null=True, help_text='180x180 Apple touch icon')
    favicon_android_192 = models.ImageField(upload_to='site/favicon/', blank=True, null=True, help_text='192x192 Android chrome icon')
    favicon_android_512 = models.ImageField(upload_to='site/favicon/', blank=True, null=True, help_text='512x512 Android chrome icon')
    favicon_manifest = models.FileField(upload_to='site/favicon/', blank=True, null=True, help_text='Web app manifest file')
    
    # SEO Settings
    meta_author = models.CharField(max_length=100, blank=True, null=True)
    meta_robots = models.CharField(max_length=100, blank=True, null=True, default='index, follow')
    meta_viewport = models.CharField(max_length=100, blank=True, null=True, default='width=device-width, initial-scale=1')
    og_title = models.CharField(max_length=100, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to='site/og/', blank=True, null=True)
    twitter_card = models.CharField(max_length=100, blank=True, null=True, default='summary_large_image')
    twitter_site = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
    
    def __str__(self):
        return 'Site Settings'
    
    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

# Model UserSiteSettings telah dihapus
