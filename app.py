import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np

csv_file_path = '/Users/benlmaoujoud/ns-3-dev-git/data.csv'

# Chargement du fichier CSV pour analyse
df = pd.read_csv(csv_file_path)

# Définir les noms des colonnes (ajustez-les si nécessaire)
df.columns = ['TX Packets', 'RX Packets', 'Lost Packets', 'Throughput (Kbps)']

print(df)
# Vérifiez si la colonne 'Lost Packets' existe
if 'Lost Packets' in df.columns:
    df['Packet Loss Rate'] = df['Lost Packets'] / df['TX Packets']
else:
    print("La colonne 'Lost Packets' n'existe pas dans le DataFrame.")
    exit



# Éliminer les lignes avec des valeurs NaN dans les colonnes spécifiées
df_clean = df.dropna(subset=['Packet Loss Rate', 'Throughput (Kbps)'])

# Afficher les statistiques descriptives
stats_descriptives = df_clean.describe()
print("Calculs des statistiques : ")
print(stats_descriptives)

# Test de corrélation, si suffisamment de données
if len(df_clean) > 1:
    correlation, p_value = stats.pearsonr(df_clean['Lost Packets'], df_clean['Throughput (Kbps)'])
    print(f"\nCorrélation entre le taux de perte de paquets et le débit: {correlation}, p-value: {p_value}")
else:
    print("\nPas assez de données pour calculer la corrélation.")



# Analyse de régression linéaire
X = sm.add_constant(df_clean['Lost Packets'])
Y = df_clean['Throughput (Kbps)']
model = sm.OLS(Y, X).fit()
print(model.summary())



# ... [Le reste de votre script précédent]

# Test de Shapiro-Wilk pour la normalité
shapiro_test = stats.shapiro(df_clean['Throughput (Kbps)'].dropna())
print(f"Test de Shapiro-Wilk: Statistique={shapiro_test.statistic}, p-value={shapiro_test.pvalue}")


# Test pour la distribution Log-Normale
params_lognorm = stats.lognorm.fit(df_clean['Throughput (Kbps)'].dropna())
ks_lognorm = stats.kstest(df_clean['Throughput (Kbps)'], "lognorm", args=params_lognorm)
print(f"Test KS pour Log-Normale: D={ks_lognorm.statistic}, p-value={ks_lognorm.pvalue}")




