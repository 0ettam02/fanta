from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    action = request.form.get("action")
    if request.method == 'POST' and action ==  'predict':
        return redirect(url_for('predict_assist'))
    return render_template('index.html')

@app.route("/predict", methods=["GET", "POST"])
def predict_assist():
    global giocatore, prediction_assist

    dataset1 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\dataset_jumbo.csv", sep=",")
    dataset2 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea2023_24.csv", sep=",")

    X = dataset1.drop(['R', 'Nome', 'Squadra', 'Id'], axis=1).values
    y = dataset1['Ass'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)
    X_test = ss.transform(X_test)

    model = Sequential()
    model.add(Dense(12, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(36, activation='relu'))
    model.add(Dense(42, activation='relu'))
    model.add(Dense(1, activation='linear'))  

    model.compile(optimizer='sgd', loss='mean_squared_error', metrics=['accuracy'])  

    print(model.summary())

    model.fit(X_train, y_train, epochs= 100)

    if request.method == 'POST':
        giocatore = request.form["giocatore"]

        if giocatore in dataset2['Nome'].values:
            giocatore_data = dataset1[dataset1['Nome'] == giocatore].drop(['R', 'Nome', 'Squadra', 'Id'], axis=1).values

            if len(giocatore_data) > 0:
                giocatore_data_normalized = ss.transform(giocatore_data)

                predicted = model.predict(giocatore_data_normalized)

                prediction_assist = predicted.mean()
                return redirect(url_for('results_stats'))

    return render_template("pred_assist.html")

@app.route('/results_stats')
def results_stats():
    return render_template("results_pred_assist.html", giocatore=giocatore, prediction_assist=prediction_assist)

if __name__ == "__main__":
    app.run(debug=True)