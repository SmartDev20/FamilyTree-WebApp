from django import template


register = template.Library()

@register.filter('img_decode')    
def img_decode(value) :
    return value.decode()
    
register.filter('img_decode', img_decode)

