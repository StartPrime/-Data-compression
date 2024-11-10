def my_counter(iterable):
    frequency_dict = {}

    for item in iterable:
        if item in frequency_dict:
            frequency_dict[item] += 1
        else:
            frequency_dict[item] = 1

    return frequency_dict

def build_tree(frequencies):
    # Символы первичного алфавита m1 выписывают по убыванию вероятностей.
    # Символы полученного алфавита делят на две части, суммарные вероятности символов которых максимально близки друг другу.
    # В префиксном коде для первой части алфавита присваивается двоичная цифра «0», второй части — «1».
    # Полученные части рекурсивно делятся, и их частям назначаются соответствующие двоичные цифры в префиксном коде.

    sorted_items = sorted(frequencies.items(), key=lambda item: item[1], reverse=True) # Сортируем по количеству частот по убыванию
    if len(sorted_items) == 1:
        return {sorted_items[0][0]: ''}

    total = sum(frequencies.values())
    cumulative = 0 # переменная для суммирования частот
    split_index = 0 # индекс для точки разбиения

    for i, (char, freq) in enumerate(sorted_items):
        cumulative += freq
        if cumulative >= total / 2:
            split_index = i
            break

    left = dict(sorted_items[:split_index + 1])
    right = dict(sorted_items[split_index + 1:])

    left_codes = build_tree(left)
    right_codes = build_tree(right)

    for char in left_codes:
        left_codes[char] = '0' + left_codes[char]
    for char in right_codes:
        right_codes[char] = '1' + right_codes[char]

    return {**left_codes, **right_codes}

def encode(text, codes):
    return ''.join(f'/{codes[char]}' for char in text)

def decode(encoded_text, codes):
    current_code = ''
    decoded_text = ''
    for bit in encoded_text:
        current_code += bit
        if bit.isdigit():
            if current_code in codes:
                if codes[current_code] == '___':
                    decoded_text += '\n'
                    current_code = ''
                    continue
                decoded_text += codes[current_code]
                current_code = ''
        else:
            current_code = ''
    return decoded_text
def shannon_fano_encode(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    frequencies = my_counter(text)
    codes = build_tree(frequencies)
    encoded_text = encode(text, codes)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(encoded_text)

        file.write("/\nКоды:\n")  # Добавляем заголовок для кодов
        for char, code in frequencies.items():
            if char == '\n':
                file.write(f"___: {code}\n")  # Используем ___ для новой строки
                continue
            file.write(f"{char}: {code}\n")  # Записываем символ и его код

def shannon_fano_decode(encoded_file, output_file):
    with open(encoded_file, 'r', encoding='utf-8') as file:
        lines = file.read()

    encoded_text = ''
    codes = {}

    encode_data = ''
    for i in lines[1:]:
        if i == 'К':
            break
        if i == '/':
            encoded_text += encode_data
            encode_data = ''
            continue
        encode_data += i
    file.close()
    with open(encoded_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Читаем коды после закодированного текста
    for line in lines:
        line = line.strip() if line[0] != ' ' else line.rstrip()
        if ':' in line and 'Коды' not in line:  # Игнорируем контрольные символы и заголовок
            parts = line.split(': ', 1)
            if len(parts) == 2:
                char, code = parts
                codes[char] = int(code)

    codes = build_tree(codes)
    codes = {value: key for key, value in codes.items()}
    decoded_text = decode(encoded_text, codes)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(decoded_text)
