# bets/utils.py
from datetime import date, datetime, timedelta
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Q
from django.utils import timezone
from bets.models import RefineryRevenueReport
import calendar
from django.core.mail import EmailMessage

from utils.email_templates import get_account_approved_template


def get_table_data_last_30_days():
    """
    Obtiene un queryset de RefineryRevenueReport de los últimos 30 días ordenado
    de más reciente a más antiguo.

    Returns:
        queryset: Queryset de RefineryRevenueReport filtrado y ordenado
    """
    # Obtener fechas de los últimos 30 días (hasta ayer)
    today = date.today()
    yesterday = today - timedelta(days=1)
    start_date = yesterday - timedelta(days=29)  # 30 días en total incluyendo ayer

    # Filtrar y ordenar el queryset
    revenue_data = (RefineryRevenueReport.objects.filter(
        date__gte=start_date,
        date__lte=yesterday
    ).only('website', 'date', 'impressions_net', 'cpm', 'revenue_net').order_by('-date'))
    # Ordenar de más reciente a más antiguo

    return {'table_revenue': revenue_data}


def get_revenue_metrics(context=None):
    """
    Calcula métricas de revenue para diferentes períodos de tiempo y
    las comparativas entre períodos.

    Args:
        context (dict, optional): Diccionario de contexto al que se agregarán las métricas.
                                  Si es None, se creará uno nuevo.

    Returns:
        dict: Diccionario con las métricas calculadas
    """
    if context is None:
        context = {}

    # Fechas de referencia
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Día de la semana anterior (mismo día de la semana que ayer pero de la semana pasada)
    same_day_last_week = yesterday - timedelta(days=7)

    # Inicio y fin de esta semana
    start_of_this_week = today - timedelta(days=today.weekday())
    end_of_this_week = yesterday  # Solo hasta ayer

    # Inicio y fin de la semana pasada
    start_of_last_week = start_of_this_week - timedelta(days=7)
    end_of_last_week = start_of_this_week - timedelta(days=1)

    # Inicio de este mes hasta ayer
    start_of_this_month = today.replace(day=1)
    end_of_this_month = yesterday  # Solo hasta ayer

    # Mismo período del mes pasado
    last_month = (today.replace(day=1) - timedelta(days=1)).month
    last_month_year = (today.replace(day=1) - timedelta(days=1)).year

    start_of_last_month = date(last_month_year, last_month, 1)
    # Calculamos el mismo día del mes, o el último día si el mes pasado tiene menos días
    day_of_month = min(yesterday.day, calendar.monthrange(last_month_year, last_month)[1])
    end_of_last_month_partial = date(last_month_year, last_month, day_of_month)

    # Mes pasado completo
    end_of_last_month_full = date(last_month_year, last_month,
                                  calendar.monthrange(last_month_year, last_month)[1])

    # Mes antepasado
    prev_prev_month = (start_of_last_month - timedelta(days=1)).month
    prev_prev_month_year = (start_of_last_month - timedelta(days=1)).year

    start_of_prev_prev_month = date(prev_prev_month_year, prev_prev_month, 1)
    end_of_prev_prev_month = date(prev_prev_month_year, prev_prev_month,
                                  calendar.monthrange(prev_prev_month_year, prev_prev_month)[1])

    # 1. AYER vs MISMO DÍA SEMANA PASADA
    # ---------------------------------------
    # Revenue de ayer
    yesterday_data = RefineryRevenueReport.objects.filter(date=yesterday)
    rev_yesterday = yesterday_data.aggregate(total=Sum('revenue_net'))['total'] or 0

    # Revenue del mismo día de la semana pasada
    ylw_data = RefineryRevenueReport.objects.filter(date=same_day_last_week)
    rev_ylw = ylw_data.aggregate(total=Sum('revenue_net'))['total'] or 0

    # Variación
    var_yesterday = 0 if rev_ylw == 0 else (rev_yesterday / rev_ylw) - 1

    # 2. ESTA SEMANA vs SEMANA PASADA
    # ---------------------------------------
    # Revenue de esta semana (hasta ayer)
    this_week_data = RefineryRevenueReport.objects.filter(
        date__gte=start_of_this_week,
        date__lte=end_of_this_week
    )
    rev_this_week = this_week_data.aggregate(total=Sum('revenue_net'))['total'] or 0

    # Revenue de la semana pasada
    last_week_data = RefineryRevenueReport.objects.filter(
        date__gte=start_of_last_week,
        date__lte=end_of_last_week
    )
    rev_last_week = last_week_data.aggregate(total=Sum('revenue_net'))['total'] or 0

    # Variación
    var_week = 0 if rev_last_week == 0 else (rev_this_week / rev_last_week) - 1

    # 3. ESTE MES (hasta ayer) vs MISMO PERÍODO MES PASADO
    # ---------------------------------------
    # Revenue de este mes hasta ayer
    this_month_data = RefineryRevenueReport.objects.filter(
        date__gte=start_of_this_month,
        date__lte=end_of_this_month
    )
    rev_this_month_partial = this_month_data.aggregate(total=Sum('revenue_net'))['total'] or 0

    # Revenue del mismo período del mes pasado
    last_month_partial_data = RefineryRevenueReport.objects.filter(
        date__gte=start_of_last_month,
        date__lte=end_of_last_month_partial
    )
    rev_last_month_partial = last_month_partial_data.aggregate(total=Sum('revenue_net'))['total'] or 0

    # Variación
    var_month_partial = 0 if rev_last_month_partial == 0 else (rev_this_month_partial / rev_last_month_partial) - 1

    # 4. MES PASADO COMPLETO vs MES ANTEPASADO COMPLETO
    # ---------------------------------------
    # Revenue del mes pasado completo
    last_month_full_data = RefineryRevenueReport.objects.filter(
        date__gte=start_of_last_month,
        date__lte=end_of_last_month_full
    )
    rev_last_month_full = last_month_full_data.aggregate(total=Sum('revenue_net'))['total'] or 0

    # Revenue del mes antepasado completo
    prev_prev_month_data = RefineryRevenueReport.objects.filter(
        date__gte=start_of_prev_prev_month,
        date__lte=end_of_prev_prev_month
    )
    rev_prev_prev_month = prev_prev_month_data.aggregate(total=Sum('revenue_net'))['total'] or 0

    # Variación
    var_month_full = 0 if rev_prev_prev_month == 0 else (rev_last_month_full / rev_prev_prev_month) - 1

    # Agregamos todos los valores al contexto
    metrics = {
        # Ayer vs mismo día semana pasada
        'rev_yesterday': rev_yesterday,
        'rev_ylw': rev_ylw,
        'var_yesterday': var_yesterday,
        'var_yesterday_pct': var_yesterday * 100,  # Porcentaje

        # Esta semana vs semana pasada
        'rev_this_week': rev_this_week,
        'rev_last_week': rev_last_week,
        'var_week': var_week,
        'var_week_pct': var_week * 100,  # Porcentaje

        # Este mes (parcial) vs mismo período mes pasado
        'rev_this_month_partial': rev_this_month_partial,
        'rev_last_month_partial': rev_last_month_partial,
        'var_month_partial': var_month_partial,
        'var_month_partial_pct': var_month_partial * 100,  # Porcentaje

        # Mes pasado completo vs mes antepasado completo
        'rev_last_month_full': rev_last_month_full,
        'rev_prev_prev_month': rev_prev_prev_month,
        'var_month_full': var_month_full,
        'var_month_full_pct': var_month_full * 100,  # Porcentaje

        # Fechas de referencia para mostrar en la interfaz
        'yesterday_date': yesterday,
        'same_day_last_week_date': same_day_last_week,
        'this_week_start': start_of_this_week,
        'this_week_end': end_of_this_week,
        'last_week_start': start_of_last_week,
        'last_week_end': end_of_last_week,
        'this_month_start': start_of_this_month,
        'this_month_end': end_of_this_month,
        'last_month_start': start_of_last_month,
        'last_month_end_partial': end_of_last_month_partial,
        'last_month_full_start': start_of_last_month,
        'last_month_full_end': end_of_last_month_full,
        'prev_prev_month_start': start_of_prev_prev_month,
        'prev_prev_month_end': end_of_prev_prev_month,
    }

    # Actualizar el contexto con las métricas calculadas
    if context is not None:
        context.update(metrics)

    # Obtener datos para el gráfico
    # Obtener datos para el gráfico
    chart_data = get_chart_data_last_30_days()
    context.update(chart_data)

    # Obtener datos para la tabla
    table_revenue = get_table_data_last_30_days()
    context['table_revenue'] = table_revenue

    table_data = get_table_data_last_30_days()
    context.update(table_data)

    return context


def get_chart_data_last_30_days():
    """
    Obtiene datos de los últimos 30 días para el gráfico de ingresos e impresiones.

    Returns:
        dict: Diccionario con listas de fechas, ingresos e impresiones
    """
    # Obtener fechas de los últimos 30 días (hasta ayer)
    today = date.today()
    yesterday = today - timedelta(days=1)
    start_date = yesterday - timedelta(days=29)  # 30 días en total incluyendo ayer

    # Lista de fechas para el rango
    date_list = [start_date + timedelta(days=x) for x in range(30)]

    # Formatear fechas para el gráfico ('DD MMM')
    formatted_dates = [d.strftime('%d %b') for d in date_list]
    # Convertir directamente a lista de strings con formato JavaScript
    formatted_dates_js = "[" + ", ".join(["'" + d.strftime('%d %b') + "'" for d in date_list]) + "]"

    # Crear un diccionario para mapear fechas a sus posiciones en la lista
    date_positions = {date_list[i]: i for i in range(len(date_list))}

    # Inicializar listas para datos con ceros
    income_data = [0] * 30
    impressions_data = [0] * 30
    rpm_data = [0] * 30

    # Consultar datos agrupados por fecha
    daily_data = RefineryRevenueReport.objects.filter(
        date__gte=start_date,
        date__lte=yesterday
    ).values('date').annotate(
        total_revenue=Sum('revenue_net'),
        total_impressions=Sum('impressions_net')
    ).order_by('date')

    # Llenar las listas con datos reales
    for item in daily_data:
        position = date_positions.get(item['date'])
        if position is not None:
            income_data[position] = float(item['total_revenue'] or 0)
            impressions_data[position] = int(item['total_impressions'] or 0)
            # # Calcular RPM (Revenue per Mille) - ingresos por cada mil impresiones
            # if impressions_data[position] > 0:
            #     rpm_data[position] = round((income_data[position] / impressions_data[position]) * 1000, 2)

    # Normalizar datos de impresiones para que se muestren bien en el gráfico
    # (dividir por 1000 para que se ajusten a una escala similar a los ingresos)
    # impressions_data_normalized = [round(imp / 1000, 2) for imp in impressions_data]

    return {
        # Usar mark_safe para evitar que Django escape las comillas en el JSON
        'chart_dates': formatted_dates,
        'chart_income_data': income_data,
        'chart_impressions_data': impressions_data,
        # También incluir los datos originales por si se necesitan para cálculos
        'chart_impressions_data_original': impressions_data
    }


def send_email(email, html_message=None, subject=None):
    """
    Función general para enviar emails HTML

    Args:
        email (str): Email del destinatario
        html_message (str, optional): Mensaje HTML. Si es None, se usa un mensaje predeterminado.
        subject (str, optional): Asunto del correo. Si es None, se usa un asunto predeterminado.

    Returns:
        bool: True si el email se envió correctamente, False en caso contrario
    """
    try:
        to_email = [email]
        bcc_recipients = ['ivan.varela@gmail.com']

        # Mensaje HTML predeterminado para activación de cuenta
        if html_message is None:
            html_message = get_account_approved_template(email)

        if subject is None:
            subject = 'Su cuenta en Bulldata Dashboard ha sido aprobada'

        filtered_bcc = [bcc_email for bcc_email in bcc_recipients if bcc_email.lower() != email.lower()]

        email_message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='request@bulldata.info',
            to=to_email,
            bcc=filtered_bcc,
        )

        email_message.content_subtype = "html"
        email_message.send()
        return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
