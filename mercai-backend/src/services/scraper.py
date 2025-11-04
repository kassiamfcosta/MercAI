"""
Scraper Service - Web Scraping

Módulo responsável por fazer scraping ético de encartes de supermercados.
"""

import time
import random
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import logging

from src.config.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()


class EncartesDFScraper:
    """
    Scraper para o site encartesdf.com.br.
    
    Implementa scraping ético com rate limiting, retry e logging.
    """
    
    def __init__(self):
        """
        Inicializa o scraper com configurações.
        """
        self.base_url = "https://encartesdf.com.br"
        self.user_agent = settings.USER_AGENT
        self.delay_min = settings.SCRAPING_DELAY_MIN
        self.delay_max = settings.SCRAPING_DELAY_MAX
        self.timeout = 10
        self.max_retries = 3
    
    def _make_request(self, url: str, retry_count: int = 0) -> Optional[requests.Response]:
        """
        Faz uma requisição HTTP com retry e tratamento de erros.
        
        Args:
            url: URL a ser requisitada.
            retry_count: Contador de tentativas.
        
        Returns:
            Optional[requests.Response]: Resposta da requisição ou None se falhar.
        """
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response
        
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout ao acessar {url}")
            if retry_count < self.max_retries:
                logger.info(f"Tentando novamente ({retry_count + 1}/{self.max_retries})...")
                time.sleep(2)
                return self._make_request(url, retry_count + 1)
            return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            if retry_count < self.max_retries:
                logger.info(f"Tentando novamente ({retry_count + 1}/{self.max_retries})...")
                time.sleep(2)
                return self._make_request(url, retry_count + 1)
            return None
    
    def _rate_limit(self) -> None:
        """
        Aplica rate limiting entre requisições.
        """
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)
    
    def get_latest_encartes(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        Busca os últimos encartes da home do site.
        
        Args:
            limit: Número máximo de encartes a retornar.
        
        Returns:
            List[Dict[str, str]]: Lista de encartes com title, url, date, store_name.
        """
        try:
            logger.info(f"Buscando últimos {limit} encartes...")
            
            response = self._make_request(self.base_url)
            if not response:
                logger.error("Não foi possível acessar a home do site")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            encartes = []
            
            # Buscar elementos de encartes (ajustar seletores conforme estrutura real do site)
            # Nota: Seletores devem ser adaptados após análise do HTML real
            encarte_elements = soup.find_all('div', class_='encarte', limit=limit)
            
            # Se não encontrar com o seletor padrão, tentar outros
            if not encarte_elements:
                encarte_elements = soup.find_all('article', limit=limit)
            
            if not encarte_elements:
                encarte_elements = soup.find_all('a', href=True, limit=limit)
            
            for element in encarte_elements[:limit]:
                try:
                    # Tentar extrair título
                    title_elem = element.find('h2') or element.find('h3') or element.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else "Sem título"
                    
                    # Tentar extrair URL
                    link_elem = element.find('a', href=True) or element
                    url = link_elem.get('href', '')
                    if url and not url.startswith('http'):
                        url = f"{self.base_url}{url}" if url.startswith('/') else f"{self.base_url}/{url}"
                    
                    # Tentar extrair nome da loja (ajustar conforme estrutura)
                    store_elem = element.find('span', class_='store') or element.find('div', class_='store-name')
                    store_name = store_elem.get_text(strip=True) if store_elem else "Loja Desconhecida"
                    
                    # Tentar extrair data (ajustar conforme estrutura)
                    date_elem = element.find('time') or element.find('span', class_='date')
                    date = date_elem.get_text(strip=True) if date_elem else "Data não disponível"
                    
                    if url:
                        encartes.append({
                            'title': title,
                            'url': url,
                            'date': date,
                            'store_name': store_name
                        })
                
                except Exception as e:
                    logger.warning(f"Erro ao processar elemento de encarte: {e}")
                    continue
            
            logger.info(f"Encontrados {len(encartes)} encartes")
            
            # Aplicar rate limiting
            self._rate_limit()
            
            return encartes
        
        except Exception as e:
            logger.error(f"Erro ao buscar encartes: {e}", exc_info=True)
            return []
    
    def get_encarte_images(self, encarte_url: str) -> List[str]:
        """
        Extrai URLs das imagens de um encarte.
        
        Args:
            encarte_url: URL do encarte.
        
        Returns:
            List[str]: Lista de URLs das imagens.
        """
        try:
            logger.info(f"Extraindo imagens de: {encarte_url}")
            
            response = self._make_request(encarte_url)
            if not response:
                logger.error(f"Não foi possível acessar o encarte: {encarte_url}")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            images = []
            
            # Buscar todas as imagens
            img_elements = soup.find_all('img')
            
            for img in img_elements:
                src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                if src:
                    # Normalizar URL
                    if not src.startswith('http'):
                        src = f"{self.base_url}{src}" if src.startswith('/') else f"{self.base_url}/{src}"
                    
                    # Filtrar apenas imagens relevantes (ajustar conforme necessário)
                    if any(keyword in src.lower() for keyword in ['encarte', 'ofert', 'produto', 'promo']):
                        images.append(src)
            
            logger.info(f"Encontradas {len(images)} imagens")
            
            # Aplicar rate limiting
            self._rate_limit()
            
            return images
        
        except Exception as e:
            logger.error(f"Erro ao extrair imagens do encarte: {e}", exc_info=True)
            return []
    
    def download_image(self, image_url: str, save_path: str) -> Optional[str]:
        """
        Baixa uma imagem e salva localmente.
        
        Args:
            image_url: URL da imagem.
            save_path: Caminho onde salvar a imagem.
        
        Returns:
            Optional[str]: Caminho do arquivo salvo ou None se falhar.
        """
        try:
            logger.info(f"Baixando imagem: {image_url}")
            
            response = self._make_request(image_url)
            if not response:
                logger.error(f"Não foi possível baixar a imagem: {image_url}")
                return None
            
            # Salvar arquivo
            import os
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Imagem salva em: {save_path}")
            
            # Aplicar rate limiting
            self._rate_limit()
            
            return save_path
        
        except Exception as e:
            logger.error(f"Erro ao baixar imagem: {e}", exc_info=True)
            return None

