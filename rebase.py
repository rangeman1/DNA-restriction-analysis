import tkinter as tk
from tkinter import filedialog, messagebox
from Bio import SeqIO
from Bio.Restriction import *

def load_and_analyze():
    input_path = filedialog.askopenfilename(
        title="Wybierz plik FASTA",
        filetypes=[("FASTA files", "*.fasta *.fa *.fna"), ("All files", "*.*")]
    )
    
    if not input_path:
        return

    output_path = filedialog.asksaveasfilename(
        title="Zapisz wynik jako",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not output_path:
        return

    try:
        record = SeqIO.read(input_path, "fasta")
        dna_sequence = record.seq

        enzymes = CommOnly
        analysis = RestrictionBatch(enzymes)
        result = analysis.search(dna_sequence)

        with open(output_path, "w") as f:
            f.write(f"Plik wejściowy: {input_path}\n")
            f.write(f"Długość sekwencji: {len(dna_sequence)}\n\n")
            f.write("Miejsca cięcia:\n\n")

            for enzyme, cuts in result.items():
                if cuts:
                    f.write(f"{enzyme}: {cuts}\n")

        messagebox.showinfo("Sukces", "Wynik zapisany do pliku!")

    except Exception as e:
        messagebox.showerror("Błąd", str(e))

# GUI
root = tk.Tk()
root.title("Analiza restrykcyjna DNA (zapis do pliku)")

frame = tk.Frame(root)
frame.pack(pady=10)

load_button = tk.Button(frame, text="Wczytaj FASTA i zapisz wynik", command=load_and_analyze)
load_button.pack()

root.mainloop()
