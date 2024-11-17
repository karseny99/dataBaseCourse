import pandas as pd
import psycopg2
import psycopg2.extras
import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'search_request' not in st.session_state:
    st.session_state.search_request = ""


def main() -> None:

    if not(st.session_state.logged_in):
        st.title("You need to log in")
        st.session_state.logged_in = False

        reg_button = st.button("Register")
        login_button = st.button("log in")

        if reg_button:
            st.switch_page("pages/register.py")
        if login_button:
            st.switch_page("pages/login.py")

    else:
        st.title("Open Library")
        search_request = st.text_input("Enter book's name").strip()
        search_button = st.button("🔎")

        search_by_title = st.checkbox("Search by title")
        search_by_isbn = st.checkbox("Search by ISBN")
        search_by_author = st.checkbox("Search by author")

        if search_button:
            if len(search_request):
                search_columns = []
                if search_by_title:
                    search_columns.append("title")
                if search_by_author:
                    search_columns.append("author")
                if search_by_isbn:
                    search_columns.append("isbn")

                if len(search_columns) == 0:
                    st.error("At least one column must be selected")
                else:
                    st.session_state.search_request = [search_request, search_columns]
                    st.switch_page("pages/search.py")
                    st.write(f"Searching for {search_request}")
            else:
                st.error("Invalid book's name")



if __name__ == "__main__":
    main()
    

# # @st.cache_data
# def get_products() -> dict[str, str]:
#     print("Получение продуктов")
#     query = "SELECT barcode, name FROM products;"
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
#             cur.execute(query)
#             products = cur.fetchall()

#     return {product["name"]: product["barcode"] for product in products}


# def add_sale(sale_date: date) -> int:
#     query = """
#         INSERT INTO sales (sale_date)
#         VALUES (%(sale_date)s) RETURNING sale_id;
#     """
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor() as cur:
#             cur.execute(query, {"sale_date": sale_date})
#             return cur.fetchone()[0]


# def add_sale_details(sales: pd.DataFrame) -> None:
#     query = """
#         INSERT INTO sales_details (sale_id, barcode, quantity)
#         VALUES (%s, %s, %s);
#     """
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor() as cur:
#             cur.executemany(
#                 query,
#                 sales[["sale_id", "barcode", "quantity"]].itertuples(
#                     index=False, name=None
#                 ),
#             )


# products = get_products()

# # Хранение добавленных товаров в таблице
# if "sales_table" not in st.session_state:
#     st.session_state.sales_table = pd.DataFrame(
#         columns=["Название продукта", "Barcode", "Количество"]
#     )


# st.title("Продажа продуктов")

# # Поля для ввода данных
# selected_product = st.selectbox("Выберите продукт", products.keys())
# quantity = st.number_input("Количество", min_value=1, max_value=100, value=1)

# # кнопки
# add_product_btn = st.button("Добавить продукт")
# clear_table_btn = st.button("Очистить таблицу")
# apply_btn = st.button("Подтвердить продажу")


# def add_product(product_name, product_barcode, product_quantity):
#     new_row = pd.DataFrame(
#         {
#             "Название продукта": [product_name],
#             "Barcode": [product_barcode],
#             "Количество": [product_quantity],
#         }
#     )
#     st.session_state.sales_table = pd.concat(
#         [st.session_state.sales_table, new_row], ignore_index=True
#     )


# def clear_table():
#     st.session_state.sales_table = pd.DataFrame(
#         columns=["Название продукта", "Barcode", "Количество"]
#     )
#     # st.rerun()


# def upload_sales(sales_table: pd.DataFrame) -> int:
#     items = sales_table.rename(columns={"Количество": "quantity", "Barcode": "barcode"})
#     items = items.groupby("barcode", as_index=False)["quantity"].sum()
#     sale_id = add_sale(date.today())

#     items["sale_id"] = sale_id
#     add_sale_details(items)

#     return sale_id


# # event handlers
# if add_product_btn:
#     add_product(selected_product, products[selected_product], quantity)

# if clear_table_btn:
#     clear_table()

# if apply_btn and len(st.session_state.sales_table) > 0:
#     sale_id = upload_sales(st.session_state.sales_table)
#     st.success(f"Продажа добавлена успешно! ID чека: {sale_id}")
#     clear_table()

# st.write("Добавленные товары:")
# st.dataframe(st.session_state.sales_table)