from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

app = Flask(__name__)


#RETURN AI CODICI-----------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    action = request.form.get("action")
    if request.method == 'POST' and action == 'squadra':
        return redirect(url_for('squadra'))
    elif request.method == 'POST' and action == 'predict':
        return redirect(url_for('predict'))
    return render_template('index.html')


#CODICE DATA MINING CREZZIONE SQUADRA----------------------------------------------------------
@app.route('/squadra', methods=['GET', 'POST'])
def squadra():
    global squadra_fantacalcio
    if request.method == 'POST':
        dataset = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea2022_23.csv", sep=",")
        dataset2 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea2023_24.csv", sep=",")

        soglia_voto_minimo = float(request.form.get("soglia_voto_minimo", 0))
        soglia_voto_massimo = float(request.form.get("soglia_voto_massimo", 10))
        soglia_assist_minimo = float(request.form.get("soglia_Ass_minimo", 0))
        soglia_rigori_minimi_segnati = float(request.form.get("soglia_rigori_minimi_segnati", 0))
        soglia_rp_minimi_parati = float(request.form.get("soglia_rp_minimi_parati", 0))
        soglia_rc_minimi_calciati = float(request.form.get("soglia_rc_minimi_calciati", 0))
        soglia_r_errati_max = float(request.form.get("soglia_r_errati_max", 0))
        soglia_amm_max = float(request.form.get("soglia_amm_max", 0))
        soglia_esp_max = float(request.form.get("soglia_esp_max", 0))
        soglia_au_max = float(request.form.get("soglia_au_max", 0))

        for i in range(0,1):
            if dataset["Nome"][i] in dataset2["Nome"].values:
                portieri_selezionati = dataset[
                    (dataset['Mv'] >= soglia_voto_minimo) & (dataset['Mv'] < soglia_voto_massimo) & 
                    (dataset['Pv'] > 10) & (dataset['R'] == 'P') & 
                    (dataset['Rp'] >= soglia_rp_minimi_parati) & 
                    (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & 
                    (dataset['Au'] <= soglia_au_max)
                ].sort_values(by='Fm', ascending=False)

                difensori_selezionati = dataset[
                    (dataset['Fm'] >= soglia_voto_minimo) & (dataset['Fm'] < soglia_voto_massimo) & (dataset['Ass'] >= soglia_assist_minimo) & (dataset['R+'] >= soglia_rigori_minimi_segnati) &
                    (dataset['R'] == 'D') &
                    (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
                    (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & 
                    (dataset['Au'] <= soglia_au_max)
                ].sort_values(by='Fm', ascending=False)

                centrocampisti_selezionati = dataset[
                    (dataset['Fm'] >= soglia_voto_minimo) & (dataset['Fm'] < soglia_voto_massimo) & (dataset['Ass'] >= soglia_assist_minimo) & (dataset['R+'] >= soglia_rigori_minimi_segnati) &
                    (dataset['R'] == 'C') & 
                    (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
                    (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & 
                    (dataset['Au'] <= soglia_au_max)
                ].sort_values(by='Fm', ascending=False)

                attaccanti_selezionati = dataset[
                    (dataset['Fm'] >= soglia_voto_minimo) & (dataset['Fm'] < soglia_voto_massimo) & (dataset['Ass'] >= soglia_assist_minimo) & (dataset['R+'] >= soglia_rigori_minimi_segnati) &
                    (dataset['R'] == 'A') & 
                    (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R-'] <= soglia_r_errati_max) &
                    (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & 
                    (dataset['Au'] <= soglia_au_max)
                ].sort_values(by='Fm', ascending=False)

                portieri_finali = portieri_selezionati.head(3)
                difensori_finali = difensori_selezionati.head(8)
                centrocampisti_finali = centrocampisti_selezionati.head(8)
                attaccanti_finali = attaccanti_selezionati.head(6)

                squadra_fantacalcio = pd.concat([portieri_finali, difensori_finali, centrocampisti_finali, attaccanti_finali])

        return redirect(url_for('results'))
    return render_template('squadra.html')

@app.route("/predict", methods=["GET", "POST"])
def predict():
    global giocatore, prediction

    dataset1 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\flask\\seriea2022_23.csv", sep=",")
    dataset2 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\flask\\seriea2023_24.csv", sep=",")

    X = dataset1.drop(['Gf', 'R', 'Nome', 'Squadra', 'Id', 'Rm'], axis=1).values
    y = dataset1['Gf'].values

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3)

    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)

    model = Sequential()
    model.add(Dense(12, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='sgd', loss='mean_squared_error', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=100)

    if request.method == "POST":
        giocatore = request.form["giocatore"]

        if giocatore in dataset2['Nome'].values:
            giocatore_data = dataset1[dataset1['Nome'] == giocatore].drop(['Gf', 'R', 'Nome', 'Squadra', 'Id', 'Rm'], axis=1).values

            giocatore_data_normalized = ss.transform(giocatore_data)

            predicted = model.predict(giocatore_data_normalized)

            prediction = predicted[0][0]
            return redirect(url_for('results_stats'))

    return render_template("pred_squad.html")


#VISUALIZZAZIONE RISULTATI CREAZIONE SQUADRA----------------------------------------------
@app.route('/results')
def results():
        return render_template('results.html', squadra=squadra_fantacalcio)
    
#VISUALIZZAZIONE RISULTATI PREVISIONE STATISTICHE------------------------------------------
@app.route('/results_stats')
def results_stats():
    return render_template("results_pred_squad.html", giocatore=giocatore, prediction=prediction)
    
    

if __name__ == '__main__':
    app.run(debug=True)