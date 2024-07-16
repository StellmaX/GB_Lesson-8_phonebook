from csv import DictWriter, DictReader
from os.path import exists


class MyNameError(Exception):
    def __init__(self, txt):
        self.txt = txt

class Num:
    def __init__(self, max):
        self.max = max
        
    def __iter__(self):
        self.num = 0
        return self
    
    def __next__(self):
        if(self.num >= self.max):
            raise StopIteration
        self.num += 1
        return self.num

    
def get_data():
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise MyNameError("Слишком короткое имя")
            last_name = input("Введите Фамиилию: ")
            if len(last_name) < 2:
                raise MyNameError("Слишком короткая фамилия")
            phone = input("Введите номер телефона: ")
            if len(phone) < 5:
                raise MyNameError("Номер телефона должен быть не менее 5 символов")
        except MyNameError as err:
            print(err)
        else:
            flag = True
    return [first_name, last_name, phone]


def create_file(filename):
    with open(filename, "w", encoding="utf-8") as data:
        f_w = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_w.writeheader()


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as data:
        f_r = DictReader(data)
        return list(f_r)


def write_file(filename, lst):
    res = read_file(filename)
    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    standard_write(filename, res)


def row_search(filename):
    last_name = input("Введите фамилию: ")
    res = read_file(filename)
    for row in res:
        if last_name == row["Фамилия"]:
            return row
    return "Запись не найдена"


def delete_row(filename):
    row_number = int(input("Введите номер строки: "))
    res = read_file(filename)
    res.pop(row_number - 1)
    standard_write(filename, res)


def standard_write(filename, res):
    with open(filename, "w", encoding="utf-8") as data:
        f_w = DictWriter(data, fieldnames=["Имя", "Фамилия", "Телефон"])
        f_w.writeheader()
        f_w.writerows(res)


def change_row(filename):
    row_number = int(input("Введите номер строки: "))
    res = read_file(filename)
    data = get_data()
    res[row_number - 1]["Имя"] = data[0]
    res[row_number - 1]["Фамилия"] = data[1]
    res[row_number - 1]["Телефон"] = data[2]
    standard_write(filename, res)\
       


def help():
    options = ["Список команд:" , "'q'-завершение" , "'w'-запись в книгу" , "'r'-чтение из книги" , "'f'-поиск" , "'d'-удаление данных" , "'c'-изменить данные"]
    for i in options:
        print(i, end='\n')

def main():
    while True:
        help()
        command = input("Укажите команду: ")
        if command == "q":
            break
        elif command == "w":
            if not exists(filename):
                create_file(filename)
            write_file(filename, get_data())
        elif command == "r":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            num = iter(Num(len(read_file(filename))))
            for i in read_file(filename):
                print(next(num), *i.values(), end = '\n')
        elif command == "f":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            print(*row_search(filename).values(), end = '\n')
        elif command == "d":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            delete_row(filename)
        elif command == "c":
            if not exists(filename):
                print("Файл не существует. Создайте его.")
                continue
            change_row(filename)

filename = "phone.csv"
main() 
