def lz78_encode(data):
    """Кодирование данных с использованием алгоритма LZ78."""
    dictionary = {}
    result = []
    current_string = ""
    index = 1

    # Находим позицию слова "Коды" в тексте
    tx, codes = data.split("Коды")

    # Кодируем текст до "Коды"
    for char in tx:
        current_string += char
        if current_string not in dictionary:
            dictionary[current_string] = index
            result.append((dictionary[current_string[:-1]], char if not char.isdigit() else int(char)) if current_string[:-1] else (0, char if not char.isdigit() else int(char)))
            index += 1
            current_string = ""

    # Обработка остатка в current_string
    if current_string:
        dictionary[current_string] = index
        result.append((dictionary[current_string[:-1]], current_string[-1]) if current_string[:-1] else (0, current_string[-1]))
        index += 1

    return result, "\nКоды" + codes

def lz78_decode(encoded_data):
    """Декодирование данных, закодированных с использованием LZ78 с устойчивостью к ошибкам."""
    dictionary = {}
    decoded_string = ""
    index = 1
    # Ищем индекс "Коды" в закодированном списке
    codes_index = encoded_data[0:encoded_data.index("Коды")]
    codes_index = codes_index.split(')')
    # Декодируем текст до "Коды"
    for i in codes_index:
        try:
            i = i.split(',')
            (idx, char) = int(i[0][1:]), str(i[1])
            if idx == 0:
                decoded_string += char
            else:
                decoded_string += dictionary[idx] + char
            dictionary[index] = decoded_string[-1] if idx == 0 else decoded_string[-(len(dictionary[idx]) + 1):]
            index += 1
        except:
            continue
    # Добавляем "Коды" без декодирования
    decoded_string += "Коды"

    # Добавляем оставшийся текст без декодирования
    decoded_string += encoded_data[2:]  # Добавляем оставшийся текст как единую строку
    return decoded_string

def write_file(filename, data, codes=''):
    """Запись данных в файл."""
    with open(filename, 'w', encoding='utf-8') as file:
        if codes != '':
            for i in data:
                if i[1] == '\n':
                    file.write(f'({i[0]}, ')
                else:
                    file.write(f'({i[0]},{i[1]})')
            file.write(codes)
            file.close()
        else:
            file.write(data)
def main(input_file, output_file, mode='encode'):
    """Главная функция для обработки файлов."""
    data = open(input_file, encoding='utf-8')
    data = data.read()
    if mode == 'encode':
        encoded_data, codes = lz78_encode(data)
        write_file(output_file, encoded_data, codes)
    elif mode == 'decode':
        # Преобразование строкового представления кортежей обратно в реальные кортежи
        decoded_data = lz78_decode(data)
        write_file(output_file, decoded_data,)
        print('Декодирование LZ78 закончено')


