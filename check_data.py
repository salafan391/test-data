import pandas as pd
from tk_try import merge_files

def check_data():
    try:
        merged_files = merge_files()[['تاريخ الإنشاء', 'اسم المتوفي','انشأ بواسطة','اسم المبلغ','الشاهد الأول','الشاهد الثاني']]
        df = pd.read_csv('data_files/rafed_data.csv')
        def full_func(value):
            if isinstance(value,float):
                return len(str(value).split('.')[0])
            elif isinstance(value,str) and value[0] != '0':
                return len(value)
            elif value[0] == '0':
                return len(value[1:]) 
        def check_id(value):
            value = str(value)
            if value != '10':
                return 'x'
            else:
                return ''
        def check_phone(value):
            value = str(value)
            if value != '9':
                return 'x'
            else:
                return ''

        df['id_rep'] = df['رقم هوية المبلغ '].apply(full_func)
        df['phone_rep'] = df['رقم تليفون المبلغ'].apply(full_func)

        df['id_w1'] = df['رقم هوية الشاهد الأول'].apply(full_func)
        df['phone_w1']=df['رقم تلفون الشاهد الأول'].apply(full_func)

        df['id_w2'] = df['رقم هوية الشاهد الثاني'].apply(full_func)
        df['phone_w2']=df['رقم تلفون الشاهد الثاني'].apply(full_func)

        clean_df = df[df['رقم تلفون الشاهد الأول'].notna()]
        w1 = clean_df[['الشاهد الأول','id_w1','phone_w1']].query("id_w1 !=10 | phone_w1 != 9")
        w2 = clean_df[['الشاهد الثاني','id_w2','phone_w2']].query("id_w2 !=10 or phone_w2 != 9")
        reporters = df[['اسم المبلغ','id_rep','phone_rep']].query('id_rep !=10 | phone_rep != 9')
        w1['phone_w1']=w1['phone_w1'].apply(check_phone)
        w1['id_w1']=w1['id_w1'].apply(check_id)
        reporters['id_rep'] = reporters['id_rep'].apply(check_id)
        reporters['phone_rep'] = reporters['phone_rep'].apply(check_phone)

        w2['id_w2'] = w2['id_w2'].apply(check_id)
        w2['phone_w2'] = w2['phone_w2'].apply(check_phone)
        w1.rename(columns={'id_w1' : 'رقم البطاقة','phone_w1':'رقم الجوال'},inplace=True)
        w2.rename(columns={'id_w2' : 'رقم البطاقة','phone_w2':'رقم الجوال'},inplace=True)
        
        reporters.rename(columns={'id_rep' : 'رقم البطاقة','phone_rep':'رقم الجوال'},inplace=True)
        reporters = reporters.merge(merged_files,left_on='اسم المبلغ',right_on='اسم المبلغ',how='inner')
        w1 = w1.merge(merged_files,left_on='الشاهد الأول',right_on='الشاهد الأول')
        w2 = w2.merge(merged_files,left_on='الشاهد الثاني',right_on='الشاهد الثاني')
        writer = pd.ExcelWriter('data_files/final_reports_errors.xlsx', engine='xlsxwriter')

        reporters.to_excel(writer,sheet_name='1')
        w1.to_excel(writer,sheet_name='2')
        w2.to_excel(writer,sheet_name='3')
        writer.close()
        
    except:
        print('لا يوجد أخطاء')



check_data()
