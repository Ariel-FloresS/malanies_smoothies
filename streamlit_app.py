# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests


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
my_dataframe = sesion.table("smoothies.public.fruit_options").select(col("Fruit_NAME"),col("SEARCH_ON"))}
pd_df=my_dataframe.to_pandas()
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
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_choosen+'Nutricional Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    my_insert_stmt = """ INSERT INTO smoothies.public.orders(ingredients,name_on_order)
            VALUES ('""" + ingredients_string +"""','"""+name_on_order+"""')"""
    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        sesion.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!, '+name_on_order, icon="✅")


