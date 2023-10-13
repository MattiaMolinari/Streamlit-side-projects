import streamlit as st
import pandas as pd

# TITLE
st.title("New York City Airbnb Open Data")
# DESCRIPTION (saved in external file)
description = open("README.md")
st.markdown(description.read())
description.close()
st.divider()

# reading the dataset
df = pd.read_csv("NYC-airbnb-2019.csv")
# FILTERS
with st.container():
    st.header("Filters")
    # room
    room_type_option = pd.unique(df.room_type.values)
    room_type_select = st.multiselect(
        "Room type filter",
        (room_type_option),
        placeholder="Select room type",
    )
    # neighbourhood group filter
    neighbourhood_group_option = pd.unique(df.neighbourhood_group.values)
    neighbourhood_group_select = st.multiselect(
        "Neighbourhood group filter",
        (neighbourhood_group_option),
        placeholder="Select neighbourhood group",
    )
    # neighbourhood filter
    neighbourhood_option = pd.unique(
        df[df.neighbourhood_group.isin(neighbourhood_group_select)].neighbourhood.values
    )
    neighbourhood_select = st.multiselect(
        "Neighbourhood filter",
        (neighbourhood_option),
        placeholder="Select neighbourhood",
    )
    # price
    (min_price_option, max_price_option) = (min(df.price), max(df.price))
    (min_price_select, max_price_select) = st.slider(
        "Price range filter",
        min_value=min_price_option,
        max_value=max_price_option,
        value=(min_price_option, max_price_option),
        format="$ %f",
    )

# creating a copy of the dataframe with the possibility to select a row
df_select = df.copy()
df_select.insert(0, "select", value=False)


# appling filters
df_select = df_select[
    df_select.room_type.isin(room_type_select)
    & df_select.neighbourhood.isin(neighbourhood_select)
]
df_select = df_select[df_select.price >= min_price_select]
df_select = df_select[df_select.price <= max_price_select]


# WARNING IF NO MATCH FOUND, ELSE SHOWING LIST OR MAP
if len(df_select.index) == 0:
    st.warning("Sorry, no airbnb found")
else:
    st.metric("Unique airbnb found", value=len(df_select.index))

    airbnb_list, airbnb_map = st.tabs(["List", "Map"])
    with airbnb_list:
        # the dataframe with user selected rows is saved in a new varaible
        df_details = st.data_editor(
            df_select,
            hide_index=True,
            column_config={
                "select": st.column_config.CheckboxColumn(
                    "Select",
                    required=True,
                    help="Select airbnb and press the button to view details",
                ),
                "host_id": None,
                "id": None,
                "name": "Name",
                "host_name": "Host Name",
                "neighbourhood_group": None
                if len(neighbourhood_group_select) == 1
                else "Location",
                "neighbourhood": None
                if len(neighbourhood_select) == 1
                and len(neighbourhood_group_select) == 1
                else "Area",
                "latitude": None,
                "longitude": None,
                "room_type": None if len(room_type_select) == 1 else "Room type",
                "price": st.column_config.NumberColumn("Price (in USD)", format="$ %f"),
                "minimum_nights": st.column_config.NumberColumn(
                    "Minimum nights",
                    help="Minimum number of nights the place has to be booked",
                ),
                "number_of_reviews": None,
                "last_review": None,
                "reviews_per_month": None,
                "calculated_host_listings_count": None,
                "availability_365": st.column_config.ProgressColumn(
                    "Availability",
                    help="How many days per year the airbnb is available",
                    format="%d",
                    min_value=0,
                    max_value=365,
                ),
            },
            disabled=df.columns,
        )
        if st.button("See details"):
            df_details = df_details[df_details.select]
            df_details = df_details.drop("select", axis=1)
            if len(df_details.index) == 0:
                st.warning("Please select at least one airbnb")
            else:
                price_mean = df_details.price.mean()
                minimum_nights_min = df_details.minimum_nights.min()
                with st.expander("", expanded=True):
                    for index, row in df_details.iterrows():
                        st.subheader(f":blue[{row[1]}] - _{row.host_name}_")
                        st.markdown(
                            f"_:blue[{row.room_type}] located in {row.neighbourhood}, {row.neighbourhood_group}_"
                        )
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric(
                                "Price",
                                value=f"$ {row.price}",
                                delta=f"{(row.price - price_mean):.2f}",
                                delta_color="inverse",
                            )
                        with c2:
                            st.metric(
                                "Minimum nights number",
                                value=row.minimum_nights,
                                delta=row.minimum_nights - minimum_nights_min,
                                delta_color="inverse",
                            )
                        with c3:
                            st.metric(
                                "Host's number of listings",
                                value=row.calculated_host_listings_count,
                            )

                        c4, c5, c6 = st.columns(3)
                        with c4:
                            st.metric("Number of reviews", value=row.number_of_reviews)
                        with c5:
                            st.metric("Date of last review", value=row.last_review)
                        with c6:
                            st.metric("Review per month", value=row.reviews_per_month)
                        st.divider()

    with airbnb_map:
        st.map(
            df_details.replace(
                {
                    "room_type": {
                        "Private room": "#32a852",
                        "Entire home/apt": "#a83232",
                        "Shared room": "#3234a8",
                    }
                }
            ),
            latitude="latitude",
            longitude="longitude",
            # color="room_type",
        )
