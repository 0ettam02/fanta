import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

dataset1 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea2022_23.csv", sep=",")
dataset2 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea2023_24.csv", sep=",")

X = dataset1.drop(['Gf', 'R', 'Nome', 'Squadra', 'Id', 'Rm'], axis=1).values
y = dataset1['Gf'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

model = Sequential()
model.add(Dense(12, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(1, activation='linear'))  

model.compile(optimizer='sgd', loss='mean_squared_error', metrics=['accuracy'])  # Using 'mean_squared_error' loss for regression

print(model.summary())

model.fit(X_train, y_train, epochs= 100)

giocatore = str(input("Inserisci il nome del giocatore: "))

if giocatore in dataset2['Nome'].values:
    # Estrai i dati relativi al giocatore specifico da dataset1
    giocatore_data = dataset1[dataset1['Nome'] == giocatore].drop(['Gf', 'R', 'Nome', 'Squadra', 'Id', 'Rm'], axis=1).values

    # Effettua la normalizzazione sui nuovi dati
    giocatore_data_normalized = ss.transform(giocatore_data)

    # Ottieni la previsione del numero di gol fatti (Gf) utilizzando il modello
    predicted = model.predict(giocatore_data_normalized)

    print("Prevista quantità di Gf:", predicted[0][0])
else:
    print("Giocatore non trovato nel dataset.")


