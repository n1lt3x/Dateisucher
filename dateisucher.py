import os
import tkinter as tk
from tkinter import filedialog

class DateisucherGUI:
    def __init__(self, master):
        self.master = master
        master.title("Erweiterter Dateisucher")

        self._verzeichnis_label = tk.Label(master, text="Verzeichnis:")
        self._verzeichnis_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self._verzeichnis_entry = tk.Entry(master, width=50)
        self._verzeichnis_entry.grid(row=0, column=1, padx=5, pady=5)

        self._verzeichnis_button = tk.Button(master, text="Verzeichnis wählen", command=self._verzeichnis_auswahl)
        self._verzeichnis_button.grid(row=0, column=2, padx=5, pady=5)

        self._suchbegriff_label = tk.Label(master, text="Suchbegriff:")
        self._suchbegriff_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self._suchbegriff_entry = tk.Entry(master, width=20)
        self._suchbegriff_entry.grid(row=1, column=1, padx=5, pady=5)

        self._suche_button = tk.Button(master, text="Suche", command=self._suche_button_click)
        self._suche_button.grid(row=1, column=2, padx=5, pady=5)

        self._ergebnis_label = tk.Label(master, text="Gefundene Dateien:")
        self._ergebnis_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Erstelle ein Text-Widget für das Suchergebnis
        self._ergebnis_text = tk.Text(master, wrap="word", width=50, height=10)
        self._ergebnis_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        self._ergebnis_text.tag_configure("highlight", background="yellow")

    def suche_dateien(self, verzeichnis, suchbegriff):
        gefunden_dateien = []
        for root, dirs, files in os.walk(verzeichnis):
            for datei in files:
                if suchbegriff in datei:
                    gefunden_dateien.append(os.path.join(root, datei))
        return gefunden_dateien

    def _suche_button_click(self):
        verzeichnis = self._verzeichnis_entry.get()
        suchbegriff = self._suchbegriff_entry.get()

        gefundene_dateien = self.suche_dateien(verzeichnis, suchbegriff)

        if gefundene_dateien:
            gefundene_dateien.sort()  # Sortiere das Suchergebnis vor dem Anzeigen
            self._ergebnis_text.delete(1.0, tk.END)
            for datei in gefundene_dateien:
                self._ergebnis_text.insert(tk.END, datei + '\n')
            self.markiere_woerter(suchbegriff)
        else:
            self._ergebnis_text.delete(1.0, tk.END)
            self._ergebnis_text.insert(tk.END, "Keine Dateien gefunden, die den Suchbegriff enthalten.")

    def markiere_woerter(self, suchbegriff):
        start = "1.0"
        while True:
            position = self._ergebnis_text.search(suchbegriff, start, tk.END)
            if not position:
                break
            end = f"{position}+{len(suchbegriff)}c"
            self._ergebnis_text.tag_add("highlight", position, end)
            start = end

    def _verzeichnis_auswahl(self):
        verzeichnis = filedialog.askdirectory()
        self._verzeichnis_entry.delete(0, tk.END)
        self._verzeichnis_entry.insert(0, verzeichnis)

class AngepassterDateisucherGUI(DateisucherGUI):
    def suche_dateien(self, verzeichnis, suchbegriff):
        gefunden_dateien = super().suche_dateien(verzeichnis, suchbegriff)
        # Fügen Sie hier zusätzliche Anpassungen oder Filter hinzu, falls erforderlich
        return gefunden_dateien

def main():
    root = tk.Tk()
    app = DateisucherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
