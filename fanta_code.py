import pandas as pd

# Carica il dataset da un file CSV
dataset = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\fanta\\seriea.csv", sep=",")

# Richiedi le soglie all'utente
soglia_voto_minimo = float(input("Inserisci la soglia di voto minima: "))
soglia_voto_massimo = float(input("Inserisci la soglia di voto massima: "))
soglia_assist_minimo = float(input("Inserisci la soglia di assist minima: "))
soglia_rigori_minimi_segnati = float(input("Inserisci la soglia di rigori minimi segnati: "))
soglia_rp_minimi_parati = float(input("Inserisci la soglia di rigori parati minima: "))
soglia_rc_minimi_calciati = float(input("Inserisci la soglia di rigori calciati minima: "))
soglia_r_errati_max = float(input("Inserisci la soglia di rigori sbagliati massimi: "))
soglia_amm_max = float(input("Inserisci la soglia di ammunizioni massime: "))
soglia_esp_max = float(input("Inserisci la soglia di espulsioni massime: "))
soglia_au_max = float(input("Inserisci la soglia di autogol massimi: "))

# Filtra i giocatori in base ai criteri specificati per ciascun ruolo
portieri_selezionati = dataset[
    (dataset['Mv'] >= soglia_voto_minimo) & (dataset['Mv'] < soglia_voto_massimo) & 
    (dataset['Pv'] > 10) & (dataset['R'] == 'P') & 
    (dataset['Rp'] >= soglia_rp_minimi_parati) & 
    (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & 
    (dataset['Au'] <= soglia_au_max)
].sort_values(by='Mf', ascending=False)

difensori_selezionati = dataset[
    (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) & 
    (dataset['R'] == 'D') & 
    (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
    (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & 
    (dataset['Au'] <= soglia_au_max)
].sort_values(by='Mf', ascending=False)

centrocampisti_selezionati = dataset[
    (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) & 
    (dataset['R'] == 'C') & 
    (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
    (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & 
    (dataset['Au'] <= soglia_au_max)
].sort_values(by='Mf', ascending=False)

attaccanti_selezionati = dataset[
    (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) & 
    (dataset['R'] == 'A') & 
    (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
    (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & 
    (dataset['Au'] <= soglia_au_max)
].sort_values(by='Mf', ascending=False)

# Seleziona i migliori giocatori per ciascun ruolo
portieri_finali = portieri_selezionati.head(3)
difensori_finali = difensori_selezionati.head(8)
centrocampisti_finali = centrocampisti_selezionati.head(8)
attaccanti_finali = attaccanti_selezionati.head(6)

# Combina i giocatori di tutti i ruoli per formare la squadra completa
squadra_fantacalcio = pd.concat([portieri_finali, difensori_finali, centrocampisti_finali, attaccanti_finali])

# Stampa la squadra di fantacalcio risultante
print(squadra_fantacalcio)
