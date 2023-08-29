import tkinter as tk
from tkinter import messagebox
from scrap import Scrap
from tkinter import ttk
import pandas as pd
from check_data import check_data
from tkinter import filedialog
import shutil
import plotly.express as px
import os
from tkcalendar import DateEntry
import time


def formatting_data():
    path = os.path.join('data_files','rafed_data.csv')
    df = pd.read_csv(path)
    df['تاريخ الوفاة ميلادي'] = pd.to_datetime(df['تاريخ الوفاة ميلادي'])

    return df

def filter_excel(sdate,edate,col):
    df = formatting_data()
    if sdate == '':
        sdate = formatting_data()['تاريخ الوفاة ميلادي'].min()
    if edate == '':
        edate = formatting_data()['تاريخ الوفاة ميلادي'].max()
    return df[df[col].between(sdate,edate,inclusive='both')]
    
def chart_pie(sdate,edate,col,title):
    df = formatting_data()
    if sdate == '':
        sdate = formatting_data()['تاريخ الوفاة ميلادي'].min()
    if edate == '':
        edate = formatting_data()['تاريخ الوفاة ميلادي'].max()
    specific_date=df[df['تاريخ الوفاة ميلادي'].between(sdate,edate)]
    subset = specific_date[col].value_counts()
    fg = px.pie(subset,values=subset.values,title= f'{subset.values} {title}',names=subset.index)
    fg.show()


def rm_files():
    try:
        shutil.rmtree('data_files')
    except OSError:
        print('no folder found')

def scrape_data():
    # Simulate a time-consuming task
    time.sleep(5)
    print("Scraping complete")
def scrape_website():
    rm_files()
    url = 'https://www.muasah.org.sa/rafed/'
    username = username_entry.get()
    password = password_entry.get()
    try:
        os.mkdir('data_files')
        scrap = Scrap(url, username, password)
        
        msg = messagebox.showinfo("success", "تمت العملية بنجاح!")
        if msg:
            username_entry.delete(0, tk.END)  # Clear username entry
            password_entry.delete(0, tk.END)  # Clear password entry
           
    except Exception as e:
        messagebox.showerror("Error", str(e))
def run_center_chart():
    start_date = sdate_entry.get()
    end_date = edate_entry.get()
    chart_pie(start_date,end_date,'إسم المغسلة','نسبة غسل الوفيات في المراكز')
def run_sex_chart():
    start_date = sdate_entry.get()
    end_date = edate_entry.get()
    chart_pie(start_date,end_date,'النوع','نسبة الوفاة بين الذكور والإناث')
def run_cleaner_chart():
    start_date = sdate_entry.get()
    end_date = edate_entry.get()
    chart_pie(start_date,end_date,'المغسل','نسبة غسل الوفيات في المراكز')
def show_table():
    try:
        # Clear existing data
        tree.delete(*tree.get_children())
        path = os.path.join('data_files','rafed_data.csv')
        # Read the CSV file
        df = pd.read_csv(path)
        # Insert data into the treeview
        for i, row in enumerate(df.itertuples(), start=1):
            values = [str(row[j]) for j in range(1, len(columns) + 1)]
            tree.insert("", "end", iid=i, values=values)
    except FileNotFoundError:
        messagebox.showerror("لا يوجد ملف", "البيانات غير متوفرة.")
def export_excel():
    start_date = sdate_entry.get()
    end_date = edate_entry.get()
    df = filter_excel(start_date,end_date,'تاريخ الوفاة ميلادي')
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
    # Save the workbook to the selected file location
    if file_path:
    # Save the DataFrame to the selected file location
        df.to_excel(file_path, index=False)
# Create the main window
root = tk.Tk()

root.title("أداة استيراد البيانات من الموقع")
root.geometry("800x600")
style = ttk.Style()
style.configure("Treeview",
                background="#D3D3D3",
                foreground="black",
                rowheight=25,
                fieldbackground="#D3D3D3")
style.configure("TWindow",
                background="#ECECEC")
style.configure("TLabel",
                background="#ECECEC",
                foreground="#333333",
                font=("Helvetica", 13))
style.configure("TEntry",
                fieldbackground="#F0F0F0",
                font=("Helvetica", 13),
                )
style.configure("TButton",
                background="#5B9A8B",  # Green background
                foreground="#252B48",  # White text color
                font=("Helvetica", 14),
                padding=10)
username_label = ttk.Label(root, text=":اسم المستخدم", style="TLabel")
username_label.grid(row=1, column=1, padx=10, pady=5, sticky="s")
password_label = ttk.Label(root, text=":كلمة المرور", style="TLabel")
password_label.grid(row=2, column=1, padx=10, pady=5, sticky="s")
username_entry = ttk.Entry(root, style="TEntry")
username_entry.grid(row=1, column=0, padx=10, pady=5,sticky='e')
password_entry = ttk.Entry(root, show="*", style="TEntry")
password_entry.grid(row=2, column=0, padx=10, pady=5,sticky='e')
sdate_label = ttk.Label(root, text="تاريخ البداية", style="TLabel")
sdate_label.grid(row=7, column=3, padx=10, pady=5, sticky="s")
sdate_entry = DateEntry(root, style="TEntry",year=2023,month=1,day=1)
sdate_entry.grid(row=7, column=2, padx=10, pady=5,sticky='e')
edate_label = ttk.Label(root, text="تاريخ النهاية", style="TLabel")
edate_label.grid(row=7, column=1, padx=10, pady=5, sticky="s")
edate_entry = DateEntry(root, style="TEntry")
edate_entry.grid(row=7, column=0, padx=10, pady=5,sticky='e')
# Create and position the scrape button
scrape_button = ttk.Button(root, text="استيراد", command=scrape_website, style="TButton")
scrape_button.grid(row=4, column=0, padx=10, pady=10)

check_button = ttk.Button(root,text='فحص الأخطاء',command=check_data)
check_button.grid(row=4, column=1, padx=10, pady=10)
export_button = tk.Button(root, text="تصدير إكسل", command=export_excel)
export_button.grid(row=6,column=1,padx=10, pady=10)
sex_button = ttk.Button(root, text="الجنسين", command=run_sex_chart, style="TButton")
sex_button.grid(row=8, column=0, padx=10, pady=10,sticky='e')
centers_button = ttk.Button(root, text="المراكز", command=run_center_chart, style="TButton")
centers_button.grid(row=8, column=1, padx=10, pady=10,sticky='e')
cleaners_button = ttk.Button(root, text="المغسلين", command=run_cleaner_chart, style="TButton")
cleaners_button.grid(row=8, column=2, padx=10, pady=10,sticky='s')

# Create a Treeview widget
columns = [
    "الرقم",
    "الاسم",
    "الجنس"
]
tree = ttk.Treeview(root, columns=columns, show="headings", style="Treeview")

# Configure the Treeview columns
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='center')

# Create a scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

# Create a button to show the table
show_button = ttk.Button(root, text="عرض المتوفين", command=show_table, style="TButton")

# Grid layout
tree.grid(row=5, column=0,columnspan=4, padx=10, pady=10, sticky="nsew")
scrollbar.grid(row=5, column=4, columnspan=4,padx=(0, 10), pady=10, sticky="ns")
show_button.grid(row=6, column=0,columnspan=2,padx=10, pady=10)

# Configure the grid weights
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)

# Start the main loop
root.mainloop()