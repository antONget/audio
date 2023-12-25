import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

gp = gspread.service_account(filename='aquarel.json')
#Open Google spreadsheet
gsheet = gp.open("AquarelArt")
#Select worksheet
wsheet = gsheet.worksheet("Нейрокартины")
masterClass = gsheet.worksheet("Мастер-класс")
start = gsheet.worksheet("/start")
# получить все значения
# wsheet.get_all_values()

# добавить значения
def append_name(ID, name):
    wsheet.append_row([ID, name])

def append_name_start(ID):
    start.append_row([ID])

def append_name_master(ID, name):
    masterClass.append_row([ID, name])

# поиск строки и столбца положения значения
def values_row_col(value):
    values = wsheet.get_all_values()
    res = []
    for i, r in enumerate(values):
        for j, c in enumerate(r):
            if str(value) in c:
                res.append({'row': i, 'col': j})
    return res

def values_row_col_master(value):
    print("values_row_col_master")
    values = masterClass.get_all_values()
    res = []
    for i, r in enumerate(values):
        for j, c in enumerate(r):
            if str(value) in c:
                res.append({'row': i, 'col': j})
    return res
# добавления значения
def update_phone(message):
    print("update_phone")
    ID = message.chat.id
    print(f"ID: {ID}")
    res = values_row_col(ID)
    print(res)
    row = res[-1]["row"]+1
    print(f"row: {row}")
    if message.contact != None:
        print("contact")
        phone = message.contact.phone_number
    else:
        print("text")
        phone = message.text
    wsheet.update(f'C{row}', phone)

def update_phone_master(message):
    print("update_phone_master")
    ID = message.chat.id
    res = values_row_col_master(ID)
    row = res[-1]["row"]+1
    if message.contact != None:
        phone = message.contact.phone_number
    else:
        phone = message.text
    masterClass.update(f'C{row}', phone)


def get_all_user():
    values = start.get_all_values()
    users = set()
    for user in values:
        users.add(user[0])
    print(users)
    return list(users)

if __name__ == '__main__':
    values_row_col(value='anna')
