import tkinter as tk
from tkinter import messagebox
from random import randint
import webbrowser
from PIL import Image, ImageTk

class PerfectGuessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Perfect Guess Game")
        self.root.geometry("400x500")  # Adjusted height for image display
        self.root.configure(bg="#282C34")  # Dark background for attractiveness

        self.show_intro_screen()

    def show_intro_screen(self):
        # Intro screen elements
        self.intro_frame = tk.Frame(self.root, bg="#282C34")
        self.intro_frame.pack(fill=tk.BOTH, expand=True)

        # Load and display the image
        self.load_image()

        # Place the image directly on the frame
        self.image_label = tk.Label(self.intro_frame, image=self.img_tk, bg="#282C34")
        self.image_label.pack(pady=20)

        intro_label = tk.Label(self.intro_frame, text="Welcome to Perfect Guess Game!", font=("Impact", 16,), fg="white", bg="#282C34")
        intro_label.pack(pady=20)

        author_label = tk.Label(self.intro_frame, text="Created by: Muhammad Shahzaib", font=("Consolas", 15,), fg="red", bg="#282C34")
        author_label.pack(pady=10)

        info_label = tk.Label(self.intro_frame, text="Guess the number in the fewest attempts to win!", font=("Consolas", 11,), fg="lightblue", bg="#282C34")
        info_label.pack(pady=20)

        start_button = tk.Button(self.intro_frame, text="Start Game", command=self.start_game, bg="#4CAF50", fg="white", font=("Impact", 14,))
        start_button.pack(pady=20)

    def load_image(self):
        # Load the image
        self.img = Image.open("PROFILE PIC.png")  # Replace with your image file
        self.img = self.img.resize((200, 200))  # Resize image to fit
        self.img_tk = ImageTk.PhotoImage(self.img)

    def start_game(self):
        self.intro_frame.destroy()  # Remove intro screen
        self.setup_game_screen()  # Show game screen

    def setup_game_screen(self):
        self.high_score = self.load_high_score()

        # GUI Elements
        self.range_label = tk.Label(self.root, text="Enter the range for guessing:", font=("Impact", 14,), fg="white", bg="#282C34")
        self.range_label.pack(pady=10)

        self.starting_point_label = tk.Label(self.root, text="Starting Point:", font=("Consolas", 12,), fg="white", bg="#282C34")
        self.starting_point_label.pack()

        self.starting_point_entry = tk.Entry(self.root, font=("Impact", 12,))
        self.starting_point_entry.pack()

        self.ending_point_label = tk.Label(self.root, text="Ending Point:", font=("Consolas", 12,), fg="white", bg="#282C34")
        self.ending_point_label.pack()

        self.ending_point_entry = tk.Entry(self.root, font=("Impact", 12,))
        self.ending_point_entry.pack()

        self.submit_range_button = tk.Button(self.root, text="Submit Range", command=self.set_range, bg="#4CAF50", fg="white", font=("Impact", 12,))
        self.submit_range_button.pack(pady=10)

        self.label = tk.Label(self.root, text="", font=("Impact", 14,), fg="yellow", bg="#282C34")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root, font=("Impact", 14,))
        self.entry.pack(pady=10)

        # Updated Font Colors
        self.guess_button = tk.Button(self.root, text="Guess", command=self.check_guess, bg="#2196F3", fg="black", font=("Impact", 12,), state=tk.DISABLED)
        self.guess_button.pack(pady=10)

        self.reset_button = tk.Button(self.root, text="Play Again", command=self.confirm_reset, bg="#F44336", fg="black", font=("Impact", 12,), state=tk.DISABLED)
        self.reset_button.pack(pady=10)

    def set_range(self):
        try:
            self.starting_point = int(self.starting_point_entry.get())
            self.ending_point = int(self.ending_point_entry.get())
            if self.starting_point >= self.ending_point:
                raise ValueError("Starting point must be less than ending point.")
            self.number = randint(self.starting_point, self.ending_point)
            self.attempts = 0
            self.label.config(text=f"Guess the number between {self.starting_point} and {self.ending_point}")
            self.guess_button.config(state=tk.NORMAL)
            self.starting_point_entry.config(state=tk.DISABLED)
            self.ending_point_entry.config(state=tk.DISABLED)
            self.submit_range_button.config(state=tk.DISABLED)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid range: {e}")

    def check_guess(self):
        try:
            guessed_number = int(self.entry.get())
            self.attempts += 1

            if guessed_number > self.number:
                messagebox.showinfo("Hint", "Lower Number Please!")
            elif guessed_number < self.number:
                messagebox.showinfo("Hint", "Greater Number Please!")
            else:
                messagebox.showinfo("Congratulations", f"You guessed the number {guessed_number} in {self.attempts} attempts!")
                self.update_high_score(self.attempts)
                self.show_prize_popup()
                self.guess_button.config(state=tk.DISABLED)
                self.reset_button.config(state=tk.NORMAL)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def show_prize_popup(self):
        claim_window = tk.Toplevel(self.root)
        claim_window.title("You Won Prize!")
        claim_window.geometry("300x150")
        claim_window.configure(bg="#282C34")  # Dark background for popup

        label = tk.Label(claim_window, text="Congratulations! You won $1!\nClick below to claim your prize!", font=("Impact", 10,), fg="yellow", bg="#282C34")
        label.pack(pady=10)

        claim_button = tk.Button(claim_window, text="Claim Prize", command=lambda: webbrowser.open("https://dollarkamaowithme.blogspot.com/"), bg="#4CAF50", fg="white", font=("Impact", 10,))
        claim_button.pack(pady=10)

    def confirm_reset(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to restart the game?"):
            self.reset_game()

    def reset_game(self):
        # Reset the game and allow the user to set a new range
        self.starting_point_entry.config(state=tk.NORMAL)
        self.ending_point_entry.config(state=tk.NORMAL)
        self.submit_range_button.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.label.config(text="Enter the range for guessing:")
        self.guess_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return None

    def update_high_score(self, score):
        if self.high_score is None or score < self.high_score:
            self.high_score = score
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))
            messagebox.showinfo("New High Score!", f"New high score: {self.high_score} attempts!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PerfectGuessApp(root)
    root.mainloop()
