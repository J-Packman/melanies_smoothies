# Import python packages IDK WHAT VERSION THIS IS TBH
import streamlit as st
import os
from snowflake.snowpark.functions import col
import requests  

# Write directly to the app
st.title("🥤Customize Your Smoothie🥤")
st.write(
  """Choose the fruits you want in your custom Smothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on your Smothie will be:', name_on_order)


#    option = st.selectbox(
#        "What is your favourite fruit?",
#       ("Strawberries", "Mangos", "Peaches"),
#    )

#st.write("You selected:", option)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://www.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen)  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order +"""')"""

    time_to_insert = st.button('Submit Order')
    
    st.write(my_insert_stmt)
    #st.stop()
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")




        
