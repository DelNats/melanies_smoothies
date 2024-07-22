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
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+i)
# st.text(fruityvice_response.json())
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    # st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER )
            values ('""" + ingredient_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+ name_on_order+'!', icon="✅", )

# Importing info from fruityvice.com



#######################################

# option = st.selectbox(
#     "Select your favourite fruit?",
#     ("Apple", "Passion Fruit", "Blueberries"))

# st.write("Your selected Fruit is:", option)

# # Get the current credentials
# session = get_active_session()

# # Use an interactive slider to get user input
# hifives_val = st.slider(
#     "Number of high-fives in Q3",
#     min_value=0,
#     max_value=90,
#     value=60,
#     help="Use this to enter the number of high-fives you gave in Q3",
# )

# #  Create an example dataframe
# #  Note: this is just some dummy data, but you can easily connect to your Snowflake data
# #  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
# created_dataframe = session.create_dataframe(
#     [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
#     schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
# )

# # Execute the query and convert it into a Pandas dataframe
# queried_data = created_dataframe.to_pandas()

# # Create a simple bar chart
# # See docs.streamlit.io for more types of charts
# st.subheader("Number of high-fives")
# st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

# st.subheader("Underlying data")
# st.dataframe(queried_data, use_container_width=True)
