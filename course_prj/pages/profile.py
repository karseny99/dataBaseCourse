
import streamlit as st
from datetime import datetime
import os


from services.user import *
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


def book_uploading() -> None:
    upload_book = st.file_uploader("Choose book's file", type=["fb2"], accept_multiple_files=False)
    upload_cover = st.file_uploader("Choose cover's file (jpg)", type=["jpg"], accept_multiple_files=False)
    
    if upload_book is not None:
        if upload_book.type != 'application/octet-stream':
            st.error("Wrong file format")
            return
        
        st.success(f"File {upload_book.name} uploaded")

        if upload_cover is not None:
            st.success(f"File {upload_cover.name} uploaded")
        else:
            st.info("Cover wasn't uploaded")

        book_item = {
            "title": st.text_input("Enter book's name").strip(),
            "published_year": st.number_input("Enter publishing year", step=1, max_value=datetime.now().year),
            "isbn": st.text_input("Enter ISBN").strip(),
            "description": st.text_input("Enter book's description").strip(),
            "file_path": None,
            "cover_image_path": None,
            "authors": st.text_input("Enter author(s) - split by , if more then one").strip().split(','),
            "categories": st.text_input("Enter category(s) - split by , if more then one").strip().split(',')
        }

        submit_button = st.button("Submit book's data")

        if submit_button \
            and len(book_item['title']) \
            and len(book_item['published_year']) \
            and len(book_item['isbn']) \
            and len(book_item['authors']) \
            :
            path_list = services.book.load_to_storage(upload_book, upload_cover)
            book_item['file_path'] = path_list[0]
            if len(path_list) > 1: book_item['cover_image_path'] = path_list[1]

            st.success(f"Book added to database with id {services.book.add_book(book_item)}")

            if st.button("Upload more"):
                st.rerun() 
        else:
            if submit_button:
                st.error("You didn't fill important fiels")


def admin_requests() -> None:

    file_path = get_info_data_file()

    with open(file_path) as data_file:
        if st.download_button(
                label="Download user's data",
                data=data_file,
                file_name=f"{file_path}",
                mime="application/x-fictionbook",
                on_click=remove_file(file_path)
            ) :
            st.success("Downloaded")


def show_dump_save() -> None:
    with st.sidebar:
        st.header("database dump")
        db_name = st.text_input("Enter database's name").strip()
        user = st.text_input("Enter database user's name").strip()
        password = st.text_input("Enter password", type="password").strip()

        auth_submit = st.button("Submit entered data")
        if auth_submit and len(db_name) and len(user) and len(password):
            filename = create_database_dump(db_name, user, password)
            if not filename:
                st.error("Wrong entered data")
            else:
                with open(filename, 'rb') as db_dump:
                    if st.download_button(
                            label="Download db_dump",
                            data=db_dump,
                            file_name=f"{os.path.basename(filename)}",
                            mime="application/octet-stream"
                        ) :
                        st.success("Downloaded")


def display_admin_page(user_info: dict) -> None:

    if user_info['role'] != 'admin':
        return
    
    # '''
    #     Book uploading part
    # '''
    book_uploading()

    # '''
    #     Admin requests
    # '''
    show_admin_requests = st.button("Show admin-requests")
    if show_admin_requests:
        st.info("Here is the data about user's who requested admin role")
        admin_requests()
  
    new_admin_id = st.number_input("Enter user_id to add admin role for him", step=1, min_value=1)

    if st.button(f"Approve admin for user"):
        
        user_id = set_admin_role(new_admin_id)

        if not user_id:
            st.error(f"Cannot assign admin to unexisted person-{new_admin_id}")
        else:
            st.success(f"New admin-{user_id} added")

    # '''
    #     Database dump
    # '''
    show_dump_save()




@error_handler
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
    if len(user_info.get('actions', [])) == 0:
        st.warning("No actions ...")
    else:
        for i in range(len(user_info['actions'])):
            st.markdown("---")
            user_book_actions = user_info['actions'][i]
            if user_book_actions['rating'] or \
                user_book_actions['comment_count'] or \
                    user_book_actions['last_download_date']:
                st.subheader(f"- **{user_book_actions['title']}**")
            else:
                continue


            if user_book_actions['rating']:
                st.markdown(f"Rated it `{user_book_actions['rating']}/5` <small>at {user_book_actions['rated_at'].strftime('%d.%m.%Y')}</small>", unsafe_allow_html=True)
            
            if user_book_actions['comment_count']:
                st.markdown(f"left ```{user_book_actions['comment_count']}``` comments", unsafe_allow_html=True)
            
            if user_book_actions['last_download_date']:
                st.markdown(f"Downloaded at {user_book_actions['last_download_date'].strftime('%d.%m.%Y')}", unsafe_allow_html=True)




        







if __name__ == "__main__":
    profile_page()