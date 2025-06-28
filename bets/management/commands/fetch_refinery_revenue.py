# bets/management/commands/fetch_refinery_last_90_days.py
import logging
import requests
import csv
import io
from datetime import datetime, timedelta, date
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from bets.models import RefineryRevenueReport

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Descarga datos de ventas de la API de Refinery de los últimos 90 días'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-key',
            type=str,
            help='API Key de Refinery (por defecto usa la configurada en settings)',
        )

    def handle(self, *args, **options):
        # Configurar fechas para los últimos 90 días
        end_date = date.today() - timedelta(days=1)  # Ayer
        start_date = end_date - timedelta(days=89)   # 90 días en total (incluyendo ayer)

        # Obtener API Key
        api_key = options['api_key'] or getattr(settings, 'REFINERY_API_KEY', 'LLim6leLjDSQ5Jc1UAYlIs0EKcs5Ucnb')

        if not api_key:
            self.stdout.write(
                self.style.ERROR('API Key no proporcionada. Use --api-key o configure REFINERY_API_KEY en settings')
            )
            return

        self.stdout.write(f"Iniciando descarga de datos de Refinery desde {start_date} hasta {end_date}")

        try:
            records_processed = self._fetch_data_for_period(
                api_key, start_date, end_date
            )
            
            self.stdout.write(
                self.style.SUCCESS(f"Proceso completado. Total de registros procesados: {records_processed}")
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error procesando período {start_date} - {end_date}: {str(e)}")
            )
            logger.error(f"Error en fetch_refinery_last_90_days: {str(e)}")

    def _fetch_data_for_period(self, api_key, start_date, end_date):
        """Descarga datos para un período específico"""
        url = "https://publisher.refinery89.com/api/report"

        headers = {
            'x-api-key': api_key,
            'Cookie': 'XSRF-TOKEN=eyJpdiI6IjJySzFkd3ZSazZvb044N0RlTituRnc9PSIsInZhbHVlIjoiUU9iOVhjeW1aM2hJL0VXWmpLWlNwVWRNVGZEaVVmZExFQTMvejMyVzVJWWcxbWFFL0JzYVRCQk9qYWtTOENtZGRIQWxncU1pdDA1UVVSQXZ5R3lKazNndU9SZk00aDgyTDBPWjQzMTdyMHVvYlJXeXptNnpRWEF1RHFRS1BGS1YiLCJtYWMiOiIxMjRjMDlhZTJiNmM2ZTYxYTBhN2E1MzIwZjBhOWQ1ZTBjNTkwYWU5NDVmZDhhMWZjNDRiNTc0NGFhYmZlMGE1IiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6InNDNVd6M3dWOUx0ekVlWDltcmtaRVE9PSIsInZhbHVlIjoieXNXY043a3ZqSml6WXdyaTlzcW4yQnRvRFptOE1XSHc2M2VLeURIYlIreGdIS3BFazFyZEFPaFFBNmR2NUFPTy93TEptUDFFT2VVR0owS0h0SzN2UUVvMkUyaWxwUExFWVZvaUM0MXJKbHNHVDhYMDBGRDk5c2lVQ2JhZHhVc2siLCJtYWMiOiI0NDNkM2NlNjdhZDhlN2NlNzIzMzljYzZhYWQ3ZjMzN2RjOGNmODRmYjcyNzU5Yjg3NDQwMTZkMmYwYjNjNmVkIiwidGFnIjoiIn0%3D'
        }

        try:
            # Construir URL con parámetros
            url = url + f'?start={start_date}&end={end_date}'
            
            self.stdout.write(f"Realizando petición a: {url}")
            
            response = requests.request("GET", url, headers=headers, data={})
            response.raise_for_status()

            # Procesar el CSV
            csv_data = response.text
            records_processed = self._process_csv_data(csv_data, start_date, end_date)

            return records_processed

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la petición HTTP: {str(e)}")
        except Exception as e:
            raise Exception(f"Error procesando respuesta: {str(e)}")

    def _process_csv_data(self, csv_data, start_date, end_date):
        """Procesa los datos CSV y los guarda en la base de datos"""
        records_processed = 0

        try:
            # Crear un buffer de memoria para el CSV
            csv_buffer = io.StringIO(csv_data)
            csv_reader = csv.DictReader(csv_buffer)

            for row in csv_reader:
                try:
                    # Parsear la fecha
                    date_str = row.get('date', '').strip()
                    if not date_str:
                        continue

                    try:
                        report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        # Intentar otros formatos de fecha si es necesario
                        continue

                    # Verificar que la fecha esté en el rango esperado
                    if not (start_date <= report_date <= end_date):
                        continue

                    # Crear o actualizar el registro
                    # Como la combinación (date, website) es única, esto reemplazará 
                    # los registros existentes con los nuevos valores

                    # Calcular impressions_net (impresiones * revshare)
                    revshare = 0.78
                    impressions = self._parse_int(row.get('impressions', 0))
                    impressions_net = int(impressions * revshare)  # Convertir a entero sin decimales
                    cpm = self._parse_decimal(row.get('cpm', 0))
                    revenue_net = (impressions_net * cpm)/1000


                    report, created = RefineryRevenueReport.objects.update_or_create(
                        date=report_date,
                        website=row.get('website', '').strip(),
                        defaults={
                            'clicks': self._parse_int(row.get('clicks', 0)),
                            'revenue': self._parse_decimal(row.get('revenue', 0)),
                            'revenue_net': revenue_net,
                            'impressions': impressions,
                            'impressions_net': impressions_net,
                            'tag_loads': self._parse_int(row.get('tag_loads', 0)),
                            'page_with_ads': self._parse_int(row.get('page_with_ads', 0)),
                            'cpm': self._parse_decimal(row.get('cpm', 0)),
                            'view_measured_impressions': self._parse_int(row.get('view_measured_impressions', 0)),
                            'viewable_impressions': self._parse_int(row.get('viewable_impressions', 0)),
                            'viewability_rate': self._parse_decimal(row.get('viewability_rate', 0)),
                        }
                    )

                    records_processed += 1

                    if records_processed % 100 == 0:
                        self.stdout.write(f"Procesados {records_processed} registros hasta ahora...")

                except Exception as e:
                    logger.error(f"Error procesando fila CSV: {str(e)}")
                    continue

        except Exception as e:
            raise Exception(f"Error procesando CSV: {str(e)}")

        return records_processed

    def _parse_int(self, value):
        """Convierte un valor a entero de forma segura"""
        try:
            if isinstance(value, str):
                # Remover caracteres no numéricos excepto el signo
                cleaned = ''.join(c for c in value if c.isdigit() or c in '+-.')
                if cleaned:
                    return int(float(cleaned))
            elif isinstance(value, (int, float)):
                return int(value)
        except (ValueError, TypeError):
            pass
        return 0

    def _parse_decimal(self, value):
        """Convierte un valor a decimal de forma segura"""
        try:
            if isinstance(value, str):
                # Remover caracteres no numéricos excepto el punto decimal y signo
                cleaned = ''.join(c for c in value if c.isdigit() or c in '+-.')
                if cleaned:
                    return float(cleaned)
            elif isinstance(value, (int, float)):
                return float(value)
        except (ValueError, TypeError):
            pass
        return 0.0