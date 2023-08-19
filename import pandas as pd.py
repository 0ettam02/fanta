import pandas as pd 

dataset1 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea.csv", sep=",")
dataset2 = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea2022_23.csv", sep=",")

print(dataset1.head())
print(dataset2.head())

lunghezza = max(dataset1.shape[0], dataset2.shape[0])

for i in range(lunghezza):
    if dataset1["Nome"][i] in dataset2["Nome"].values:
        print(f"il giocatore {dataset1['Nome'][i]} esiste")


for i in range(lunghezza):
    if dataset1["Nome"][i] in dataset2["Nome"].values:
        print(f"il giocatore {dataset1['Nome'][i]} esiste")


if dataset1['Gs'][1] > dataset2['Gs'][1]:
    print('Serie A')
else:
    print(f"ha subito {dataset2['Gs']}")

