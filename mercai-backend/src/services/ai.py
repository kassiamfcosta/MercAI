"""
AI Service - Integração com Gemini Flash

Módulo responsável por estruturar dados de encartes usando IA.
"""

import json
import re
from typing import Dict, List, Optional, Any
import google.generativeai as genai
import logging

from src.config.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()

# Configurar Gemini API
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


class AIService:
    """
    Serviço de IA usando Google Gemini Flash.
    
    Estrutura dados de encartes e categoriza produtos.
    """
    
    def __init__(self):
        """
        Inicializa o serviço de IA.
        """
        self.model_name = "gemini-1.5-flash"
        self.model = None
        
        if settings.GEMINI_API_KEY:
            try:
                self.model = genai.GenerativeModel(self.model_name)
                logger.info(f"Modelo Gemini {self.model_name} inicializado")
            except Exception as e:
                logger.error(f"Erro ao inicializar modelo Gemini: {e}")
        else:
            logger.warning("GEMINI_API_KEY não configurada")
    
    def clean_and_parse_json(self, raw_response: str) -> Optional[Dict[str, Any]]:
        """
        Limpa e faz parse do JSON retornado pela IA.
        
        Remove markdown code blocks e valida estrutura.
        
        Args:
            raw_response: Resposta bruta da IA (pode conter markdown).
        
        Returns:
            Optional[Dict[str, Any]]: JSON parseado ou None se inválido.
        """
        try:
            # Remover markdown code blocks
            cleaned = raw_response.strip()
            
            # Remover ```json no início
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            elif cleaned.startswith('```'):
                cleaned = cleaned[3:]
            
            # Remover ``` no final
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            # Tentar fazer parse
            data = json.loads(cleaned)
            
            # Validar estrutura básica
            if isinstance(data, dict):
                return data
            
            logger.warning("Resposta da IA não é um dicionário válido")
            return None
        
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao fazer parse do JSON: {e}")
            logger.debug(f"Resposta bruta: {raw_response[:200]}...")
            
            # Tentar extrair JSON manualmente
            try:
                # Buscar padrão { ... }
                match = re.search(r'\{.*\}', cleaned, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    return json.loads(json_str)
            except:
                pass
            
            return None
        
        except Exception as e:
            logger.error(f"Erro ao processar resposta da IA: {e}", exc_info=True)
            return None
    
    def structure_encarte_data(
        self,
        ocr_text: str,
        store_name: str,
        valid_until: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Estrutura dados de um encarte usando IA.
        
        Extrai produtos, preços, marcas e pesos do texto OCR.
        
        Args:
            ocr_text: Texto extraído via OCR.
            store_name: Nome do supermercado.
            valid_until: Data de validade da oferta (opcional).
        
        Returns:
            Dict[str, Any]: Dados estruturados com produtos.
        """
        if not self.model:
            logger.error("Modelo Gemini não está disponível")
            return {"products": []}
        
        try:
            # Criar prompt estruturado
            prompt = f"""Você é um extrator de dados de encartes de supermercado.

Supermercado: {store_name}
Validade: {valid_until or "Não especificada"}

Texto extraído do encarte (OCR):
{ocr_text[:5000]}  # Limitar para evitar exceder tokens

Extraia TODOS os produtos com preços visíveis e retorne APENAS um JSON válido no formato:
{{
  "products": [
    {{
      "name": "Nome completo do produto",
      "brand": "Marca (se identificável)",
      "weight": "Peso/quantidade (ex: 5kg, 500g, 1L)",
      "price": 12.99,
      "original_price": 15.99,
      "discount_percentage": 20
    }}
  ]
}}

REGRAS IMPORTANTES:
- Apenas produtos com preços visíveis no texto
- Preços em formato decimal (ex: 12.99, não "R$ 12,99")
- Se não houver desconto, omita original_price e discount_percentage
- Se não houver marca identificável, use null
- Retorne APENAS o JSON, sem markdown, sem texto adicional
- Se não encontrar produtos, retorne {{"products": []}}
"""
            
            logger.info(f"Enviando texto para estruturação (loja: {store_name})")
            
            # Chamar modelo
            response = self.model.generate_content(prompt)
            
            # Extrair texto da resposta
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            logger.debug(f"Resposta bruta da IA: {response_text[:200]}...")
            
            # Parsear JSON
            structured_data = self.clean_and_parse_json(response_text)
            
            if structured_data:
                products_count = len(structured_data.get('products', []))
                logger.info(f"Dados estruturados com sucesso: {products_count} produtos encontrados")
                return structured_data
            else:
                logger.warning("Não foi possível estruturar os dados da resposta da IA")
                return {"products": []}
        
        except Exception as e:
            logger.error(f"Erro ao estruturar dados do encarte: {e}", exc_info=True)
            return {"products": []}
    
    def categorize_product(self, product_name: str) -> str:
        """
        Categoriza um produto automaticamente.
        
        Args:
            product_name: Nome do produto.
        
        Returns:
            str: Categoria do produto.
        """
        if not self.model:
            # Fallback: categorização básica por palavras-chave
            return self._categorize_by_keywords(product_name)
        
        try:
            prompt = f"""Categorize o seguinte produto de supermercado:

Produto: {product_name}

Retorne APENAS a categoria, sem explicações. Categorias possíveis:
- Alimentos
- Bebidas
- Limpeza
- Higiene
- Carnes
- Frios e Laticínios
- Padaria
- Hortifruti
- Congelados
- Utilidades Domésticas
- Outros

Categoria:"""
            
            response = self.model.generate_content(prompt)
            category = response.text.strip() if hasattr(response, 'text') else str(response).strip()
            
            # Limpar resposta (pode ter texto adicional)
            category = category.split('\n')[0].strip()
            
            logger.debug(f"Produto '{product_name}' categorizado como: {category}")
            
            return category
        
        except Exception as e:
            logger.warning(f"Erro ao categorizar produto '{product_name}': {e}")
            return self._categorize_by_keywords(product_name)
    
    def _categorize_by_keywords(self, product_name: str) -> str:
        """
        Categorização básica por palavras-chave (fallback).
        
        Args:
            product_name: Nome do produto.
        
        Returns:
            str: Categoria do produto.
        """
        product_lower = product_name.lower()
        
        # Alimentos
        if any(kw in product_lower for kw in ['arroz', 'feijao', 'macarrao', 'oleo', 'acucar', 'farinha']):
            return 'Alimentos'
        
        # Bebidas
        if any(kw in product_lower for kw in ['refrigerante', 'suco', 'agua', 'cerveja', 'coca', 'pepsi']):
            return 'Bebidas'
        
        # Limpeza
        if any(kw in product_lower for kw in ['sabao', 'detergente', 'desinfetante', 'amaciante', 'agua sanit']):
            return 'Limpeza'
        
        # Higiene
        if any(kw in product_lower for kw in ['papel higienico', 'sabonete', 'shampoo', 'condicionador', 'pasta dente']):
            return 'Higiene'
        
        # Carnes
        if any(kw in product_lower for kw in ['carne', 'frango', 'peixe', 'linguica']):
            return 'Carnes'
        
        # Frios e Laticínios
        if any(kw in product_lower for kw in ['queijo', 'manteiga', 'iogurte', 'requeijao', 'presunto']):
            return 'Frios e Laticínios'
        
        # Padaria
        if any(kw in product_lower for kw in ['pao', 'bolo', 'bolacha', 'biscoito']):
            return 'Padaria'
        
        # Hortifruti
        if any(kw in product_lower for kw in ['tomate', 'cebola', 'batata', 'alface', 'banana', 'laranja']):
            return 'Hortifruti'
        
        # Congelados
        if any(kw in product_lower for kw in ['sorvete', 'gelo', 'frios', 'congelado']):
            return 'Congelados'
        
        return 'Outros'

