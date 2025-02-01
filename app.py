import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("vehicles_us.csv")

# App title
st.title("🚗 Analysis of Car Sales in the USA")

# --- CHART 1: PRICE DISTRIBUTION ---
if st.checkbox("Show price distribution of cars"):
    st.header("📊 Price Distribution of Cars")

    # Checkboxes for selecting car condition
    conditions = df["condition"].dropna().unique()
    selected_conditions = st.multiselect(
        "Select car condition(s)", options=conditions, default=conditions
    )

    # Filter data by selected condition
    if selected_conditions:
        df_filtered = df[df["condition"].isin(selected_conditions)]
    else:
        df_filtered = df

    # Create histogram
    fig_price = px.histogram(
        df_filtered, x="price", nbins=50,
        title=f"Price Distribution of Cars ({', '.join(selected_conditions)})",
        labels={"price": "Price ($)", "count": "Number of Listings"},
        color_discrete_sequence=["royalblue"]
    )

    # Customize chart
    fig_price.update_layout(
        xaxis_title="Price ($)",
        yaxis_title="Number of Listings",
        xaxis=dict(range=[0, 60000]),
        bargap=0.05,
        template="plotly_white",
        height=600
    )

    # Display chart
    st.plotly_chart(fig_price)

# --- CHART 2: POPULARITY OF CAR TYPES ---
if st.checkbox("Show popularity of car types"):
    st.header("🚘 Popularity of Car Types")

    # Count listings by car type and sort
    type_counts = df["type"].value_counts().reset_index()
    type_counts.columns = ["type", "count"]
    type_counts = type_counts.sort_values(by="count", ascending=False)

    # Checkbox to show only the top 5 car types
    show_top_5 = st.checkbox("Show Only Top 5 Car Types", help="Toggle to show only the 5 most common car types")

    if show_top_5:
        type_counts = type_counts.head(5)

    # Create bar chart
    fig_type = px.bar(
        type_counts, x="count", y="type", orientation="h",
        title="Popularity of Car Types",
        labels={"count": "Number of Listings", "type": "Car Type"},
        color_discrete_sequence=["royalblue"],
        text="count"
    )

    # Customize chart
    fig_type.update_layout(
        xaxis_title="Number of Listings",
        yaxis_title="Car Type",
        template="plotly_white",
        xaxis=dict(range=[0, max(type_counts["count"]) * 1.1]),
        yaxis=dict(categoryorder="total ascending"),
        height=600,
        bargap=0.1
    )

    # Display chart
    st.plotly_chart(fig_type)

# --- CHART 3: PRICE VS. ODOMETER ---
if st.checkbox("Show price vs. odometer"):
    st.header("💰 Price vs. Odometer")

    # Filter outliers
    df_filtered_odometer = df[(df["price"] <= 100000) & (df["odometer"] <= 400000)]

    # Create scatter plot
    fig_scatter = px.scatter(
        df_filtered_odometer, x="odometer", y="price",
        title="Price vs. Odometer",
        labels={"odometer": "Odometer (miles)", "price": "Price ($)"},
        color_discrete_sequence=["royalblue"],
        opacity=0.5
    )

    # Customize chart
    fig_scatter.update_layout(
        xaxis_title="Odometer (miles)",
        yaxis_title="Price ($)",
        template="plotly_white",
        height=600,
        width=800
    )

    # Display chart
    st.plotly_chart(fig_scatter)
