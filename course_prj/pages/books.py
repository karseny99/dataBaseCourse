import streamlit as st
from pages.search import show_book_info
from services.book import get_total_books_count, get_books, get_authors, get_paginated_books, get_categories, get_publishing_years


# def paginator(label, books, items_per_page) -> None:

#     if page_number:

        # get_books()

def pagination_panel() -> None:
    with st.sidebar:
        books_count = get_total_books_count()
        print(books_count)
        published_years = get_publishing_years()
        authors = get_authors()
        categories = get_categories()


        category_filter = st.selectbox(label="Select category", options=categories, index=None)
        author_filter = st.selectbox(label="Select Author", options=authors, index=None, placeholder="Choose author")
        published_year_filter = st.selectbox(label="Select year", options=published_years, index=None, placeholder="Choose year")
        
        if category_filter or author_filter or published_year_filter:
            books_count = get_total_books_count(category_filter, author_filter, published_year_filter)

        items_per_page = 4
        n_pages = (books_count - 1) // items_per_page + 1  
        page_format_func = lambda i: "Page %s" % (i + 1)
        page_number = st.selectbox("Select page", options=range(n_pages), format_func=page_format_func)

    if page_number is not None:
        books = get_paginated_books(page_number + 1, items_per_page, author_filter, published_year_filter, category_filter)

        for book in books:
            show_book_info(book)
    else:
        st.info("There are no books like that")


def books_page() -> None:
    back_button = st.button("Back")

    st.title("Book's views")

    if not(st.session_state.get("logged_in", None)) or back_button:
        st.switch_page("main.py")


    pagination_panel()






if __name__ == "__main__":
    books_page()
