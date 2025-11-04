"""
Script para popular o banco de dados com dados de exemplo.

Execute: python seed_data.py
"""

import os
import sys
from datetime import datetime, date, timedelta
from decimal import Decimal

# Configurar variáveis de ambiente
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('DATABASE_URL', 'sqlite:///test.db')

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.database import get_db, init_db
from src.models.store import Store
from src.models.product import Product
from src.models.offer import Offer


def create_stores(db):
    """Cria lojas de exemplo."""
    stores_data = [
        {
            'name': 'Supermercado Central',
            'url': 'https://supercentral.com.br',
            'latitude': Decimal('-15.7942'),
            'longitude': Decimal('-47.8822'),
            'address': 'Av. Central, 123 - Asa Norte - Brasília, DF',
            'phone': '(61) 3333-4444'
        },
        {
            'name': 'Mercado Popular',
            'url': 'https://mercadopopular.com.br',
            'latitude': Decimal('-15.8000'),
            'longitude': Decimal('-47.8900'),
            'address': 'Rua Comercial, 456 - Asa Sul - Brasília, DF',
            'phone': '(61) 3333-5555'
        },
        {
            'name': 'Atacadão',
            'url': 'https://atacadao.com.br',
            'latitude': Decimal('-15.7900'),
            'longitude': Decimal('-47.8800'),
            'address': 'Rodovia BR-040, Km 10 - Taguatinga - Brasília, DF',
            'phone': '(61) 3333-6666'
        },
        {
            'name': 'Supermercado Bom Preço',
            'url': 'https://bompreco.com.br',
            'latitude': Decimal('-15.8100'),
            'longitude': Decimal('-47.9000'),
            'address': 'Av. Norte, 789 - Sobradinho - Brasília, DF',
            'phone': '(61) 3333-7777'
        },
        {
            'name': 'Carrefour',
            'url': 'https://carrefour.com.br',
            'latitude': Decimal('-15.7850'),
            'longitude': Decimal('-47.8750'),
            'address': 'Shopping Center Iguatemi - Brasília, DF',
            'phone': '(61) 3333-8888'
        }
    ]
    
    stores = []
    for store_data in stores_data:
        # Verificar se já existe
        existing = db.query(Store).filter(Store.name == store_data['name']).first()
        if existing:
            stores.append(existing)
            print(f"  ✓ Loja '{store_data['name']}' já existe")
        else:
            store = Store(**store_data)
            db.add(store)
            stores.append(store)
            print(f"  + Criada loja: {store_data['name']}")
    
    db.commit()
    print(f"\n[OK] {len(stores)} lojas criadas/verificadas\n")
    return stores


def create_products(db):
    """Cria produtos de exemplo."""
    products_data = [
        # Alimentos Básicos
        {'name': 'Arroz Tio João Tipo 1 - 5kg', 'category': 'Alimentos', 'brand': 'Tio João'},
        {'name': 'Feijão Carioca Camil - 1kg', 'category': 'Alimentos', 'brand': 'Camil'},
        {'name': 'Óleo de Soja Liza - 900ml', 'category': 'Alimentos', 'brand': 'Liza'},
        {'name': 'Açúcar Cristal União - 1kg', 'category': 'Alimentos', 'brand': 'União'},
        {'name': 'Macarrão Espaguete Galo - 500g', 'category': 'Alimentos', 'brand': 'Galo'},
        {'name': 'Farinha de Trigo Dona Benta - 1kg', 'category': 'Alimentos', 'brand': 'Dona Benta'},
        {'name': 'Sal Refinado Cisne - 1kg', 'category': 'Alimentos', 'brand': 'Cisne'},
        
        # Bebidas
        {'name': 'Coca-Cola Lata - 350ml', 'category': 'Bebidas', 'brand': 'Coca-Cola'},
        {'name': 'Guaraná Antarctica Lata - 350ml', 'category': 'Bebidas', 'brand': 'Antarctica'},
        {'name': 'Água Mineral Crystal - 1.5L', 'category': 'Bebidas', 'brand': 'Crystal'},
        
        # Frios e Laticínios
        {'name': 'Leite Longa Vida Parmalat - 1L', 'category': 'Frios e Laticínios', 'brand': 'Parmalat'},
        {'name': 'Manteiga Doriana - 200g', 'category': 'Frios e Laticínios', 'brand': 'Doriana'},
        {'name': 'Queijo Mussarela Tirolez - 500g', 'category': 'Frios e Laticínios', 'brand': 'Tirolez'},
        
        # Padaria
        {'name': 'Pão de Açúcar Francês - 500g', 'category': 'Padaria', 'brand': 'Pão de Açúcar'},
        {'name': 'Biscoito Maizena Marilan - 200g', 'category': 'Padaria', 'brand': 'Marilan'},
        
        # Limpeza
        {'name': 'Sabão em Pó Omo - 1kg', 'category': 'Limpeza', 'brand': 'Omo'},
        {'name': 'Detergente Ypê - 500ml', 'category': 'Limpeza', 'brand': 'Ypê'},
        {'name': 'Água Sanitária Qboa - 1L', 'category': 'Limpeza', 'brand': 'Qboa'},
        {'name': 'Papel Higiênico Personal Vip - 12 unidades', 'category': 'Limpeza', 'brand': 'Personal'},
        {'name': 'Sabonete Protex - 85g', 'category': 'Higiene', 'brand': 'Protex'},
        {'name': 'Shampoo Pantene - 400ml', 'category': 'Higiene', 'brand': 'Pantene'},
    ]
    
    products = []
    for product_data in products_data:
        # Verificar se já existe
        existing = db.query(Product).filter(Product.name == product_data['name']).first()
        if existing:
            products.append(existing)
            print(f"  ✓ Produto '{product_data['name']}' já existe")
        else:
            product = Product(**product_data)
            db.add(product)
            products.append(product)
            print(f"  + Criado produto: {product_data['name']}")
    
    db.commit()
    print(f"\n[OK] {len(products)} produtos criados/verificados\n")
    return products


def create_offers(db, stores, products):
    """Cria ofertas para os produtos."""
    # Mapeamento de produtos para ofertas (preço, preço original, loja_ids)
    # Cada produto terá ofertas em diferentes lojas com preços variados
    offers_config = {
        # Arroz - 3 ofertas diferentes
        'Arroz Tio João Tipo 1 - 5kg': [
            {'price': Decimal('28.90'), 'original_price': Decimal('32.90'), 'store_idx': 0},  # Central
            {'price': Decimal('27.50'), 'original_price': Decimal('30.00'), 'store_idx': 1},  # Popular
            {'price': Decimal('26.99'), 'original_price': None, 'store_idx': 2},  # Atacadão (sem desconto)
        ],
        # Feijão - 4 ofertas
        'Feijão Carioca Camil - 1kg': [
            {'price': Decimal('8.90'), 'original_price': Decimal('10.90'), 'store_idx': 0},
            {'price': Decimal('9.50'), 'original_price': None, 'store_idx': 3},
            {'price': Decimal('8.50'), 'original_price': Decimal('9.90'), 'store_idx': 2},
            {'price': Decimal('9.99'), 'original_price': None, 'store_idx': 4},
        ],
        # Óleo - 3 ofertas
        'Óleo de Soja Liza - 900ml': [
            {'price': Decimal('6.99'), 'original_price': Decimal('8.99'), 'store_idx': 1},
            {'price': Decimal('7.50'), 'original_price': None, 'store_idx': 2},
            {'price': Decimal('7.29'), 'original_price': Decimal('8.50'), 'store_idx': 0},
        ],
        # Açúcar - 2 ofertas
        'Açúcar Cristal União - 1kg': [
            {'price': Decimal('4.50'), 'original_price': Decimal('5.50'), 'store_idx': 0},
            {'price': Decimal('4.99'), 'original_price': None, 'store_idx': 2},
        ],
        # Macarrão - 3 ofertas
        'Macarrão Espaguete Galo - 500g': [
            {'price': Decimal('3.99'), 'original_price': Decimal('4.99'), 'store_idx': 0},
            {'price': Decimal('4.50'), 'original_price': None, 'store_idx': 1},
            {'price': Decimal('3.89'), 'original_price': None, 'store_idx': 2},
        ],
        # Coca-Cola - 4 ofertas
        'Coca-Cola Lata - 350ml': [
            {'price': Decimal('4.50'), 'original_price': Decimal('5.50'), 'store_idx': 0},
            {'price': Decimal('4.99'), 'original_price': None, 'store_idx': 1},
            {'price': Decimal('4.79'), 'original_price': Decimal('5.20'), 'store_idx': 2},
            {'price': Decimal('5.29'), 'original_price': None, 'store_idx': 4},
        ],
        # Leite - 3 ofertas
        'Leite Longa Vida Parmalat - 1L': [
            {'price': Decimal('5.99'), 'original_price': Decimal('7.49'), 'store_idx': 0},
            {'price': Decimal('6.50'), 'original_price': None, 'store_idx': 1},
            {'price': Decimal('5.89'), 'original_price': Decimal('6.99'), 'store_idx': 2},
        ],
        # Sabão em Pó - 2 ofertas
        'Sabão em Pó Omo - 1kg': [
            {'price': Decimal('18.90'), 'original_price': Decimal('22.90'), 'store_idx': 0},
            {'price': Decimal('19.99'), 'original_price': None, 'store_idx': 2},
        ],
        # Detergente - 3 ofertas
        'Detergente Ypê - 500ml': [
            {'price': Decimal('2.99'), 'original_price': Decimal('3.99'), 'store_idx': 0},
            {'price': Decimal('3.50'), 'original_price': None, 'store_idx': 1},
            {'price': Decimal('2.89'), 'original_price': None, 'store_idx': 2},
        ],
        # Papel Higiênico - 2 ofertas
        'Papel Higiênico Personal Vip - 12 unidades': [
            {'price': Decimal('15.90'), 'original_price': Decimal('19.90'), 'store_idx': 0},
            {'price': Decimal('16.99'), 'original_price': None, 'store_idx': 2},
        ],
        # Guaraná - 2 ofertas
        'Guaraná Antarctica Lata - 350ml': [
            {'price': Decimal('4.49'), 'original_price': Decimal('5.49'), 'store_idx': 1},
            {'price': Decimal('4.79'), 'original_price': None, 'store_idx': 2},
        ],
        # Água Mineral - 3 ofertas
        'Água Mineral Crystal - 1.5L': [
            {'price': Decimal('3.50'), 'original_price': Decimal('4.50'), 'store_idx': 0},
            {'price': Decimal('3.99'), 'original_price': None, 'store_idx': 1},
            {'price': Decimal('3.29'), 'original_price': None, 'store_idx': 2},
        ],
        # Farinha - 2 ofertas
        'Farinha de Trigo Dona Benta - 1kg': [
            {'price': Decimal('4.99'), 'original_price': Decimal('5.99'), 'store_idx': 0},
            {'price': Decimal('5.50'), 'original_price': None, 'store_idx': 2},
        ],
        # Sal - 2 ofertas
        'Sal Refinado Cisne - 1kg': [
            {'price': Decimal('2.99'), 'original_price': None, 'store_idx': 0},
            {'price': Decimal('3.29'), 'original_price': None, 'store_idx': 1},
        ],
    }
    
    offers_created = 0
    valid_until = date.today() + timedelta(days=30)  # Válido por 30 dias
    
    for product in products:
        product_name = product.name
        if product_name not in offers_config:
            # Para produtos sem configuração específica, criar ofertas genéricas
            print(f"  ⚠ Produto '{product_name}' sem configuração - criando ofertas padrão")
            for i, store in enumerate(stores[:2]):  # Apenas 2 lojas
                price = Decimal('10.00') + Decimal(str(i * 0.50))
                offer = Offer(
                    product_id=product.id,
                    store_id=store.id,
                    price=price,
                    original_price=None,
                    discount_percentage=None,
                    in_stock=True,
                    valid_until=valid_until,
                    scraped_at=datetime.utcnow()
                )
                db.add(offer)
                offers_created += 1
            continue
        
        configs = offers_config[product_name]
        for config in configs:
            store = stores[config['store_idx']]
            
            # Calcular desconto se houver preço original
            discount_percentage = None
            if config.get('original_price'):
                discount = ((config['original_price'] - config['price']) / config['original_price']) * 100
                discount_percentage = Decimal(str(round(discount, 2)))
            
            # Verificar se oferta já existe
            existing = db.query(Offer).filter(
                Offer.product_id == product.id,
                Offer.store_id == store.id
            ).first()
            
            if existing:
                # Atualizar oferta existente
                existing.price = config['price']
                existing.original_price = config.get('original_price')
                existing.discount_percentage = discount_percentage
                existing.in_stock = True
                existing.valid_until = valid_until
                existing.scraped_at = datetime.utcnow()
                print(f"    ↻ Atualizada oferta: {product_name} em {store.name}")
            else:
                # Criar nova oferta
                offer = Offer(
                    product_id=product.id,
                    store_id=store.id,
                    price=config['price'],
                    original_price=config.get('original_price'),
                    discount_percentage=discount_percentage,
                    in_stock=True,
                    valid_until=valid_until,
                    scraped_at=datetime.utcnow()
                )
                db.add(offer)
                offers_created += 1
                print(f"    + Criada oferta: {product_name} em {store.name} - R$ {config['price']}")
    
    db.commit()
    print(f"\n[OK] {offers_created} ofertas criadas/atualizadas\n")
    return offers_created


def main():
    """Função principal."""
    print("=" * 60)
    print("  MERC AI - POPULANDO BANCO DE DADOS")
    print("=" * 60)
    print()
    
    try:
        # Inicializar banco
        print("[1/3] Inicializando banco de dados...")
        init_db()
        print("[OK] Banco inicializado\n")
        
        # Obter sessão
        db = next(get_db())
        
        try:
            # Criar lojas
            print("[2/3] Criando lojas...")
            stores = create_stores(db)
            
            # Criar produtos
            print("[3/4] Criando produtos...")
            products = create_products(db)
            
            # Criar ofertas
            print("[4/4] Criando ofertas...")
            offers_count = create_offers(db, stores, products)
            
            print("=" * 60)
            print("  RESUMO")
            print("=" * 60)
            print(f"  Lojas: {len(stores)}")
            print(f"  Produtos: {len(products)}")
            print(f"  Ofertas: {offers_count}")
            print()
            print("[SUCESSO] Banco de dados populado com sucesso!")
            print()
            print("Agora você pode:")
            print("  1. Buscar produtos: GET /api/products/search?q=arroz")
            print("  2. Ver ofertas: GET /api/products/1/offers")
            print("  3. Criar lista e gerar ranking!")
            print("=" * 60)
            
        except Exception as e:
            db.rollback()
            print(f"\n[ERRO] Erro ao popular banco: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            db.close()
    
    except Exception as e:
        print(f"\n[ERRO] Erro ao inicializar: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()