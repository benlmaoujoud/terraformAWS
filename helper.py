import xml.etree.ElementTree as ET
import csv

# Fonction pour convertir la durée du format ns à secondes
def ns_to_sec(time_ns):
    return float(time_ns.replace('ns', '')) * 1e-9

# Charger et parser le fichier XML
tree = ET.parse('/Users/benlmaoujoud/ns-3-dev-git/netanim/flowMonitor')
root = tree.getroot()

# Créer et ouvrir un fichier CSV pour l'écriture
with open('/Users/benlmaoujoud/ns-3-dev-git/blo.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Écrire l'en-tête du fichier CSV
    writer.writerow(["txPackets", "rxPackets", "lostPackets", "Throughput (kbps)"])

    # Parcourir chaque élément 'Flow' dans le fichier XML
    for flow in root.find('FlowStats').findall('Flow'):
        # Convertir les temps en secondes
        time_first_tx_packet = ns_to_sec(flow.get('timeFirstTxPacket'))
        time_last_rx_packet = ns_to_sec(flow.get('timeLastRxPacket'))

        # Calculer la durée en secondes
        duration = time_last_rx_packet - time_first_tx_packet

        # Convertir les octets reçus (rxBytes) en kilobits et calculer le débit
        rx_bytes = int(flow.get('rxBytes'))
        throughput_kbps = (rx_bytes * 8 / 1000) / duration if duration > 0 else 0

        # Préparer les données pour le CSV
        flow_data = [
            flow.get('txPackets'),
            flow.get('rxPackets'),
            flow.get('lostPackets'),
            throughput_kbps
        ]

        # Écrire les données dans le fichier CSV
        writer.writerow(flow_data)
