import csv
import json


def distribute_books():
    # Читаем книги из CSV
    books = []
    with open('dz4/books.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append({
                "title": row['Title'],
                "author": row['Author'],
                "pages": int(row['Pages']),
                "genre": row['Genre']
            })
    
    # Читаем пользователей из JSON
    with open('dz4/users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    # Распределяем книги максимально поровну
    total_books = len(books)
    total_users = len(users)
    books_per_user = total_books // total_users
    extra_books = total_books % total_users
    
    # Создаем новый список пользователей с нужными полями
    result = []
    book_index = 0
    for i, user in enumerate(users):
        # Первые extra_books пользователей получат на 1 книгу больше
        books_count = books_per_user + (1 if i < extra_books else 0)
        
        # Создаем пользователя только с нужными полями
        result.append({
            "name": user['name'],
            "gender": user['gender'],
            "address": user['address'],
            "age": user['age'],
            "books": books[book_index:book_index + books_count]
        })
        book_index += books_count
    
    # Сохраняем результат
    with open('dz4/result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"Распределено {total_books} книг между {total_users} пользователями")
    print(f"Книг на пользователя: {books_per_user}, дополнительных книг: {extra_books}")


if __name__ == '__main__':
    distribute_books()
