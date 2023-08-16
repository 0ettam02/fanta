from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dataset = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\flask\\seriea.csv", sep=",")

        # Recupera i valori dai campi del form, con controlli per valori mancanti o non validi
        soglia_voto_minimo = float(request.form.get('soglia_voto_minimo', 0.0))
        soglia_voto_massimo = float(request.form.get('soglia_voto_massimo', 0.0))
        soglia_Ass_minimo = float(request.form.get('soglia_Ass_minimo', 0.0))
        soglia_rigori_minimi_segnati = float(request.form.get('soglia_rigori_minimi_segnati', 0.0))
        soglia_rp_minimi_parati = float(request.form.get('soglia_rp_minimi_parati', 0.0))
        soglia_rc_minimi_calciati = float(request.form.get('soglia_rc_minimi_calciati', 0.0))
        soglia_r_errati_max = float(request.form.get('soglia_r_errati_max', 0.0))
        soglia_amm_max = float(request.form.get('soglia_amm_max', 0.0))
        soglia_esp_max = float(request.form.get('soglia_esp_max', 0.0))
        soglia_au_max = float(request.form.get('soglia_au_max', 0.0))

        portieri_selezionati = dataset[
            (dataset['Mv'] >= soglia_voto_minimo) & (dataset['Mv'] < soglia_voto_massimo) &
            (dataset['Pv'] > 10) & (dataset['R'] == 'P') &
            (dataset['Rp'] >= soglia_rp_minimi_parati) &
            (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) &
            (dataset['Au'] <= soglia_au_max)
        ].sort_values(by='Mf', ascending=False)

        soglia_Ass_rigori_filter = (
            (dataset['Ass'] >= soglia_Ass_minimo) &
            (dataset['R+'] >= soglia_rigori_minimi_segnati)
        )

        difensori_selezionati = dataset[
            (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) &
            (dataset['R'] == 'D') & soglia_Ass_rigori_filter &
            (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
            (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) &
            (dataset['Au'] <= soglia_au_max)
        ].sort_values(by='Mf', ascending=False)

        centrocampisti_selezionati = dataset[
            (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) &
            (dataset['R'] == 'C') & soglia_Ass_rigori_filter &
            (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
            (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) &
            (dataset['Au'] <= soglia_au_max)
        ].sort_values(by='Mf', ascending=False)

        attaccanti_selezionati = dataset[
            (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) &
            (dataset['R'] == 'A') & soglia_Ass_rigori_filter &
            (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
            (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) &
            (dataset['Au'] <= soglia_au_max)
        ].sort_values(by='Mf', ascending=False)

        portieri_finali = portieri_selezionati.head(3)
        difensori_finali = difensori_selezionati.head(8)
        centrocampisti_finali = centrocampisti_selezionati.head(8)
        attaccanti_finali = attaccanti_selezionati.head(6)

        squadra_fantacalcio = pd.concat([portieri_finali, difensori_finali, centrocampisti_finali, attaccanti_finali])

        return render_template('results.html', squadra=squadra_fantacalcio)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
