/**
 * Splash Screen - Tela inicial de carregamento
 */

import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authService } from '../services/apiService';

export default function SplashScreen({ navigation }) {
  useEffect(() => {
    // Verificar se usuário está logado após 2 segundos
    const checkAuth = async () => {
      setTimeout(async () => {
        try {
            const isAuthenticated = await authService.isAuthenticated();
            
            // Verificar se já viu o tutorial
            const hasSeenTutorial = await AsyncStorage.getItem('hasSeenTutorial');
            
            if (isAuthenticated) {
              if (hasSeenTutorial === 'true') {
                navigation.replace('Home');
              } else {
                navigation.replace('Tutorial');
              }
            } else {
              if (hasSeenTutorial === 'true') {
                navigation.replace('Login');
              } else {
                navigation.replace('Tutorial');
              }
            }
        } catch (error) {
          console.error('Erro ao verificar autenticação:', error);
          navigation.replace('Tutorial');
        }
      }, 2000);
    };

    checkAuth();
  }, [navigation]);

  return (
    <LinearGradient
      colors={['#4CAF50', '#45A049', '#388E3C']}
      style={styles.container}
    >
      <View style={styles.content}>
        <Text style={styles.logoEmoji}>🛒</Text>
        <Text style={styles.title}>MercAI</Text>
        <Text style={styles.subtitle}>Compare preços inteligentemente</Text>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  logoEmoji: {
    fontSize: 100,
    marginBottom: 20,
  },
  title: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: '#FFFFFF',
    opacity: 0.9,
  },
});

