import tkinter as tk
from tkinter import messagebox
from random import randint

class DiceRoller:
    def __init__(self, root):
        self.root = root
        self.root.title("VTM Dice Roller")
        self.root.geometry("400x410")
        self.root.configure(bg="#2E2E2E")

        # Style configuration
        self.title_font = ("Times New Roman", 18, "bold")
        self.label_font = ("Times New Roman", 12)
        self.button_font = ("Times New Roman", 12, "bold")
        self.result_font = ("Times New Roman", 12, "bold")

        # Title label
        tk.Label(root, text="VTM Dice Roller",
                 font=self.title_font, bg="#2E2E2E", fg="#FF4500").pack(pady=10)

        # Main frame
        self.main_frame = tk.Frame(root, bg="#2E2E2E")
        self.main_frame.pack(padx=20, pady=20)

        # Dice number input
        tk.Label(self.main_frame, text="Number of Dice:",
                 font=self.label_font, bg="#2E2E2E", fg="#CCCCCC").grid(row=0, column=0, padx=5, pady=5)
        self.dice_var = tk.IntVar(value=1)
        self.dice_spin = tk.Spinbox(self.main_frame, from_=0, to=20, width=5,
                                   textvariable=self.dice_var, font=self.label_font)
        self.dice_spin.grid(row=0, column=1, padx=5, pady=5)

        # Difficulty selector
        tk.Label(self.main_frame, text="Difficulty:",
                 font=self.label_font, bg="#2E2E2E", fg="#CCCCCC").grid(row=1, column=0, padx=5, pady=5)
        self.difficulty = tk.IntVar(value=6)
        self.diff_menu = tk.OptionMenu(self.main_frame, self.difficulty, *range(2, 10))
        self.diff_menu.config(font=self.label_font, bg="#5A5A5A", fg="#CCCCCC")
        self.diff_menu.grid(row=1, column=1, padx=5, pady=5)

        # Specialization checkbox
        self.specialization = tk.BooleanVar()
        tk.Checkbutton(self.main_frame, text="Specialization",
                      variable=self.specialization,
                      font=self.label_font, bg="#2E2E2E", fg="#CCCCCC",
                      selectcolor="#5A5A5A").grid(row=2, columnspan=2, pady=10)

        # Roll button
        self.roll_btn = tk.Button(root, text="Roll Dice",
                                 command=self.roll_dice,
                                 font=self.button_font,
                                 bg="#FFA500", fg="#000000")
        self.roll_btn.pack(pady=10)

        # Results display
        self.result_frame = tk.Frame(root, bg="#2E2E2E")
        self.result_frame.pack(padx=20, pady=20)

        self.result_text = tk.Text(self.result_frame,
                                  width=40, height=10,
                                  bg="#2E2E2E", fg="#CCCCCC",
                                  font=self.result_font,
                                  bd=0, highlightthickness=0)
        self.result_text.pack()

        # Text tags configuration
        self.result_text.tag_config("yellow", foreground="#CCCC00")
        self.result_text.tag_config("green", foreground="#32CD32")
        self.result_text.tag_config("red", foreground="#CD5C5C")
        self.result_text.tag_config("bold_red", foreground="#CD5C5C", font=("Times New Roman", 12, "bold"))
        self.result_text.tag_config("bold_green", foreground="#32CD32", font=("Times New Roman", 12, "bold"))

    def validate_input(self):
        try:
            num_dice = self.dice_var.get()
            difficulty = self.difficulty.get()

            if num_dice < 0:
                raise ValueError("Number of dice cannot be negative")
            if difficulty < 2 or difficulty > 9:
                raise ValueError("Difficulty must be between 2 and 9")

            return num_dice, difficulty
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

    def roll_dice(self):
        self.result_text.delete(1.0, tk.END)
        validation = self.validate_input()
        if not validation:
            return

        num_dice, difficulty = validation
        dice = [randint(1, 10) for _ in range(num_dice)]
        successes = 0
        ones = 0
        tens = 0

        for die in dice:
            if die == 1:
                ones += 1
            if die >= difficulty:
                successes += 1
                if die == 10 and self.specialization.get():
                    tens += 1

        total_successes = (successes + tens) - ones

        # Determine result type
        if total_successes < 0:
            result = "Critical Failure!"
            tag = "bold_red"
        elif total_successes == 0:
            result = "Failure"
            tag = "red"
        else:
            result = f"{total_successes} Success(es)"
            tag = "green"

        # Format results
        self.result_text.insert(tk.END, "Dice rolled: ", "yellow")
        self.result_text.insert(tk.END, f"{num_dice}\n", "bold_green")

        for die in dice:
            self.result_text.insert(tk.END, f"{die} ", "green" if die >= difficulty else "red")
        self.result_text.insert(tk.END, "\n\n")

        if self.specialization.get() and tens > 0:
            self.result_text.insert(tk.END, "Critical successes: ", "yellow")
            self.result_text.insert(tk.END, f"{tens} (10s doubled)\n", "bold_green")

        self.result_text.insert(tk.END, "Result: ", "yellow")
        self.result_text.insert(tk.END, f"{result}\n", tag)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRoller(root)
    root.mainloop()
