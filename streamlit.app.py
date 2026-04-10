# Import python packages.

import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(f" :cup_with_straw: Customize you Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name of Smoothie",)
st.write('The name on your Smoothie will be:', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")

Ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    [row['FRUIT_NAME'] for row in my_dataframe.select(col('FRUIT_NAME')).collect()]
)

if Ingredients_list:
    ingredients_string = ''

    for fruit_chosen in Ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    if ingredients_string:
        time_to_insert = st.button('Submit Order')
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success(name_on_order + ', Your Smoothie is ordered!', icon="✅")
