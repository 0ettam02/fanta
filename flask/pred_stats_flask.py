from flask import Flask, request, render_template
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

def train_model():
    dataset1 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\flask\\seriea2022_23.csv", sep=",")

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

    return model, ss

model, ss = train_model()

@app.route("/", methods=["GET", "POST"])
def predict():
    dataset1 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\flask\\seriea2022_23.csv", sep=",")
    dataset2 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\flask\\seriea2023_24.csv", sep=",")

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

if __name__ == "__main__":
    app.run(debug=True)

