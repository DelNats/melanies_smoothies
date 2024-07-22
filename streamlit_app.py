# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":smile: Customise Your Smoothie! :snowflake:")
st.write(
    """Choose the fruit you want in your
    **custom** smoothie.
    """
)

name_on_order = st.text_input('Name on Smoothie')

# session = get_active_session() 

cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# convert the Snowflake DF to a Pandas DF in order to use the LOC function
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredient_lit =  st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5);

if ingredient_lit:
    # st.write(ingredient_lit);
    # st.text(ingredient_lit);

    ingredient_string =''
    for i in ingredient_lit:
        ingredient_string += i+' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == i, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', i,' is ', search_on, '.')

        st.subheader(i + 'Nutrition information')
        
# Importing info from fruityvice.com
        # removing response based on fruit ID
        # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+i)
        # adding response based on SEARCH_ON
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+'SEARCH_ON')
        # st.text(fruityvice_response.json())
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER )
            values ('""" + ingredient_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order+'!', icon="✅", )





