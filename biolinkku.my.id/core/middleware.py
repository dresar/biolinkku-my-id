"""
Custom middleware for HTML compression
"""
import re
from django.utils.deprecation import MiddlewareMixin


class HTMLCompressionMiddleware(MiddlewareMixin):
    """
    Middleware untuk mengkompres HTML dengan menghapus whitespace yang tidak perlu
    """
    
    def process_response(self, request, response):
        # Hanya kompres jika response adalah HTML
        content_type = response.get('Content-Type', '')
        if not content_type.startswith('text/html'):
            return response
            
        # Skip untuk AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return response
            
        # Skip jika response sudah di-compress
        if response.get('Content-Encoding'):
            return response
        
        try:
            content = response.content.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            return response
        
        # Preserve content dalam tag yang sensitive
        preserved_blocks = []
        preserve_pattern = r'(<(pre|textarea|script|style)[^>]*>.*?</\2>)'
        
        def preserve_replace(match):
            preserved_blocks.append(match.group(0))
            return f'__PRESERVED_BLOCK_{len(preserved_blocks) - 1}__'
        
        # Simpan blok yang perlu di-preserve
        content = re.sub(preserve_pattern, preserve_replace, content, flags=re.DOTALL | re.IGNORECASE)
        
        # Hapus komentar HTML (kecuali conditional comments)
        content = re.sub(r'<!--(?!\[if|<!)[\s\S]*?-->', '', content)
        
        # Hapus whitespace berlebihan di antara tag
        content = re.sub(r'>\s+<', '><', content)
        
        # Hapus whitespace di awal dan akhir string
        content = content.strip()
        
        # Hapus baris kosong berlebihan
        content = re.sub(r'\n\s*\n+', '\n', content)
        
        # Hapus whitespace di awal dan akhir baris (tapi preserve single space jika perlu)
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                cleaned_lines.append(stripped)
        content = '\n'.join(cleaned_lines)
        
        # Restore preserved blocks
        for i, block in enumerate(preserved_blocks):
            content = content.replace(f'__PRESERVED_BLOCK_{i}__', block)
        
        # Final cleanup: hapus whitespace berlebihan di antara tag (tapi jangan terlalu agresif)
        content = re.sub(r'>\s{2,}<', '><', content)
        
        # Update response
        compressed_content = content.encode('utf-8')
        response.content = compressed_content
        response['Content-Length'] = str(len(compressed_content))
        
        return response

