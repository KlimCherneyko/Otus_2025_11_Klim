import csv
import json


def distribute_books():
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
    
    with open('dz4/users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    total_books = len(books)
    total_users = len(users)
    books_per_user = total_books // total_users
    extra_books = total_books % total_users
    
    result = []
    book_index = 0
    for i, user in enumerate(users):
        books_count = books_per_user + (1 if i < extra_books else 0)
        
        result.append({
            "name": user['name'],
            "gender": user['gender'],
            "address": user['address'],
            "age": user['age'],
            "books": books[book_index:book_index + books_count]
        })
        book_index += books_count
    
    with open('dz4/result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    print(f"Распределено {total_books} книг между {total_users} пользователями")
    print(f"Книг на пользователя: {books_per_user}, дополнительных книг: {extra_books}")


if __name__ == '__main__':
    distribute_books()
