import plotly.express as px
import pandas as pd
import numpy as np

def select_continent(df):
    list_of_continents = df['Continent'].sort_values().unique().tolist()
    return list_of_continents

def select_country(df):
    list_of_countries = df['country'].sort_values().unique().tolist()
    list_of_countries.insert(0, 'India')
    list_of_countries.insert(1, 'China')
    list_of_countries.insert(2, 'United States')
    list_of_countries.insert(3, 'United Kingdom')
    list_of_countries.insert(4, 'Russia')
    list_of_countries.insert(5, 'France')
    list_of_countries.insert(6, 'Pakistan')
    return list_of_countries
