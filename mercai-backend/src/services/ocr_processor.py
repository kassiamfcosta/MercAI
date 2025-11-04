"""
OCR Processor - Processamento de Imagens

Módulo responsável por extrair texto de imagens usando OCR.
"""

import os
from typing import Optional
import requests
from PIL import Image
import pytesseract
import logging

logger = logging.getLogger(__name__)


class OCRProcessor:
    """
    Processador OCR usando Tesseract.
    
    Extrai texto de imagens de encartes com pré-processamento.
    """
    
    def __init__(self, language: str = 'por'):
        """
        Inicializa o processador OCR.
        
        Args:
            language: Idioma do OCR (padrão: 'por' para português).
        """
        self.language = language
    
    def _preprocess_image(self, image_path: str) -> Image.Image:
        """
        Pré-processa a imagem para melhorar o OCR.
        
        Args:
            image_path: Caminho da imagem.
        
        Returns:
            Image.Image: Imagem pré-processada.
        """
        try:
            # Carregar imagem
            image = Image.open(image_path)
            
            # Converter para escala de cinza
            if image.mode != 'L':
                image = image.convert('L')
            
            # Aumentar contraste
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Aumentar nitidez
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Redimensionar se muito pequena (melhora OCR)
            if image.width < 300 or image.height < 300:
                scale_factor = max(300 / image.width, 300 / image.height)
                new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            return image
        
        except Exception as e:
            logger.error(f"Erro ao pré-processar imagem: {e}", exc_info=True)
            # Retornar imagem original se pré-processamento falhar
            return Image.open(image_path)
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extrai texto de uma imagem usando OCR.
        
        Args:
            image_path: Caminho da imagem.
        
        Returns:
            str: Texto extraído.
        """
        try:
            if not os.path.exists(image_path):
                logger.error(f"Arquivo não encontrado: {image_path}")
                return ""
            
            logger.info(f"Processando OCR em: {image_path}")
            
            # Pré-processar imagem
            processed_image = self._preprocess_image(image_path)
            
            # Executar OCR
            config = f'--psm 6 -l {self.language}'
            text = pytesseract.image_to_string(processed_image, config=config)
            
            # Limpar texto
            text = text.strip()
            text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
            
            logger.info(f"Texto extraído ({len(text)} caracteres)")
            
            if not text:
                logger.warning("Nenhum texto foi extraído da imagem")
            
            return text
        
        except pytesseract.TesseractNotFoundError:
            logger.error("Tesseract OCR não está instalado no sistema")
            return ""
        
        except Exception as e:
            logger.error(f"Erro ao extrair texto da imagem: {e}", exc_info=True)
            return ""
    
    def extract_text_from_url(self, image_url: str, save_path: Optional[str] = None) -> str:
        """
        Baixa uma imagem de uma URL e extrai texto.
        
        Args:
            image_url: URL da imagem.
            save_path: Caminho opcional para salvar a imagem (usado apenas temporariamente).
        
        Returns:
            str: Texto extraído.
        """
        try:
            logger.info(f"Baixando imagem de: {image_url}")
            
            # Baixar imagem
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Criar caminho temporário se não fornecido
            if not save_path:
                import tempfile
                save_path = os.path.join(tempfile.gettempdir(), f"ocr_temp_{os.getpid()}.jpg")
            
            # Salvar imagem temporariamente
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            # Extrair texto
            text = self.extract_text_from_image(save_path)
            
            # Limpar arquivo temporário se foi criado automaticamente
            if not save_path or 'temp' in save_path:
                try:
                    os.remove(save_path)
                except:
                    pass
            
            return text
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao baixar imagem de {image_url}: {e}")
            return ""
        
        except Exception as e:
            logger.error(f"Erro ao processar imagem de URL: {e}", exc_info=True)
            return ""

