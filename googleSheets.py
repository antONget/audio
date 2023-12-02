import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

gp = gspread.service_account(filename='aquarel.json')
#Open Google spreadsheet
gsheet = gp.open("AquarelArt")
#Select worksheet
wsheet = gsheet.worksheet("Запись на мастер класс")
# получить все значения
# wsheet.get_all_values()

# добавить значения
def append_name(ID, name):
    wsheet.append_row([ID, name])

# поиск строки и столбца положения значения
def values_row_col(value):
    values = wsheet.get_all_values()
    res = []
    for i, r in enumerate(values):
        for j, c in enumerate(r):
            if str(value) in c:
                res.append({'row': i, 'col': j})
    return res

# добавления значения
def update_phone(message):
    ID = message.chat.id
    res = values_row_col(ID)
    row = res[-1]["row"]+1
    if message.contact != None:
        phone = message.contact.phone_number
    else:
        phone = message.text
    wsheet.update(f'C{row}', phone)

if __name__ == '__main__':
    values_row_col(value='anna')
