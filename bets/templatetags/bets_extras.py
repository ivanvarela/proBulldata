from django import template
from django.utils.safestring import mark_safe

# Inicializar la librería de templates
register = template.Library()

# Registrar el filtro
@register.filter(name='variation_display')
def variation_display(value, decimals=2):
    """
    Muestra una variación con formato: color verde/rojo y flecha arriba/abajo según sea positivo o negativo.

    Args:
        value: El valor de la variación en porcentaje
        decimals: Número de decimales a mostrar (por defecto 2)

    Returns:
        HTML formateado con el valor, color y flecha correspondiente
    """
    # Asegurar que value es un número
    try:
        value_float = float(value)
    except (ValueError, TypeError):
        return mark_safe(f'<div class="text-secondary">N/A</div>')

    # Formatear el valor con los decimales especificados
    formatted_value = f'{value_float:.{decimals}f}%'

    # Determinar clase de color y flecha según el valor
    if value_float > 0:
        css_class = 'text-success'
        icon = 'fa-arrow-up'
    elif value_float < 0:
        css_class = 'text-danger'
        icon = 'fa-arrow-down'
    else:  # value_float == 0
        css_class = 'text-body'
        icon = 'fa-equals'

    # Generar el HTML
    html = f'<div class="{css_class}"><i class="fas {icon} me-1"></i>{formatted_value}</div>'

    return mark_safe(html)
