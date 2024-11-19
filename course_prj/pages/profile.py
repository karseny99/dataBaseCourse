
import streamlit as st
from datetime import datetime
import os


from services.user import get_info_actions_user, get_user_info
from services.error_handler import error_handler
from services.request import add_request

import services.book

def role_request(user_info: dict) -> None:

    if user_info['role'] == 'admin':
        return
    
    if st.button("Request for admin-permissions"):

        if not add_request(user_info['user_id']):
            st.warning("Approval period is 7 days, wait for it!")
        else:
            st.success(f"Request-{add_request(user_info['user_id'])} sent")


def display_admin_page(user_info: dict) -> None:

    if user_info['role'] != 'admin':
        return
    
    upload_book = st.file_uploader("Choose book's file", type=["fb2"], accept_multiple_files=False)
    upload_cover = st.file_uploader("Choose cover's file (jpg)", type=["jpg"], accept_multiple_files=False)

    if upload_book is not None:

        if upload_book.type != 'application/octet-stream':
            st.error("Wrong file format")
            return
        
        unique_filename = services.book.generate_unique_filename(upload_book.name)

        save_path = os.path.join("storage", "books", unique_filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as book_file:
            book_file.write(upload_book.getbuffer())  

        st.success(f"File {upload_book.name} uploaded")

        cover_save_path = ""
        if upload_cover is not None:
            cover_save_path = os.path.join("storage", "covers", f"{os.path.splitext(unique_filename)[0]}.jpg")
            os.makedirs(os.path.dirname(cover_save_path), exist_ok=True)

            with open(cover_save_path, "wb") as cover_file:
                cover_file.write(upload_cover.getbuffer())

            st.success(f"File {upload_book.name} uploaded")

        else:
            st.info("Cover wasn't uploaded")

        book_item = {
            "title": st.text_input("Enter book's name").strip(),
            "published_year": st.number_input("Enter publishing year"),
            "isbn": st.text_input("Enter ISBN").strip(),
            "description": st.text_input("Enter book's description").strip(),
            "file_path": save_path,
            "cover_image_path": cover_save_path,
            "authors": st.text_input("Enter author(s) - split by , if more then one").strip().split(','),
            "categories": st.text_input("Enter category(s) - split by , if more then one").strip().split(',')
        }

        submit_button = st.button("Submit book's data")

        if submit_button:
            st.success(f"Book added to database with id {services.book.add_book(book_item)}")





# @error_handler
def profile_page() -> None:
    try:
        user_id = st.session_state.user_id
    except:
        st.switch_page("main.py")
    user_info = get_info_actions_user(user_id)  

    back_button = st.button("Back") 
    if back_button:
        st.switch_page("main.py")   

    st.title(f"{user_info['username']}'s profile page")
    st.write(f"*{user_info['email']}*")
    st.write(f"Permission role is *{user_info['role']}*")
    st.write(f"Since *{user_info['register_date'].strftime('%d.%m.%Y')}*")
    st.markdown("---")

    display_admin_page(user_info)

    role_request(user_info)
    
    st.markdown("---")
    st.subheader(f"Your Actions")
    if not len(user_info['actions']):
        st.warning("No actions ...")
    for i in range(len(user_info['actions'])):
        st.markdown("---")
        user_book_actions = user_info['actions'][i]
        if user_book_actions['rating'] or \
            user_book_actions['comment_count'] or \
                user_book_actions['last_download_date']:
            st.subheader(f"- **{user_book_actions['title']}**")
        
        if user_book_actions['rating']:
            st.markdown(f"Rated it `{user_book_actions['rating']}/5` <small>at {user_book_actions['rated_at'].strftime('%d.%m.%Y')}</small>", unsafe_allow_html=True)
        
        if user_book_actions['comment_count']:
            st.markdown(f"left ```{user_book_actions['comment_count']}``` comments", unsafe_allow_html=True)
        
        if user_book_actions['last_download_date']:
            st.markdown(f"Downloaded at {user_book_actions['last_download_date'].strftime('%d.%m.%Y')}", unsafe_allow_html=True)




        







if __name__ == "__main__":
    profile_page()