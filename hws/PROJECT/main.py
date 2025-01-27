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

    for char in word:
        if char == 'n': 
            print()  
            lines_to_print = ['' for _ in range(8)]  
        elif char in banner_dict:
            art = banner_dict[char]
            for i in range(8):
                lines_to_print[i] += art[i] 
        else:
            print(f"Предупреждение: символ '{char}' не найден в баннере.")

    for line in lines_to_print:
        print(line + "$") 

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
