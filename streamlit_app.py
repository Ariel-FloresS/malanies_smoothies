# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)
name_on_order=st.text_input("Name on Smoothie:!")
st.write("The name on your smoothie will be:",name_on_order)

cnx=st.connection("snowflake")
sesion = cnx.session()
my_dataframe = sesion.table("smoothies.public.fruit_options").select(col("Fruit_NAME"))
#st.dataframe(my_dataframe, use_container_width=True)
ingredients_list=st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    ingredients_string=''
    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen+" "
    my_insert_stmt = """ INSERT INTO smoothies.public.orders(ingredients,name_on_order)
            VALUES ('""" + ingredients_string +"""','"""+name_on_order+"""')"""
    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        sesión.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!, '+name_on_order, icon="✅")
