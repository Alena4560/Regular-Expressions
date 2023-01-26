from typing import List, Optional
import csv
import re


def load_raw_data(filename: str) -> Optional[List[List]]:
    try:
        with open(filename, encoding='utf-8', newline='') as f:
            lines = csv.reader(f, delimiter=",")
            return list(lines)
    except FileNotFoundError:
        print(f"Ошибка! Файл {filename} не найден!")
        return None


patterns = {
    'fio': {
        'regexp': r'^(\w+)( |,)(\w+)( |,)(\w+|),(,+|)(,,,|[А-Яа-я]+)',
        'subst': r'\1,\3,\5,\7'},
    'phone': {
        'regexp': r'(\+7|7|8)?\s?\(?(\d{3})\)?[\s-]?(\d{3})-?(\d{2})-?(\d{2})',
        'subst': r'+7(\2)\3-\4-\5'},
    'add_phone': {
        'regexp': r'\s?\(?доб\.\s?(\d{4})\)?',
        'subst': r' доб. \1'}
}


def parse_line(raw_line: List[str]) -> List[str]:
    solid_line = ','.join(raw_line)
    for key in patterns:
        regexp = patterns[key]['regexp']
        subst = patterns[key]['subst']
        solid_line = re.sub(regexp, subst, solid_line, flags=0)
    result = solid_line.split(',')
    return result


def parse_data(raw_data: List[List]) -> List[List]:
    result = []
    for raw_line in raw_data:
        result.append(parse_line(raw_line))
    return result


def double_check(data: List[List]) -> List[List]:
    names_dict = {}
    result = []

    for line in data:
        name_tuple = (line[0], line[1])
        if name_tuple in names_dict:
            number = names_dict[name_tuple]
            for i in range(3, 7):
                if result[number][i] == '':
                    result[number][i] = line[i]
        else:
            result.append(line)
            number = len(result) - 1
            names_dict[name_tuple] = number

    return result


def save_data(ready_data: List[List], filename: str):
    with open(filename, "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(ready_data)


if __name__ == '__main__':
    raw_data = load_raw_data("phonebook_raw.csv")
    data1 = parse_data(raw_data)
    data2 = double_check(data1)
    save_data(data2, "phonebook.csv")
