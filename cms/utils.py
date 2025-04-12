# En cms/utils.py
import os
import requests
import logging
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from django.conf import settings
from PIL import Image
import io

logger = logging.getLogger(__name__)


def optimize_image(image_path):
    """
    Optimiza una imagen para reducir su tamaño

    Args:
        image_path: Ruta al archivo de imagen

    Returns:
        bool: True si la optimización fue exitosa
    """
    try:
        img = Image.open(image_path)

        # Convertir a RGB si es RGBA (quitar transparencia)
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Redimensionar si es demasiado grande
        max_size = (1200, 800)  # Ajusta estos valores según tus necesidades
        if img.width > max_size[0] or img.height > max_size[1]:
            img.thumbnail(max_size, Image.LANCZOS)

        # Guardar con compresión optimizada
        img.save(image_path, optimize=True, quality=85)
        return True
    except Exception as e:
        logger.error(f"Error al optimizar imagen {image_path}: {str(e)}")
        return False


def download_image(url, model_instance):
    """
    Descarga una imagen de una URL y la guarda en el campo de imagen del modelo proporcionado.
    """
    try:
        # Obtener un nombre de archivo único basado en la URL
        filename = model_instance.get_image_filename(url)

        # Descargar la imagen
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code != 200:
            logger.error(f"Error al descargar imagen: {url}, status code: {response.status_code}")
            return False

        # Guardar la imagen en el modelo
        model_instance.image.save(filename, ContentFile(response.content), save=True)

        # Optimizar la imagen descargada
        image_path = model_instance.image.path
        optimize_image(image_path)

        logger.info(f"Imagen descargada y optimizada: {filename}")
        return True

    except Exception as e:
        logger.error(f"Error al procesar imagen {url}: {str(e)}")
        return False