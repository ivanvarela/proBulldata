from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .constants import *

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    activo = models.BooleanField(default=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    celular = models.CharField(max_length=32, null=True, blank=True)
    imagen = models.ImageField(default='default.jpeg', null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    status = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        default='B',
        choices=status_choices,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class RefineryRevenueReport(models.Model):
    """
    Modelo para almacenar los datos de ventas de la API de Refinery
    """
    date = models.DateField(verbose_name="Fecha")
    website = models.CharField(max_length=255, verbose_name="Sitio Web")
    clicks = models.IntegerField(default=0, verbose_name="Clicks")
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Ingresos")
    revenue_net = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Ingresos Netos")
    impressions = models.IntegerField(default=0, verbose_name="Impresiones")
    impressions_net = models.IntegerField(default=0, verbose_name="Impresiones Netas")
    tag_loads = models.IntegerField(default=0, verbose_name="Cargas de Tags")
    page_with_ads = models.IntegerField(default=0, verbose_name="Páginas con Anuncios")
    cpm = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, verbose_name="CPM")
    view_measured_impressions = models.IntegerField(default=0, verbose_name="Impresiones Medidas")
    viewable_impressions = models.IntegerField(default=0, verbose_name="Impresiones Visibles")
    viewability_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Tasa de Visibilidad")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    
    class Meta:
        verbose_name = "Reporte de Ingresos Refinery"
        verbose_name_plural = "Reportes de Ingresos Refinery"
        unique_together = ['date', 'website']  # Evita duplicados por fecha y sitio web
        ordering = ['-date', 'website']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['website']),
            models.Index(fields=['date', 'website']),
        ]
    
    def __str__(self):
        return f"{self.date} - {self.website} - ${self.revenue}"
    
    @property
    def ctr(self):
        """Calcula el CTR (Click Through Rate)"""
        if self.impressions > 0:
            return (self.clicks / self.impressions) * 100
        return 0