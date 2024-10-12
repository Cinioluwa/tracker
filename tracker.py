import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# Initialize bonus tracking (this would normally be loaded from the file)
user_data = {}

# Excel file path
excel_file = "user_progress.xlsx"

# Check if the file exists; if not, create it with appropriate headers
if not os.path.exists(excel_file):
    df = pd.DataFrame(columns=['User', 'Week', 'Learning Points', 'Bonus', 'Application Points', 'Certificate Points',
                               'Total Eval Points'])
    df.to_excel(excel_file, index=False)


def update_excel(user, week, learning_points, bonus, application_points, certificate_points, total_eval_points):
    # Load the existing Excel file
    df = pd.read_excel(excel_file)

    # Create a new DataFrame with the new data, ensuring non-null values
    new_data = pd.DataFrame({
        'User': [user],
        'Week': [week],
        'Learning Points': [learning_points],
        'Bonus': [bonus],
        'Application Points': [application_points],
        'Certificate Points': [certificate_points],
        'Total Eval Points': [total_eval_points]
    })

    # Ensure the dtypes of new_data match the existing DataFrame
    for col in df.columns:
        new_data[col] = new_data[col].astype(df[col].dtype)

    # Concatenate the existing DataFrame with the new data
    df = pd.concat([df, new_data], ignore_index=True)

    # Save back to the Excel file
    df.to_excel(excel_file, index=False)


def calculate_points():
    global user_data

    user = user_entry.get()
    week = int(week_entry.get())
    learning_hours = float(learning_entry.get())
    application_hours = float(application_entry.get())
    certificates = int(certificate_entry.get())

    # Get or initialize user data
    if user not in user_data:
        user_data[user] = {"bonus": 0, "last_week_points": 0}

    # Fetch user's last week bonus
    bonus = user_data[user]["bonus"]

    # Calculate learning points
    decay_rate = 0.9
    learning_points = (learning_hours ** 0.8) * 100 * decay_rate

    # Apply bonus from previous weeks
    learning_points += bonus * 0.02  # 2% bonus from previous week

    # Application points
    application_points = (application_hours ** 0.9) * 120

    # Certificate points
    certificate_points = (500 / (certificates + 1)) ** 0.5

    # Total eval points
    total_eval_points = learning_points + application_points + certificate_points

    # Update bonus (if no learning, apply decay)
    if learning_hours == 0:
        bonus *= 0.9  # Decay by 10%
    else:
        bonus = learning_points

    # Update user data for tracking
    user_data[user]["bonus"] = bonus
    user_data[user]["last_week_points"] = total_eval_points

    # Update the Excel file with current week's data
    update_excel(user, week, learning_points, bonus, application_points, certificate_points, total_eval_points)

    # Show result in messagebox
    messagebox.showinfo("Result", f"User: {user}\nTotal Eval Points: {total_eval_points:.3f}")


# GUI
root = tk.Tk()
root.title("Learning Progress Tracker")

tk.Label(root, text="User").grid(row=0, column=0)
tk.Label(root, text="Week").grid(row=1, column=0)
tk.Label(root, text="Learning Hours").grid(row=2, column=0)
tk.Label(root, text="Application Hours").grid(row=3, column=0)
tk.Label(root, text="Certificates").grid(row=4, column=0)

user_entry = tk.Entry(root)
week_entry = tk.Entry(root)
learning_entry = tk.Entry(root)
application_entry = tk.Entry(root)
certificate_entry = tk.Entry(root)

user_entry.grid(row=0, column=1)
week_entry.grid(row=1, column=1)
learning_entry.grid(row=2, column=1)
application_entry.grid(row=3, column=1)
certificate_entry.grid(row=4, column=1)

calculate_button = tk.Button(root, text="Calculate", command=calculate_points)
calculate_button.grid(row=5, column=1)

root.mainloop()
