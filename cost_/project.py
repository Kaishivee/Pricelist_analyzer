import os
import csv
import webbrowser


class PriceMachine:
    def __init__(self):
        self.data = []

    def load_prices(self, folder_path='.'):
        """
        Загружает данные из CSV файлов, содержащих "price" в имени,
        из указанной папки
        """
        for filename in os.listdir(folder_path):
            if 'price' in filename.lower() and filename.endswith('.csv'):
                filepath = os.path.join(folder_path, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)  # csv.DictReader для работы с именованными полями
                        for row in reader:
                            try:
                                name = row.get('название', row.get('товар', row.get('продукт', row.get(
                                    'наименование')))).strip().lower()
                                price = float(row.get('цена', row.get('розница')).replace(',', '.'))
                                weight = float(row.get('вес', row.get('масса', row.get('фасовка'))).replace(',', '.'))
                                price_per_kg = price / weight if weight > 0 else 0
                                self.data.append({
                                    'name': name,
                                    'price': price,
                                    'weight': weight,
                                    'file': filename,
                                    'price_per_kg': price_per_kg
                                })
                            except (ValueError, TypeError, AttributeError):
                                pass  # Пропуск строк с некорректными данными
                except Exception as e:
                    print(f'Ошибка при обработке файла {filename}: {e}')

    def find_text(self, text):
        """Находит позиции, содержащие указанный текст в названии продукта."""
        results = []
        for item in self.data:
            if text.lower() in item['name']:
                results.append(item)
        results.sort(key=lambda x: x['price_per_kg'])
        if results:
            print("\n№   Наименование               Цена   Вес      Файл      Цена за кг.")
            for i, item in enumerate(results, 1):
                print(
                    f"{i:<4} {item['name']:<25} {item['price']:<6} {item['weight']:<6} {item['file']:<12} {item['price_per_kg']:<.2f}")
        else:
            print("Ничего не найдено.")
        return results

    def export_to_html(self, filename='output.html'):
        """Экспортирует данные в HTML файл с форматированием."""
        sorted_data = sorted(self.data, key=lambda x: x['price'])
        result = '''<!DOCTYPE html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
        <table>
            <tr>
                <th>Номер</th>
                <th>Название</th>
                <th>Цена</th>
                <th>Фасовка</th>
                <th>Файл</th>
                <th>Цена за кг.</th>
            </tr>'''
        for i, item in enumerate(sorted_data, 1):
            result += f'''<tr>
                <td>{i}</td>
                <td>{item['name']}</td>
                <td>{item['price']}</td>
                <td>{item['weight']}</td>
                <td>{item['file']}</td>
                <td>{item['price_per_kg']:.2f}</td>
            </tr>\n'''
        result += '</table></body></html>'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Данные успешно экспортированы в {filename}.")
        webbrowser.open_new_tab(filename)


if __name__ == '__main__':
    pm = PriceMachine()
    pm.load_prices('C:/Users/User/PycharmProjects/diploma_thesis/my_proj/cost_')
    while True:
        user_input = input("\nВведите текст для поиска (или 'exit' для выхода): ").strip()
        if user_input.lower() == 'exit':
            break
        results = pm.find_text(user_input)
        if results and input("\nХотите экспортировать данные в HTML? (y/n): ").strip().lower() == 'y':
            pm.export_to_html()
