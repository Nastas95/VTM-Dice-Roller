#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
from random import randint

class DiceRoller:
    def __init__(self, root):
        self.root = root
        self.root.title("VTM Dice Roller")
        self.root.geometry("400x410")
        self.root.configure(bg="#2E2E2E")

        # Stile
        self.title_font = ("Times New Roman", 18, "bold")
        self.label_font = ("Times New Roman", 12)
        self.button_font = ("Times New Roman", 12, "bold")
        self.result_font = ("Times New Roman", 12, "bold")

        # Titolo
        tk.Label(root, text="VTM Dice Roller",
                 font=self.title_font, bg="#2E2E2E", fg="#FF4500").pack(pady=10)

        self.frame = tk.Frame(root, bg="#2E2E2E")
        self.frame.pack(padx=20, pady=20)

        # N° Dadi - Testo grigio chiaro
        tk.Label(self.frame, text="N° Dadi:",
                 font=self.label_font, bg="#2E2E2E", fg="#CCCCCC").grid(row=0, column=0, padx=5, pady=5)
        self.dadi_var = tk.IntVar(value=1)
        self.dadi_spin = tk.Spinbox(self.frame, from_=0, to=20, width=5,
                                   textvariable=self.dadi_var, font=self.label_font)
        self.dadi_spin.grid(row=0, column=1, padx=5, pady=5)

        # Difficoltà - Testo grigio chiaro
        tk.Label(self.frame, text="Difficoltà:",
                  font=self.label_font, bg="#2E2E2E", fg="#CCCCCC").grid(row=1, column=0, padx=5, pady=5)
        self.difficolta = tk.IntVar(value=6)
        self.diff_menu = tk.OptionMenu(self.frame, self.difficolta,
                                      *range(2, 10))
        self.diff_menu.config(font=self.label_font, bg="#5A5A5A", fg="#CCCCCC")
        self.diff_menu.grid(row=1, column=1, padx=5, pady=5)

        # Specializzazione - Testo grigio chiaro
        self.specializzazione = tk.BooleanVar()
        tk.Checkbutton(self.frame, text="Specializzazione",
                       variable=self.specializzazione,
                      font=self.label_font, bg="#2E2E2E", fg="#CCCCCC",
                      selectcolor="#5A5A5A").grid(row=2, columnspan=2, pady=10)

        # Pulsante - Arancione più opaco
        self.roll_btn = tk.Button(root, text="Lancia i Dadi",
                                 command=self.roll_dice,
                                  font=self.button_font,
                                 bg="#FFA500", fg="#000000")
        self.roll_btn.pack(pady=10)

        # Risultati
        self.result_frame = tk.Frame(root, bg="#2E2E2E")
        self.result_frame.pack(padx=20, pady=20)
        self.result_text = tk.Text(self.result_frame,
                                  width=40, height=10,
                                  bg="#2E2E2E", fg="#CCCCCC",
                                  font=self.result_font,
                                  bd=0, highlightthickness=0)
        self.result_text.pack()

        # Tag colori
        self.result_text.tag_config("yellow", foreground="#CCCC00")   # Giallo opaco
        self.result_text.tag_config("green", foreground="#32CD32")    # Verde chiaro
        self.result_text.tag_config("red", foreground="#CD5C5C")      # Rosso chiaro
        self.result_text.tag_config("bold_red", foreground="#CD5C5C", font=("Times New Roman", 12, "bold"))
        self.result_text.tag_config("bold_green", foreground="#32CD32", font=("Times New Roman", 12, "bold"))

    def validate_input(self):
        try:
            num_dice = self.dadi_var.get()
            diff = self.difficolta.get()
            if num_dice < 0:
                raise ValueError("Numero di dadi non può essere negativo")
            return num_dice, diff
        except Exception as e:
            messagebox.showerror("Errore", str(e))
            return None

    def roll_dice(self):
        self.result_text.delete(1.0, tk.END)
        validation = self.validate_input()
        if not validation:
            return
        num_dice, diff = validation
        dice = [randint(1, 10) for _ in range(num_dice)]
        successes = 0
        ones = 0
        tens = 0

        for die in dice:
            if die == 1:
                ones += 1
            if die >= diff:
                successes += 1
                if die == 10 and self.specializzazione.get():
                    tens += 1

        total_successes = successes + tens

        # Risultato
        result_type = ""
        if total_successes == 0:
            if ones > 0:
                result_type = "Fallimento Critico!"
                tag = "bold_red"
            else:
                result_type = "Fallimento"
                tag = "bold_red"
        else:
            result_type = f"{total_successes} Successi"
            tag = "green"

        # Formattazione risultati
        self.result_text.insert(tk.END, f"Dadi lanciati: ", "yellow")
        self.result_text.insert(tk.END, f"{num_dice} \n", "bold_green")

        for die in dice:
            if die >= diff:
                self.result_text.insert(tk.END, f"{die} ", "green")
            else:
                self.result_text.insert(tk.END, f"{die} ", "red")
        self.result_text.insert(tk.END, "\n\n")

        # Successi Critici
        if self.specializzazione.get() and tens > 0:
            self.result_text.insert(tk.END, "Successi critici: ", "yellow")
            self.result_text.insert(tk.END, f"{tens} \n", "bold_green")
        self.result_text.insert(tk.END, "Risultato: ", "yellow")
        self.result_text.insert(tk.END, f"{result_type}\n", tag)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRoller(root)
    root.mainloop()
