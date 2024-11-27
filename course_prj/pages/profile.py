
import streamlit as st
from datetime import datetime
import os


from services.user import *
from services.error_handler import error_handler
from services.request import add_request
from services.book import get_categories

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

    if 'categories' not in st.session_state:
        st.session_state.categories = get_categories() + ['Unexisted category']

    if upload_book is not None:
        if upload_book.type != 'application/octet-stream':
            st.error("Wrong file format")
            return
        
        st.success(f"File {upload_book.name} uploaded")
        categories = st.multiselect("Select category(s)", st.session_state.categories)

        submit_button = st.button("Submit")

        if 'Unexisted category' in categories:
            new_category = st.text_input("Enter new category's name").strip()
            if st.button("Add new category") and len(new_category):
                category_id = services.book.add_category(new_category)
                if category_id is not None:
                    st.session_state.categories = st.session_state.categories[:-1] + [new_category] + [st.session_state.categories[-1]]
                    st.success(f"New category added: {new_category}")
                else:
                    st.error(f"Category {new_category} exists")

                new_category = ""

        if submit_button and len(categories) and 'Unexisted category' not in categories:
            book_id = services.book.add_book(upload_book, categories)
            if not book_id:
                st.error("Can't upload book")
            else:
                st.success(f"Book added to database with id {book_id}")
        else:
            if 'Unexisted category' in categories:
                st.info("Remove unexisted category from selected categories")
            else:
                st.info("Add some categories")

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



@error_handler
def show_dump_recovery() -> None:
    with st.sidebar:
        st.header("database recovery")
        # db_name = st.text_input("Enter database's name").strip()
        # user = st.text_input("Enter database user's name").strip()
        # password = st.text_input("Enter password", type="password").strip()

        recover_submit = st.button("Recover database")
        if recover_submit:
            # if 'db_name' not in st.session_state:
            #     st.session_state.db_name = db_name
                
            # if 'user_db' not in st.session_state:
            #     st.session_state.user_db = user

            # if 'password_db' not in st.session_state:
            #     st.session_state.password_db = password

            st.switch_page("pages/admin_panel.py")  

        # else:
        #     if auth_submit and not check_database_connection(db_name, user, password):
        #         st.error("Invalid auth to database")



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
            st.error(f"User-{new_admin_id} haven't sent request, cannot assign")
        else:
            st.success(f"New admin-{user_id} added")

    # '''
    #     Database recover
    # '''
    show_dump_recovery()




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