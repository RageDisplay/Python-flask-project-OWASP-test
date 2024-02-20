from urllib.parse import urlparse

def filter_url(url):
    # Разбор URL
    parsed_url = urlparse(url)

    # Проверка компонентов URL
    if parsed_url.scheme not in ['http', 'https']:
        return None  # Фильтрация недопустимых схем
    if parsed_url.hostname in ['localhost', '127.0.0.1']:
        return None  # Фильтрация локальных адресов
    if parsed_url.path.startswith('/internal/'):
        return None  # Фильтрация внутренних путей

    return url  # Возвращаем отфильтрованный URL

url = input("Введите URL: ")
filtered_url = filter_url(url)
if filtered_url:
    print("Отфильтрованный URL:", filtered_url)
else:
    print("Недопустимый URL")
