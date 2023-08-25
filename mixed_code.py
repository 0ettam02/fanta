from flask import Flask, render_template, request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

def load_datasets():
    dataset1 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\flask\\seriea2022_23.csv", sep=",")
    dataset2 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\flask\\seriea2023_24.csv", sep=",")
    return dataset1, dataset2

def train_model(dataset):
    X = dataset.drop(['Gf', 'R', 'Nome', 'Squadra', 'Id', 'Rm'], axis=1).values
    y = dataset['Gf'].values

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3)

    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)

    model = Sequential()
    model.add(Dense(12, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='sgd', loss='mean_squared_error', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=100)

    return model, ss

dataset1, dataset2 = load_datasets()
model, ss = train_model(dataset1)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Carica il dataset da un file CSV
        dataset = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea2022_23.csv", sep=",")
        dataset2 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea2023_24.csv", sep=",")

        # Leggi i valori dal form
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

        # Filtra i giocatori in base ai criteri specificati per ciascun ruolo
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

                # Seleziona i migliori giocatori per ciascun ruolo
                portieri_finali = portieri_selezionati.head(3)
                difensori_finali = difensori_selezionati.head(8)
                centrocampisti_finali = centrocampisti_selezionati.head(8)
                attaccanti_finali = attaccanti_selezionati.head(6)

                # Combina i giocatori di tutti i ruoli per formare la squadra completa
                squadra_fantacalcio = pd.concat([portieri_finali, difensori_finali, centrocampisti_finali, attaccanti_finali])

        return render_template('results.html', squadra=squadra_fantacalcio)

    return render_template('squadra.html')

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        giocatore = request.form["giocatore"]

        if giocatore in dataset2['Nome'].values:
            giocatore_data = dataset1[dataset1['Nome'] == giocatore].drop(['Gf', 'R', 'Nome', 'Squadra', 'Id', 'Rm'], axis=1).values

            giocatore_data_normalized = ss.transform(giocatore_data)

            predicted = model.predict(giocatore_data_normalized)

            prediction = predicted[0][0]
            return render_template("results_pred_squad.html", giocatore=giocatore, prediction=prediction)
        else:
            return render_template("results_pred_squad.html", giocatore=giocatore, prediction=None)

    return render_template("pred_squad.html")

if __name__ == '__main__':
    app.run(debug=True)
