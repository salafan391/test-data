import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.messagebox import showinfo
import threading
import time
from scrap import Scrap
import shutil
import os
import pandas as pd
from tkcalendar import Calendar

# def export_to_pdf(preview_data):
#     pdf_filename = "data_preview.pdf"
#     arabic_font_path = "IBMPlexSansArabic-Bold.ttf"  # Provide the path to your downloaded Arabic font
#     pdfmetrics.registerFont(TTFont("IBM Plex Sans Arabic", arabic_font_path))

#     doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

#     # Create a Table from the data
#     table_data = [['Attribute', 'Value']]
#     for key, value in preview_data.items():
#         table_data.append([key, str(value)])

#     table = Table(table_data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'IBM Plex Sans Arabic',),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     # Build PDF document
#     doc.build([table])

def search():
    select_name.config(state='normal')
    search_text = search_entry.get()
    tree.delete(*tree.get_children())  # Get the search input
    df = merge_files()
    filterd_df = df[df['اسم المتوفي'].str.startswith(search_text)]

    for i, row in enumerate(filterd_df.itertuples(), start=1):
        values = [str(row[j]) for j in range(1, len(columns) + 1)]
        tree.insert("", "end", iid=i, values=values)


def clear_search():
    for item in tree.get_children():
        tree.selection_remove(item)  # Deselect all items


def export_excel():
    merge_files()
    start_date = sdate_entry.get_date()
    print(start_date)
    end_date = edate_entry.get_date()
    df = filter_excel(start_date, end_date, 'تاريخ الإنشاء')
    file_path = filedialog.asksaveasfilename(
        defaultextension='.xlsx',
        initialfile="سجلات المتوفين")
    # Save the workbook to the selected file location
    if file_path:
        # Save the DataFrame to the selected file location
        df.to_excel(file_path, index=False)


def filter_excel(sdate, edate, col):
    df = merge_files()
    if sdate == '':
        sdate = merge_files()['تاريخ الإنشاء'].min()
    if edate == '':
        edate = merge_files()['تاريخ الإنشاء'].max()
    return df[df[col].between(sdate, edate, inclusive='both')]


def imported_data():
    df2 = pd.read_html('data_est.xls')[0]
    df2['تاريخ الإنشاء'] = df2['تاريخ الإنشاء'].str.split(
        'هـ،').apply(lambda x: x[1].strip())
    df2 = df2[['تاريخ الإنشاء', 'إسم المتوفى','انشأ بواسطة']]
    df2['تاريخ الإنشاء'] = df2['تاريخ الإنشاء'].apply(lambda x: x[:13].strip())
    month_mapping = {
        'يناير': 'January',
        'فبراير': 'February',
        'مارس': 'March',
                'ابريل': 'April',
                'مايو': 'May',
                'يونيو': 'June',
                'يوليو': 'July',
                'اغسطس': 'August',
                'أغسطس': 'August',
                'سبتمبر': 'September',
                'أكتوبر': 'October',
                'اكتوبر': 'October',
                'نوفمبر': 'November',
                'ديسمبر': 'December',
                'ص': 'AM',
                'م': 'PM'
    }
    for ar_month, enmonth in month_mapping.items():
        df2['تاريخ الإنشاء'] = df2['تاريخ الإنشاء'].apply(
            lambda x: x.replace(ar_month, enmonth))
    df2['تاريخ الإنشاء'] = pd.to_datetime(
        df2['تاريخ الإنشاء'])
    return df2


def merge_files():
    path = os.path.join('data_files', 'rafed_data.csv')
    rafed_data = pd.read_csv(path)
    merged_files = rafed_data.merge(
        imported_data(), left_on='اسم المتوفي', right_on='إسم المتوفى', how='inner')
    merged_files.drop(['إسم المتوفى'], axis=1, inplace=True)
    return merged_files


def browse_file():
    file_types = [('Excel Files', '*.xlsx *.xls')]
    file_path = filedialog.askopenfilename(filetypes=file_types)
    file_var.set(file_path)


def upload_file():
    source_file = file_var.get()
    if source_file:
        destination = os.path.join(os.getcwd(), 'data_est.xls')
        shutil.copy2(source_file, destination)
        status_var.set(f"تم تحميل 'data_est.xlsx' بنجاح!")


def config_interface():
    # password_entry.config(state=tk.DISABLED)
    # username_entry.config(state=tk.DISABLED)
    status_label.config(
        text=' \nقد يستغرق الأمر دقائق..تجري الآن عملية الاستيراد\n يرجى الانتظار')
    start_button.config(state=tk.DISABLED)


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
        print(scrap.count)
        msg = messagebox.showinfo("success", "تمت العملية بنجاح!")
        if msg:
            password_entry.delete(0, tk.E)
            username_entry.delete(0, tk.E)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_table():
    try:
        # Clear existing data
        select_name.config(state='normal')
        tree.delete(*tree.get_children())
        path = os.path.join('data_files', 'rafed_data.csv')
        # Read the CSV file
        df = pd.read_csv(path)
        # Insert data into the treeview
        for i, row in enumerate(df.itertuples(), start=1):
            values = [str(row[j]) for j in range(1, len(columns) + 1)]
            tree.insert("", "end", iid=i, values=values)

    except FileNotFoundError:
        messagebox.showerror("لا يوجد ملف", "البيانات غير متوفرة.")


def lookup_name():
    def export_to_excel():
        file_path = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            initialfile=selected_name)
    # Save the workbook to the selected file location
        if file_path:
            # Save the DataFrame to the selected file location
            preview.to_excel(file_path, index=True)

    def copy_to_clipboard():
        all_data = [preview]
        if all_data:
            root.clipboard_clear()  # Clear previous clipboard contents
            root.clipboard_append(all_data)
            root.update()  # Update clipboard
            tk.messagebox.showinfo("تم النسح بنجاح", "البيانات جاهزة للصق!")
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, "values")
        selected_name = values[1]
        # Perform lookup or other actions based on the selected name
        new_window = tk.Toplevel(root)  # Create a new Toplevel window
        new_window.title("لوحة المعلومات")   # Set the title of the new window
        casted_item = int(selected_item)-1
        preview = merge_files().iloc[casted_item]
        preview = preview[preview.isna() == False]

        # Add widgets to the new window
        new_window_height = 400
        new_window.geometry(f"400x{new_window_height}")

        canvas = tk.Canvas(new_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")
        copy_button = ttk.Button(
            frame, text='نسخ البيانات', command=copy_to_clipboard)
        
        export_button = ttk.Button(
            frame, text='تصدير اكسل', command=export_to_excel)
        export_button.pack()
        # Add widgets to the frame in the new window    
        preview_index = preview.reset_index()[[casted_item,'index']]
        columns =['القيم','العناوين']
        tree_window = ttk.Treeview(frame,columns=columns,show='headings')
        tree_window.pack(padx=10, pady=5, anchor="w")
        for i, row in enumerate(preview_index.itertuples(), start=1):
            values = [str(row[j]) for j in range(1, len(preview_index.columns)+1)]
            tree_window.insert("", "end", iid=i, values=values)
        for col in columns:
            tree_window.heading(col, text=col, anchor='center')
            tree_window.column(col, anchor='center')

        scrollbar = tk.Scrollbar(
            new_window, orient=tk.VERTICAL, command=tree_window.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Configure canvas to work with the scrollbar
        tree_window.configure(yscrollcommand=scrollbar.set)
        # Configure canvas scrolling region
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        copy_button.pack()

    except IndexError:
        messagebox.showerror('خطا', '!!اختر اسماً من القائمة')


def update_gui():
    global scraping_thread
    if scraping_thread.is_alive():
        root.after(100, update_gui)
    else:
        status_label.config(text="Scraping complete")


def start_scraping():
    global scraping_thread
    scraping_thread = threading.Thread(target=scrape_website)
    scraping_thread.start()
    update_gui()
    config_interface()


def on_double_click(event):
    lookup_name()


root = tk.Tk()
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# scrapping tap
scrapping_tab = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
root.title("نظام معالجة البيانات")
useername_label = tk.Label(scrapping_tab, text='اسم المستخدم')
username_entry = tk.Entry(scrapping_tab)
password_label = tk.Label(scrapping_tab, text='كلمة المرور')
password_entry = tk.Entry(scrapping_tab, show='*')
status_label = tk.Label(scrapping_tab, text="ابدأ الاستيراد")
useername_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
start_button = ttk.Button(
    scrapping_tab, text="استيراد", command=start_scraping)
status_label.pack(pady=10)
start_button.pack(padx=10, pady=10)
notebook.add(scrapping_tab, text="استيراد السجلات")


# dead names tab
# Create a Treeview widget
columns = [
    "الرقم",
    "الاسم",
    "الجنس",
]
tree = ttk.Treeview(tab2, columns=columns, show="headings", height=25)
show_button = ttk.Button(
    tab2, text="انقر هنا لعرض الوفيات", command=show_table)
scrollbar = tk.Scrollbar(tab2, orient="vertical", command=tree.yview)
scrollbar.grid(row=1, column=1, sticky='sn')
tree.configure(yscrollcommand=scrollbar.set)
show_button.grid(row=0, column=0, columnspan=1, sticky='snew')
# Configure the Treeview columns
for col in columns:
    tree.heading(col, text=col, anchor='center')
    tree.column(col, anchor='center')
tree.grid(row=1, column=0, sticky='nsew')
tree.bind("<Double-1>", on_double_click)  # Create a Scrollbar widget
file_var = tk.StringVar()
status_var = tk.StringVar()
file_label = ttk.Label(tab3, text="اختيار الملف")
file_label.pack()
browse_button = ttk.Button(tab3, text="تحديد الملف", command=browse_file)
browse_button.pack()
select_name = ttk.Button(
    tab2, text='معاينة', command=lookup_name, state='disabled')
select_name.grid(row=2, column=0, columnspan=1, sticky='snew')
file_entry = ttk.Entry(tab3, textvariable=file_var, state='readonly')
file_entry.pack()
upload_button = ttk.Button(tab3, text="تحميل", command=upload_file)
upload_button.pack()
status_label = tk.Label(tab3, textvariable=status_var)
status_label.pack()
sdate_label = ttk.Label(tab3, text='تاريخ البداية')
sdate_label.pack()
sdate_entry = Calendar(tab3)
sdate_entry.pack()
edate_label = ttk.Label(tab3, text='تاريخ النهاية')
edate_label.pack()
edate_entry = Calendar(tab3)
edate_entry.pack()
search_label = ttk.Button(
    tab2, text='بحث باسم المتوفى', command=search, width=30)
search_entry = ttk.Entry(tab2, font=('Arial', 12))

search_entry.grid(row=4, column=0)
search_label.grid(row=3, column=0)

export_excel_button = ttk.Button(tab3, text='تصدير اكسل', command=export_excel)
export_excel_button.pack(padx=20, pady=20)
# df_describe = merge_files().describe().transpose().reset_index()
# columns = [i for i in df_describe.columns]

# tree_general = ttk.Treeview(tab4,columns=columns,show='headings')
# tree_general.pack()
# for i, row in enumerate(df_describe.itertuples(), start=1):
#             values = [str(row[j]) for j in range(1, len(df_describe.columns) + 1)]
#             tree_general.insert("", "end", iid=i, values=values)
# for col in columns:
#     tree_general.heading(col, text=col, anchor='center')
#     tree_general.column(col, anchor='center')
notebook.add(tab2, text="أسماء الوفيات")
notebook.add(tab3, text="تحليل البيانات")
# notebook.add(tab4,text='نظرة عامة')
root.mainloop()
