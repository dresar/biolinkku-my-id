from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def rupiah_format(value):
    """Format angka menjadi format Rupiah Indonesia dengan pemisah ribuan titik"""
    try:
        # Konversi ke integer untuk menghilangkan desimal
        num = int(float(value))
        # Konversi ke string dan balik untuk memudahkan penambahan titik
        num_str = str(num)[::-1]
        # Tambahkan titik setiap 3 digit
        formatted = ''
        for i, digit in enumerate(num_str):
            if i > 0 and i % 3 == 0:
                formatted += '.'
            formatted += digit
        # Balik kembali string dan tambahkan Rp
        return f"Rp {formatted[::-1]}"
    except (ValueError, TypeError):
        return f"Rp {value}"

@register.filter
def number_format(value):
    """Format angka dengan pemisah ribuan titik (tanpa Rp)"""
    try:
        # Konversi ke integer untuk menghilangkan desimal
        num = int(float(value))
        # Konversi ke string dan balik untuk memudahkan penambahan titik
        num_str = str(num)[::-1]
        # Tambahkan titik setiap 3 digit
        formatted = ''
        for i, digit in enumerate(num_str):
            if i > 0 and i % 3 == 0:
                formatted += '.'
            formatted += digit
        # Balik kembali string
        return formatted[::-1]
    except (ValueError, TypeError):
        return str(value)