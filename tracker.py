import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os
from typing import Dict, Any

class LearningProgressTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Learning Progress Tracker")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.user_data: Dict[str, Dict[str, Any]] = {}
        self.excel_file = "user_progress.xlsx"
        self.initialize_excel()

        self.create_widgets()

    def initialize_excel(self):
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=['User', 'Week', 'Learning Points', 'Bonus', 'Application Points', 'Certificate Points', 'Total Eval Points'])
            df.to_excel(self.excel_file, index=False)

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        labels = ["User", "Week", "Learning Hours", "Application Hours", "Certificates"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            self.entries[label] = ttk.Entry(main_frame, width=30)
            self.entries[label].grid(row=i, column=1, sticky=tk.W, pady=5)

        calculate_button = ttk.Button(main_frame, text="Calculate", command=self.calculate_points)
        calculate_button.grid(row=len(labels), column=1, sticky=tk.E, pady=10)

        view_history_button = ttk.Button(main_frame, text="View History", command=self.view_history)
        view_history_button.grid(row=len(labels)+1, column=1, sticky=tk.E, pady=10)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate", maximum=1000, variable=self.progress_var)
        self.progress_bar.grid(row=len(labels)+2, column=0, columnspan=2, pady=10)

    def update_excel(self, user, week, learning_points, bonus, application_points, certificate_points, total_eval_points):
        df = pd.read_excel(self.excel_file)
        new_data = pd.DataFrame({
            'User': [user], 'Week': [week], 'Learning Points': [learning_points],
            'Bonus': [bonus], 'Application Points': [application_points],
            'Certificate Points': [certificate_points], 'Total Eval Points': [total_eval_points]
        })
        for col in df.columns:
            new_data[col] = new_data[col].astype(df[col].dtype)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(self.excel_file, index=False)

    def calculate_points(self):
        try:
            user = self.entries["User"].get()
            week = int(self.entries["Week"].get())
            learning_hours = float(self.entries["Learning Hours"].get())
            application_hours = float(self.entries["Application Hours"].get())
            certificates = int(self.entries["Certificates"].get())

            if user not in self.user_data:
                self.user_data[user] = {"bonus": 0, "last_week_points": 0}

            bonus = self.user_data[user]["bonus"]
            decay_rate = 0.9
            learning_points = (learning_hours ** 0.8) * 100 * decay_rate
            learning_points += bonus * 0.02
            application_points = (application_hours ** 0.9) * 120
            certificate_points = (500 / (certificates + 1)) ** 0.5
            total_eval_points = learning_points + application_points + certificate_points

            bonus = learning_points if learning_hours > 0 else bonus * 0.9

            # Round all points to whole numbers for clarity
            learning_points = round(learning_points)
            application_points = round(application_points)
            certificate_points = round(certificate_points)
            total_eval_points = round(total_eval_points)
            bonus = round(bonus)

            self.user_data[user]["bonus"] = bonus
            self.user_data[user]["last_week_points"] = total_eval_points

            self.update_excel(user, week, learning_points, bonus, application_points, certificate_points, total_eval_points)

            # Determine performance feedback
            if total_eval_points >= 800:
                performance_feedback = "Excellent"
            elif total_eval_points >= 600:
                performance_feedback = "Good"
            elif total_eval_points >= 400:
                performance_feedback = "Average"
            else:
                performance_feedback = "Needs Improvement"

            # Update the progress bar (scale to a max of 1000 points)
            self.progress_var.set(min(total_eval_points, 1000))  # Cap at 1000 for the scale

            messagebox.showinfo(
                "Result",
                f"User: {user}\n"
                f"Week: {week}\n\n"
                f"Learning Points: {learning_points}\n"
                f"Application Points: {application_points}\n"
                f"Certificate Points: {certificate_points}\n"
                f"---------------------------\n"
                f"Total Evaluation Points: {total_eval_points}\n"
                f"Performance: {performance_feedback}\n"
                f"Bonus for Next Week: {bonus}"
            )
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for all fields.")

    def view_history(self):
        user = self.entries["User"].get()
        if not user:
            messagebox.showerror("Error", "Please enter a username to view history.")
            return

        df = pd.read_excel(self.excel_file)
        user_data = df[df['User'] == user]

        if user_data.empty:
            messagebox.showinfo("History", f"No history found for user: {user}")
        else:
            history_window = tk.Toplevel(self.master)
            history_window.title(f"History for {user}")
            history_window.geometry("600x400")

            tree = ttk.Treeview(history_window, columns=list(df.columns), show='headings')
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for _, row in user_data.iterrows():
                tree.insert("", "end", values=list(row))

            tree.pack(expand=True, fill='both')

            scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
            scrollbar.pack(side='right', fill='y')
            tree.configure(yscrollcommand=scrollbar.set)

if __name__ == "__main__":
    root = tk.Tk()
    app = LearningProgressTracker(root)
    root.mainloop()