import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedStyle

# Carica il dataset da un file CSV
dataset = pd.read_csv("C:\\Users\\aruta\\OneDrive\\Desktop\\app_fanta\\seriea.csv", sep=",")

def is_entry_empty(entry_widget):
    return entry_widget.get().strip() == ""

def show_info_popup():
    info_text = "Ricorda che puoi omettere alcuni attributi per ricevere solo alcuni specifici ruoli."
    messagebox.showinfo("Informazione", info_text)

def calcola_squadra():
    if is_entry_empty(soglia_minimo_entry):
        soglia_voto_minimo = 0.0
    else:
        soglia_voto_minimo = float(soglia_minimo_entry.get())

    if is_entry_empty(soglia_massimo_entry):
        soglia_voto_massimo = float('inf')
    else:
        soglia_voto_massimo = float(soglia_massimo_entry.get())

    if is_entry_empty(soglia_ass_entry):
        soglia_assist_minimo = 0.0
    else:
        soglia_assist_minimo = float(soglia_ass_entry.get())

    if is_entry_empty(soglia_rigori_minimi_segnati_entry):
        soglia_rigori_minimi_segnati = 0.0
    else:
        soglia_rigori_minimi_segnati = float(soglia_rigori_minimi_segnati_entry.get())

    if is_entry_empty(soglia_rp_minimi_parati_entry):
        soglia_rp_minimi_parati = 0.0
    else:
        soglia_rp_minimi_parati = float(soglia_rp_minimi_parati_entry.get())

    if is_entry_empty(soglia_rc_minimi_calciati_entry):
        soglia_rc_minimi_calciati = 0.0
    else:
        soglia_rc_minimi_calciati = float(soglia_rc_minimi_calciati_entry.get())

    if is_entry_empty(soglia_r_errati_max_entry):
        soglia_r_errati_max = float('inf')
    else:
        soglia_r_errati_max = float(soglia_r_errati_max_entry.get())

    if is_entry_empty(soglia_amm_max_entry):
        soglia_amm_max = float('inf')
    else:
        soglia_amm_max = float(soglia_amm_max_entry.get())

    if is_entry_empty(soglia_esp_max_entry):
        soglia_esp_max = float('inf')
    else:
        soglia_esp_max = float(soglia_esp_max_entry.get())

    if is_entry_empty(soglia_au_max_entry):
        soglia_au_max = float('inf')
    else:
        soglia_au_max = float(soglia_au_max_entry.get())

    portieri_selezionati = dataset[
        (dataset['Mv'] >= soglia_voto_minimo) & (dataset['Mv'] < soglia_voto_massimo) & (dataset['Pv'] > 10) & (dataset['R'] == 'P') &
        (dataset['Rp'] >= soglia_rp_minimi_parati) &
        (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & (dataset['Au'] <= soglia_au_max)
    ].sort_values(by='Mf', ascending=False)
    
    difensori_selezionati = dataset[
        (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) & (dataset['R'] == 'D') & (dataset['Ass'] >= soglia_assist_minimo) &
        (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R+'] >= soglia_rigori_minimi_segnati) & (dataset['R-'] <= soglia_r_errati_max) &
        (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & (dataset['Au'] <= soglia_au_max)
    ].sort_values(by='Mf', ascending=False)
    
    centrocampisti_selezionati = dataset[
        (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) & (dataset['R'] == 'C') & (dataset['Ass'] >= soglia_assist_minimo) &
        (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R+'] >= soglia_rigori_minimi_segnati) & (dataset['R-'] <= soglia_r_errati_max) &
        (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & (dataset['Au'] <= soglia_au_max)
    ].sort_values(by='Mf', ascending=False)
    
    attaccanti_selezionati = dataset[
        (dataset['Mf'] >= soglia_voto_minimo) & (dataset['Mf'] < soglia_voto_massimo) & (dataset['R'] == 'A') & (dataset['Ass'] >= soglia_assist_minimo) &
        (dataset['Rc'] >= soglia_rc_minimi_calciati) & (dataset['R+'] >= soglia_rigori_minimi_segnati) & (dataset['R-'] <= soglia_r_errati_max) &
        (dataset['Amm'] <= soglia_amm_max) & (dataset['Esp'] <= soglia_esp_max) & (dataset['Au'] <= soglia_au_max)
    ].sort_values(by='Mf', ascending=False)
    
    portieri_finali = portieri_selezionati.head(3)
    difensori_finali = difensori_selezionati.head(8)
    centrocampisti_finali = centrocampisti_selezionati.head(8)
    attaccanti_finali = attaccanti_selezionati.head(6)

    squadra_fantacalcio = pd.concat([portieri_finali, difensori_finali, centrocampisti_finali, attaccanti_finali])

    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, squadra_fantacalcio.to_string(index=False))
    apply_alternating_row_colors()
    result_text.config(state="disabled")
    adjust_result_text_width()

def apply_alternating_row_colors():
    content = result_text.get("1.0", "end-1c").strip().split("\n")

    result_text.config(state="normal")
    result_text.delete(1.0, tk.END)

    for index, line in enumerate(content):
        if index % 2 == 0:
            result_text.insert(tk.END, line + '\n', 'evenrow')
        else:
            result_text.insert(tk.END, line + '\n', 'oddrow')

    result_text.config(state="disabled")

def adjust_result_text_width():
    result_text.update_idletasks()
    max_line_length = max(len(line) for line in result_text.get(1.0, tk.END).splitlines())
    result_text.config(width=max_line_length)

root = tk.Tk()
root.title("Fantacalcio Squadra")
style = ThemedStyle(root)
style.set_theme("arc")

# Organizza le entry in due colonne per riga
soglia_minimo_entry = ttk.Entry(root)
soglia_massimo_entry = ttk.Entry(root)
soglia_ass_entry = ttk.Entry(root)
soglia_rigori_minimi_segnati_entry = ttk.Entry(root)
soglia_rp_minimi_parati_entry = ttk.Entry(root)
soglia_rc_minimi_calciati_entry = ttk.Entry(root)
soglia_r_errati_max_entry = ttk.Entry(root)
soglia_amm_max_entry = ttk.Entry(root)
soglia_esp_max_entry = ttk.Entry(root)
soglia_au_max_entry = ttk.Entry(root)

widgets = [
    (ttk.Label(root, text="Inserisci la soglia di voto minima:"), soglia_minimo_entry),
    (ttk.Label(root, text="Inserisci la soglia di voto massima:"), soglia_massimo_entry),
    (ttk.Label(root, text="Inserisci la soglia di ass minima:"), soglia_ass_entry),
    (ttk.Label(root, text="Inserisci la soglia di rigori minimi segnati:"), soglia_rigori_minimi_segnati_entry),
    (ttk.Label(root, text="Inserisci la soglia di rigori parati minima:"), soglia_rp_minimi_parati_entry),
    (ttk.Label(root, text="Inserisci la soglia di rigori calciati minima:"), soglia_rc_minimi_calciati_entry),
    (ttk.Label(root, text="Inserisci la soglia di rigori sbagliati massimi:"), soglia_r_errati_max_entry),
    (ttk.Label(root, text="Inserisci la soglia di ammunizioni massime:"), soglia_amm_max_entry),
    (ttk.Label(root, text="Inserisci la soglia di espulsioni massime:"), soglia_esp_max_entry),
    (ttk.Label(root, text="Inserisci la soglia di autogol massimi:"), soglia_au_max_entry)
]

for row, (label, entry) in enumerate(widgets):
    label.grid(row=row, column=0, padx=5, pady=5, sticky="w")
    entry.grid(row=row, column=1, padx=5, pady=5)

calculate_button = ttk.Button(root, text="Calcola Squadra", command=calcola_squadra)
calculate_button.grid(row=len(widgets), columnspan=2, pady=10)

info_button = ttk.Button(root, text="Info", command=show_info_popup)
info_button.grid(row=len(widgets) + 1, columnspan=2, pady=5)

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, relief="groove", state="disabled", fg="gray")
result_text.tag_configure('evenrow', background="#f0f0f0")
result_text.tag_configure('oddrow', background="white")
result_text.grid(row=len(widgets) + 2, columnspan=2, sticky="news")

root.grid_rowconfigure(len(widgets) + 2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()