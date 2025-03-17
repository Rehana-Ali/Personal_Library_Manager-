



import streamlit as st
import json

# File to store the library data
LIBRARY_FILE = "library.json"

# Load library from file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize library
library = load_library()

st.title("📚 Personal Library Manager")
st.image("bk_library.jpg", use_container_width=True)



menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Statistics"])

# Add a Book
if menu == "Add a Book":
    st.header("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read")
    
    if st.button("Add Book"):
        if title and author and year and genre:
            library.append({"title": title, "author": author, "year": year, "genre": genre, "read": read_status})
            save_library(library)
            st.success(f'Book "{title}" added!')
        else:
            st.error("All fields must be filled!")

# Remove a Book
elif menu == "Remove a Book":
    st.header("Remove a Book")
    titles = [book["title"] for book in library]
    if titles:
        book_to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != book_to_remove]
            save_library(library)
            st.success(f'Book "{book_to_remove}" removed!')
    else:
        st.info("No books available to remove.")

# Search for a Book
elif menu == "Search for a Book":
    st.header("Search for a Book")
    search_query = st.text_input("Enter title or author")
    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                st.write(f'**{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {"Read" if book["read"] else "Unread"}')
        else:
            st.warning("No matching books found.")

# Display All Books
elif menu == "Display All Books":
    st.header("All Books in Library")
    if library:
        for book in library:
            st.write(f'**{book["title"]}** by {book["author"]} ({book["year"]}) - {book["genre"]} - {"Read" if book["read"] else "Unread"}')
    else:
        st.info("No books in the library.")

# Statistics
elif menu == "Statistics":
    st.header("Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"Total books: {total_books}")
    st.write(f"Read books: {read_books} ({read_percentage:.2f}%)")
