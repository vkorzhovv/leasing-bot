import re

def remove_special_characters(input_string):
    # Используем регулярное выражение для удаления всех символов, кроме букв и цифр
    result = re.sub(r'[^a-zA-Z0-9а-яА-Я\s]', '', input_string)
    return result.replace(' ', '_')


