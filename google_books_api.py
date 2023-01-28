import requests
import pandas as pd

# Google Books API
google_books_url = 'https://www.googleapis.com/books/v1/volumes'
google_books_key = 'AIzaSyBnN9HIF15tyvLU4yKQ589uGhexjtEQ6pI'

# List of ISBN numbers
isbn = pd.read_csv("isbn.csv")
isbn_numbers = isbn["ISBN"].values.tolist()
isbn_num = isbn_numbers[:999]

# Create an empty list to store the book details
books_data = []

# Iterate through the list of ISBN numbers
for isbn in isbn_num:
    params = {'q': 'isbn:' + isbn, 'key': google_books_key}
    response = requests.get(google_books_url, params=params)
    if response.status_code == 200:
        book_data = response.json()
        if 'items' in book_data:
            book_info = book_data['items'][0]['volumeInfo']
            title = book_info.get('title', None)
            authors = book_info.get('authors', None)
            publisher = book_info.get('publisher', None)
            published_date = book_info.get('publishedDate', None)
            average_rating = book_info.get('averageRating', None)
            review_count = book_info.get('ratingsCount', None)
            books_data.append({
                'ISBN': isbn,
                'Title': title,
                'Authors': authors,
                'Publisher': publisher,
                'Published Date': published_date,
                'Rating': average_rating,
                'Review Count': review_count
            })
        else:
            print(f'ISBN {isbn} is not found.')
    else:
        print(f'An error occurred while searching for ISBN {isbn}')

# Create a DataFrame from the book details
df = pd.DataFrame(books_data)
print(df.head(5))
# Write the DataFrame to a CSV file
df.to_csv('books_data.csv', index=False)
