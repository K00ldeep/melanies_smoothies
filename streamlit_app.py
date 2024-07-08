# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie !! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie !!
    """
)


Name_On_Order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be :", Name_On_Order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col(search_on))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list=st.multiselect(
'Choose upto 5 ingredients :'
, my_dataframe
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+ ' '
        st.subheader(fruit_chosen+ ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + Name_On_Order + """')"""
    time_to_insert=st.button("Submit Order")
    #st.write(my_insert_stmt)
    #st.stop
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered'+' '+Name_On_Order+' !!', icon="✅")

