import argparse

def load_banner_from_file(file_path):
    """Загружает ASCII-арт баннер из файла и возвращает его как словарь символов."""
    banner_dict = {}

    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()  
        
        
        while len(lines) % 8 != 0:
            lines.append("        ")  

        for i in range(0, len(lines), 8):
            char_art = lines[i:i+8] 
            char = chr(i // 8 + ord(' '))  
            banner_dict[char] = char_art
        
        banner_dict[' '] = ["        "] * 8  

        return banner_dict

    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return {}
    
def print_word_in_banner(word, banner_dict):
    """Выводит слово с использованием ASCII-арт символов, корректно обрабатывая символ новой строки."""
    lines_to_print = ['' for _ in range(8)]  
    start_new_line = False  # Переменная, которая отслеживает, нужно ли начинать с новой строки

    for char in word:
        if char in banner_dict:
            art = banner_dict[char]
            for i in range(8):
                if start_new_line:
                    lines_to_print[i] = art[i]  # Начинаем с новой строки, записывая только текущий символ
                    start_new_line = False  # Сбрасываем флаг
                else:
                    lines_to_print[i] += art[i]  # Добавляем символ в текущую строку
                if char == '\n':  # Символ новой строки, начинаем с новой строки
                    print("\n".join(lines_to_print))  # Печатаем текущие строки
                    lines_to_print = ['' for _ in range(8)]  # Очищаем строки для следующего блока
        else:
            print(f"Предупреждение: символ '{char}' не найден в баннере.")

    # Выводим оставшиеся строки после завершения цикла
    if lines_to_print:
        print("\n".join(lines_to_print))

def main():
    parser = argparse.ArgumentParser(description='Отобразить слово в ASCII-арт стиле.')
    parser.add_argument('word', type=str, help='Слово для отображения в ASCII-арте')

    args = parser.parse_args()

    banner_file_path = 'standard.txt'

    banner_dict = load_banner_from_file(banner_file_path)

    if banner_dict:
        print_word_in_banner(args.word, banner_dict)
    else:
        print("Не удалось загрузить баннер.")

if __name__ == '__main__':
    main()
