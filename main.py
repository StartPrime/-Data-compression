import SF as sf
import LZ78 as ls

while True:
    print('1: Кодирование и декодирование\n2: Кодирование\n3: Декодирование\n4: Выход')
    choice = input()
    if choice == "1":
        # Кодирование
        sf.shannon_fano_encode('input.txt', 'encodeSF.txt')
        ls.main('encodeSF.txt', 'encodeLZ.txt', mode='encode')
        # Декодирование
        ls.main('encodeLZ.txt', 'decodeLZ.txt', mode='decode')
        sf.shannon_fano_decode('decodeLZ.txt', 'decodeSF.txt')
    elif choice == "2":
        # Кодирование
        sf.shannon_fano_encode('input.txt', 'encodeSF.txt')
        ls.main('encodeSF.txt', 'encodeLZ.txt', mode='encode')
    elif choice == "3":
        # Декодирование
        ls.main('encodeLZ.txt', 'decodeLZ.txt', mode='decode')
        sf.shannon_fano_decode('decodeLZ.txt', 'decodeSF.txt')
    else:
        break
