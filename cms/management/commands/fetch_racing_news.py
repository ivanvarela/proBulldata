# cms/management/commands/fetch_racing_news.py
import logging
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone
from cms.models import News  # Asegúrate que este modelo esté definido

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetches racing news from horseracingnation.com'

    def handle(self, *args, **options):

        # Iniciar proceso de scraping
        logger.info("Iniciando fetch_racing_news")
        self.stdout.write("Fetching news from horseracingnation.com...")

        url = "https://www.horseracingnation.com/news"

        try:
            url = 'https://www.horseracingnation.com/news/news.aspx'
            response = requests.get(url)

            soup = BeautifulSoup(response.content, 'lxml')
            articles = soup.find_all('article', class_='row news-story pb-2 mb-2 mt-j border-bottom')
            news = []
            cols = ['title', 'desc', 'href', 'image', 'source']

            for article in tqdm(articles, desc="Importando Noticias"):
                try:
                    # Extracción de información del artículo
                    title_element = article.find('h3').find('a')
                    title = title_element.text.strip() if title_element else "Sin título"
                    href = title_element['href'] if title_element else ""

                    # Asegurarse de que la URL es absoluta
                    if href and not href.startswith('http'):
                        href = 'https://www.horseracingnation.com' + href

                    # Buscar la imagen (primero intentar con la versión desktop, luego mobile)
                    img_element = article.find('div', class_='col-md-9 col-12').find('img') if article.find('div',
                                                                                                            class_='col-md-9 col-12') else None
                    if not img_element and article.find('div', class_='col-4'):
                        img_element = article.find('div', class_='col-4').find('img')

                    image = img_element['src'] if img_element else ""
                    image = image.replace('200x200','615x615')

                    # Descripción
                    desc_element = article.find('small')
                    desc = desc_element.text.strip() if desc_element else ""

                    # Fuente
                    source = 'HorseRacingNation.com'

                    news.append([title, desc, href, image, source])
                except Exception as e:
                    print(f"Error al procesar artículo: {e}")
                    pass

            if news:
                for n in news:
                    if not News.objects.filter(url=n[2]).exists():
                        News.objects.create(
                            title=n[0],
                            summary=n[1],
                            url=n[2],
                            image_url=n[3],
                            source=n[4]
                        )


        except requests.exceptions.RequestException as e:
            error_msg = f"Error al obtener la página: {e}"
            logger.error(error_msg)
            self.stdout.write(self.style.ERROR(error_msg))
        except Exception as e:
            error_msg = f"Error inesperado: {e}"
            logger.error(error_msg)
            self.stdout.write(self.style.ERROR(error_msg))
