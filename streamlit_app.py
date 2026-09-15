# Import Python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col


# App title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write(
    """Customize your smoothie by choosing up to 5 ingredients."""
)


# Name input
name_on_order = st.text_input("Name on Smoothie:")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)


# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()


# Get fruit options from Snowflake
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col("FRUIT_NAME"))


# Ingredient selector
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)


# Process smoothie order
if ingredients_list:

    # Create a string containing the selected ingredients
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "


    # Call SmoothieFroot API
    smoothiefroot_response = requests.get(
        "https://smoothiefroot.com/api/fruit/watermelon",
        headers={
            "Accept": "application/json"
        }
    )


    # Check for HTTP errors
    smoothiefroot_response.raise_for_status()


    # Display Fruit API response
    st.write("Fruit API response:")
    st.json(smoothiefroot_response.json())


    # Insert order into Snowflake
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES (?, ?)
    """


    session.sql(
        my_insert_stmt,
        params=[
            ingredients_string,
            name_on_order
        ]
    ).collect()


    # Confirmation
    st.success(
        "Your Smoothie is ordered!",
        icon="✅"
    )
    
