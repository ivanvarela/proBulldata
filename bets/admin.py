from django.contrib import admin
from .models import Profile, RefineryRevenueReport

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name', 'activo', 'status']
    list_filter = ['activo', 'status', 'is_admin', 'is_manager']
    search_fields = ['user__username', 'email', 'first_name', 'last_name']


@admin.register(RefineryRevenueReport)
class RefineryRevenueReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'website', 'clicks', 'revenue', 'impressions', 'cpm', 'viewability_rate']
    list_filter = ['date', 'website']
    search_fields = ['website']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('date', 'website')
        }),
        ('Métricas de Rendimiento', {
            'fields': ('clicks', 'impressions', 'impressions_net', 'revenue', 'cpm')
        }),
        ('Métricas Adicionales', {
            'fields': ('tag_loads', 'page_with_ads', 'view_measured_impressions', 
                      'viewable_impressions', 'viewability_rate')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
