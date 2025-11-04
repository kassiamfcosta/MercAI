/**
 * Dashboard Screen - Tela de dashboard com ranking
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { rankingService } from '../services/apiService';

export default function DashboardScreen({ navigation, route }) {
  const { listId, ranking: initialRanking } = route.params || {};
  const [ranking, setRanking] = useState(initialRanking);
  const [loading, setLoading] = useState(!initialRanking);
  const [detailed, setDetailed] = useState(false);

  useEffect(() => {
    if (!initialRanking && listId) {
      loadRanking();
    }
  }, [listId]);

  const loadRanking = async (detailed = false) => {
    if (!listId) return;

    setLoading(true);
    try {
      const response = detailed
        ? await rankingService.getDetailedRanking(listId)
        : await rankingService.getRanking(listId);

      if (response.success) {
        setRanking(response.data);
        setDetailed(detailed);
      }
    } catch (error) {
      Alert.alert('Erro', 'Não foi possível gerar o ranking');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadDetailed = () => {
    loadRanking(true);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Gerando ranking...</Text>
      </View>
    );
  }

  if (!ranking) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>Nenhum ranking disponível</Text>
      </View>
    );
  }

  const bestCombination = ranking.best_combination || {};
  const summary = ranking.summary || {};

  return (
    <ScrollView style={styles.container}>
      <LinearGradient
        colors={['#4CAF50', '#45A049']}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>Ranking de Ofertas</Text>
        <Text style={styles.headerSubtitle}>
          Melhores preços para sua lista
        </Text>
      </LinearGradient>

      {/* Resumo */}
      {bestCombination.recommended_store && (
        <View style={styles.summaryCard}>
          <Text style={styles.summaryTitle}>Melhor Loja</Text>
          <Text style={styles.storeName}>
            {bestCombination.recommended_store}
          </Text>
          <View style={styles.summaryRow}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Total Estimado</Text>
              <Text style={styles.summaryValue}>
                R$ {bestCombination.estimated_total?.toFixed(2) || '0.00'}
              </Text>
            </View>
            {bestCombination.total_savings > 0 && (
              <View style={styles.summaryItem}>
                <Text style={styles.summaryLabel}>Economia</Text>
                <Text style={styles.savingsValue}>
                  R$ {bestCombination.total_savings?.toFixed(2) || '0.00'}
                </Text>
              </View>
            )}
          </View>
        </View>
      )}

      {/* Itens do ranking */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Ofertas Recomendadas</Text>
        {ranking.items?.map((item, index) => (
          <View key={index} style={styles.itemCard}>
            <View style={styles.itemHeader}>
              <Text style={styles.productName}>
                {item.product?.name || 'Produto'}
              </Text>
              <Text style={styles.quantity}>x{item.quantity}</Text>
            </View>

            {item.best_offer ? (
              <View style={styles.offerInfo}>
                <View style={styles.offerRow}>
                  <Text style={styles.storeLabel}>Loja:</Text>
                  <Text style={styles.storeName}>
                    {item.best_offer.store?.name || 'Loja'}
                  </Text>
                </View>
                <View style={styles.offerRow}>
                  <Text style={styles.priceLabel}>Preço:</Text>
                  <Text style={styles.priceValue}>
                    R$ {item.best_offer.price?.toFixed(2) || '0.00'}
                  </Text>
                </View>
                {item.best_offer.score && (
                  <View style={styles.scoreBadge}>
                    <Text style={styles.scoreText}>
                      Score: {item.best_offer.score.toFixed(1)}
                    </Text>
                  </View>
                )}
              </View>
            ) : (
              <Text style={styles.noOffer}>Nenhuma oferta disponível</Text>
            )}

            {detailed && item.all_offers?.length > 1 && (
              <View style={styles.alternatives}>
                <Text style={styles.alternativesTitle}>Outras ofertas:</Text>
                {item.all_offers.slice(1, 4).map((offer, idx) => (
                  <View key={idx} style={styles.alternativeOffer}>
                    <Text style={styles.alternativeStore}>
                      {offer.store?.name || 'Loja'}
                    </Text>
                    <Text style={styles.alternativePrice}>
                      R$ {offer.price?.toFixed(2) || '0.00'}
                    </Text>
                  </View>
                ))}
              </View>
            )}
          </View>
        ))}
      </View>

      {/* Botão para ranking detalhado */}
      {!detailed && (
        <TouchableOpacity
          style={styles.detailedButton}
          onPress={handleLoadDetailed}
        >
          <Text style={styles.detailedButtonText}>
            Ver Ranking Detalhado
          </Text>
        </TouchableOpacity>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#999',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 18,
    color: '#999',
  },
  header: {
    paddingTop: 60,
    paddingBottom: 30,
    paddingHorizontal: 20,
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 10,
  },
  headerSubtitle: {
    fontSize: 18,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  summaryCard: {
    backgroundColor: '#FFFFFF',
    margin: 15,
    padding: 20,
    borderRadius: 12,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  summaryTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  storeName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
    marginBottom: 15,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  summaryItem: {
    alignItems: 'center',
  },
  summaryLabel: {
    fontSize: 14,
    color: '#999',
    marginBottom: 5,
  },
  summaryValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  savingsValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  section: {
    paddingHorizontal: 15,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
  },
  itemCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
  },
  itemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  productName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  quantity: {
    fontSize: 16,
    color: '#999',
  },
  offerInfo: {
    marginTop: 10,
  },
  offerRow: {
    flexDirection: 'row',
    marginBottom: 8,
    alignItems: 'center',
  },
  storeLabel: {
    fontSize: 14,
    color: '#999',
    marginRight: 10,
  },
  storeName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  priceLabel: {
    fontSize: 14,
    color: '#999',
    marginRight: 10,
  },
  priceValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  scoreBadge: {
    backgroundColor: '#4CAF50',
    paddingVertical: 5,
    paddingHorizontal: 10,
    borderRadius: 15,
    alignSelf: 'flex-start',
    marginTop: 10,
  },
  scoreText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: 'bold',
  },
  noOffer: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
    marginTop: 10,
  },
  alternatives: {
    marginTop: 15,
    paddingTop: 15,
    borderTopWidth: 1,
    borderTopColor: '#F5F5F5',
  },
  alternativesTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  alternativeOffer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
  },
  alternativeStore: {
    fontSize: 14,
    color: '#666',
  },
  alternativePrice: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  detailedButton: {
    backgroundColor: '#4CAF50',
    margin: 15,
    paddingVertical: 15,
    borderRadius: 12,
    alignItems: 'center',
  },
  detailedButtonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

