import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='passwords',
        database='BMI_Cal_Data'
    )

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            weight DOUBLE NOT NULL,
            height DOUBLE NOT NULL,
            bmi DOUBLE NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

except Error as e:
    print(f"Error: {e}")

class BMIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BMI Calculator")

        self.name_label = tk.Label(master, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(master)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.weight_label = tk.Label(master, text="Weight (kg):")
        self.weight_label.grid(row=1, column=0, padx=10, pady=10)
        self.weight_entry = tk.Entry(master)
        self.weight_entry.grid(row=1, column=1, padx=10, pady=10)

        self.height_label = tk.Label(master, text="Height (m):")
        self.height_label.grid(row=2, column=0, padx=10, pady=10)
        self.height_entry = tk.Entry(master)
        self.height_entry.grid(row=2, column=1, padx=10, pady=10)

        self.calculate_button = tk.Button(master, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.save_button = tk.Button(master, text="Save Data", command=self.save_data)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.view_history_button = tk.Button(master, text="View History", command=self.view_history)
        self.view_history_button.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = round(weight / (height ** 2), 2)
            result = f"BMI: {bmi}\nCategory: {self.get_bmi_category(bmi)}"
            self.result_label.config(text=result)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def save_data(self):
        try:
            name = self.name_entry.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = round(weight / (height ** 2), 2)

            cursor.execute('''
                INSERT INTO users (name, weight, height, bmi)
                VALUES (%s, %s, %s, %s)
            ''', (name, weight, height, bmi))

            conn.commit()
            messagebox.showinfo("Success", "Data saved successfully!")

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values.")

    def view_history(self):
        cursor.execute('''
            SELECT name, weight, height, bmi, date
            FROM users
        ''')
        data = cursor.fetchall()

        if data:
            names, weights, heights, bmis, dates = zip(*data)

            fig, ax = plt.subplots()
            ax.plot(dates, bmis, marker='o', linestyle='-', color='b')
            ax.set(xlabel='Date', ylabel='BMI',
                   title='BMI History')
            ax.grid()

            canvas = FigureCanvasTkAgg(fig, master=self.master)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=7, column=0, columnspan=2)
            canvas.draw()
        else:
            messagebox.showinfo("Info", "No data available for visualization.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()
