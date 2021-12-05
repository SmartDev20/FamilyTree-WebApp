from django import template
register = template.Library()

@register.filter('img_decode')    
def img_decode(img) :
    return img.decode()

