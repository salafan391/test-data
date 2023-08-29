import pandas as pd
import os

def imported_data():
    df2 = pd.read_html('data_est.xls')[0]
    df2['تاريخ الإنشاء'] = df2['تاريخ الإنشاء'].str.split(
        'هـ،').apply(lambda x: x[1].strip())
    df2 = df2[['تاريخ الإنشاء', 'إسم المتوفى','انشأ بواسطة']]
    print(df2)
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
dead_id= 1183695038
dfs = merge_files().iloc[645]
dfs = dfs.reset_index()
print(dfs)

