"""
Name:       Andrew Orser
CS230:      2
Data:       English Pubs
URL:        couldn't get this to work

Description:

This program allows you to pick a region of england to visit and pick bars from the area.
It will also give you their addresses and allow you to compare the distance between two  different bars.
The bars you select will be shown as different percents of the total bars in the region and in all of england.

"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import cos, asin, sqrt, pi
# import pydeck as pdk
# import random as rd

# distance function


def dist(lat1, lon1, lat2, lon2):
    x = pi/180
    y = 0.5 - cos((lat2-lat1)*x)/2 + cos(lat1*x) * cos(lat2*x) * (1-cos((lon2-lon1)*x))/2
    # convert to km where 12742 is the earth's diameter in km
    return 12742 * asin(sqrt(y))


# Set title:
st.title("English Pub Visitation Tool")

# What app does:

st.write("Use this tool to help you plan your next visit to England!")

# import Data
pub_data = pd.read_csv("open_pubs_8000_sample.csv")

# pub_data = pub_data.sort_values(by=['local_authority'], ascending=True)

map_main = st.empty()
map_main.map(pub_data)
sel_cont = st.container()
sel_cont.header("Your Current Selections:")

# Create Sidebar:
st.sidebar.header("Search Options")

# List Local Areas:

pub_auth = pub_data.local_authority.unique()
auth_choice = st.sidebar.selectbox("What region would you like visit?", pub_auth)
if auth_choice != "Please Select a Region":
    st.sidebar.write(f"So you want to explore pubs in {auth_choice}? Ok, let's narrow that down a bit. . .")
    sel_cont.write(f"REGION: {auth_choice}")
    st.sidebar.write()
    local_pubs = pub_data[pub_data["local_authority"] == auth_choice][["name", "address", "latitude", "longitude"]]
    map_main.map(local_pubs)
    st.sidebar.write("Would you like to know the addresses?")
    sel_key_y = st.sidebar.checkbox("Yes")
    sel_key_n = st.sidebar.checkbox("No")
    if sel_key_y:
        sel_key_n = 0
        st.sidebar.write(f"OK, We can provide that for you.")
        st.sidebar.write()
        pub_select = st.sidebar.multiselect("Please select the pubs you are interested in:", local_pubs)
        if pub_select != "Please Select a Pub":
            sel_cont.write(f"PUBS SELECTED: ")
            st.sidebar.write()
            db_pub_select = local_pubs[(local_pubs.name.isin(pub_select))][["name", "address", "latitude", "longitude"]]
            map_main.map(db_pub_select)
            if len(db_pub_select) >= 1:
                # change index
                db_pub_show = db_pub_select
                db_pub_show = db_pub_show.reset_index(drop=True)
                db_pub_show.index = np.arange(1, len(db_pub_show)+1)
                # drop  lat/long
                db_pub_show = db_pub_show.drop(["latitude", "longitude"], axis=1)
                # Display Options
                sel_cont.write(db_pub_show)
                dist_select = st.sidebar.multiselect("Select any two pubs you want to know the distance between:", db_pub_select)
                db_dist_select = db_pub_select[(db_pub_select.name.isin(dist_select))][["name", "address", "latitude", "longitude"]]
                db_dist_select = db_dist_select.reset_index(drop=True)
                calc = st.sidebar.button("Calculate!", disabled=False)
                if calc:
                    if len(dist_select) == 1:
                        st.sidebar.warning("You have to pick at lease two pubs to compare")

                    elif len(dist_select) <= 2:
                        pub1 = db_dist_select.at[0, "name"]
                        pub2 = db_dist_select.at[1, "name"]
                        a = db_dist_select.at[0, "latitude"]
                        b = db_dist_select.at[0, "longitude"]
                        c = db_dist_select.at[1, "latitude"]
                        d = db_dist_select.at[1, "longitude"]
                        kms = round(dist(a, b, c, d), 2)
                        st.sidebar.write(f"The distance between {pub1} and {pub2} is {kms} kms")
                    else:
                        st.sidebar.warning("You can only pick two pubs to compare, i'm not that good at programming")
                # Bar Graphs (Pies, actually)
                # number of bars/selected
                tot = len(pub_data)
                auth = len(local_pubs)
                sel = len(db_pub_show)

                # lists for labels/charts
                bar_in_area = [tot, auth]
                lab1 = ["All pubs in England", "Pubs in this Municipality"]
                bar_visit_eng = [tot, sel]
                lab2 = ["All pubs in England", "What you will visit"]
                bar_visit_area = [auth, sel]
                lab3 = ["Pubs in this Municipality", "What you will visit"]

                # Figures
                fig, ax = plt.subplots()
                ax.pie(bar_in_area, labels=lab1, autopct="%.2f%%")
                st.pyplot(fig)

                fig, ax = plt.subplots()
                ax.pie(bar_visit_eng, labels=lab2, autopct="%.2f%%")
                st.pyplot(fig)

                fig, ax = plt.subplots()
                ax.pie(bar_visit_area, labels=lab3, autopct="%.2f%%")
                st.pyplot(fig)

    if sel_key_n:
        sel_key_y = 0
        st.sidebar.write()
        pub_select = st.sidebar.multiselect("Please select the pubs you are interested in:", local_pubs)
        if pub_select != "Please Select a Pub":
            sel_cont.write(f"PUBS SELECTED: ")
            st.sidebar.write()
            db_pub_select = local_pubs[(local_pubs.name.isin(pub_select))][["name", "address", "latitude", "longitude"]]
            map_main.map(db_pub_select)
            if len(db_pub_select) >= 1:
                # change index
                db_pub_show = db_pub_select
                db_pub_show = db_pub_show.reset_index(drop=True)
                db_pub_show.index = np.arange(1, len(db_pub_show)+1)
                # drop  lat/long
                db_pub_show = db_pub_show.drop(["address", "latitude", "longitude"], axis=1)
                # Display Options
                sel_cont.write(db_pub_show)
                dist_select = st.sidebar.multiselect("Select any two pubs you want to know the distance between:", db_pub_select)
                db_dist_select = db_pub_select[(db_pub_select.name.isin(dist_select))][["name", "address", "latitude", "longitude"]]
                db_dist_select = db_dist_select.reset_index(drop=True)
                calc = st.sidebar.button("Calculate!", disabled=False)
                if calc:
                    if len(dist_select) == 1:
                        st.sidebar.warning("You have to pick at lease two pubs to compare")

                    elif len(dist_select) <= 2:
                        pub1 = db_dist_select.at[0, "name"]
                        pub2 = db_dist_select.at[1, "name"]
                        a = db_dist_select.at[0, "latitude"]
                        b = db_dist_select.at[0, "longitude"]
                        c = db_dist_select.at[1, "latitude"]
                        d = db_dist_select.at[1, "longitude"]
                        kms = round(dist(a, b, c, d), 2)
                        st.sidebar.write(f"The distance between {pub1} and {pub2} is {kms} kms")
                    else:
                        st.sidebar.warning("You can only pick two pubs to compare, i'm not that good at programming")

                # Bar Graphs (Pies, actually)
                # number of bars/selected
                tot = len(pub_data)
                auth = len(local_pubs)
                sel = len(db_pub_show)

                # lists for labels/charts
                bar_in_area = [tot, auth]
                lab1 = ["All pubs in England", "Pubs in this Municipality"]
                bar_visit_eng = [tot, sel]
                lab2 = ["All pubs in England", "What you will visit"]
                bar_visit_area = [auth, sel]
                lab3 = ["Pubs in this Municipality", "What you will visit"]

                # Figures
                fig, ax = plt.subplots()
                ax.pie(bar_in_area, labels=lab1, autopct="%.2f%%")
                st.pyplot(fig)

                fig, ax = plt.subplots()
                ax.pie(bar_visit_eng, labels=lab2, autopct="%.2f%%")
                st.pyplot(fig)

                fig, ax = plt.subplots()
                ax.bar(bar_visit_area, labels=lab3, autopct="%.2f%%")
                st.pyplot(fig)
