import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import helper



# ------------------------------------------------------------------------------------------------------------

csv_file='Final_electricity_data.csv'
df = pd.read_csv(csv_file)
df['Electricity_per_capita']=round((df['electricity_generation']*1000000000)/df['population'],2)
df['year']=df['year'].astype(str)
# --------------------------------------------------------------------------------------------------------------

st.set_page_config(layout='wide')
list_of_continents=df['Continent'].sort_values().unique().tolist()
list_of_continents.insert(0,'Overall')
list_of_countries=df['country'].sort_values().unique().tolist()
list_of_countries.insert(0,'Overall')
year=df['year'].sort_values(ascending=False).unique().tolist()
year.insert(0,'Overall')

st.sidebar.image('P2.jpg',width=250)
st.sidebar.title('Worldwide Electricity Generation Stats')

User_Menu=st.sidebar.radio('SELECT OPTION',('Worldwide','Continent Wise','Country Wise'))

Year = st.sidebar.selectbox('SELECT YEAR', year)

# --------------------------------------------------------------------------------------------------------(0)

# A1) -->
if User_Menu == 'Worldwide' and Year=='Overall':
    st.header("Worldwide Electricity Stats")
    st.markdown("""*****""")
    st.subheader('Electricity That Mostly Produced From --')
    x1=df.groupby('country')['coal_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x2=df.groupby('country')['gas_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x3=df.groupby('country')['oil_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x4=df.groupby('country')['nuclear_electricity'].sum().sort_values(ascending=False).head(1).index[0]

    y1=df.groupby('country')['hydro_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y2=df.groupby('country')['solar_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y3=df.groupby('country')['wind_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y4=df.groupby('country')['biofuel_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1 :
        st.info('Coal Electricity')
        st.subheader(x1)
    with col2 :
        st.info('Gas Electricity')
        st.subheader(x2)
    with col3 :
        st.info('Oil Electricity')
        st.subheader(x3)
    with col4 :
        st.info('Nuclear Electricity')
        st.subheader(x4)
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.info('Hydro Electricity')
        st.subheader(y1)
    with col2:
        st.info('Solar Electricity')
        st.subheader(y2)
    with col3:
        st.info('Wind Electricity')
        st.subheader(y3)
    with col4:
        st.info('Biofuel Electricity')
        st.subheader(y4)
    st.markdown("""***""")

    
# A1.1) -->
    Electricity_generation_YearWise=df.groupby('year')['electricity_generation'].sum().reset_index()
    fig = px.line(Electricity_generation_YearWise, x='year', y='electricity_generation',labels=({'year':'Year','electricity_generation':'Electricity Generation in (GWH)'}),markers='year',title='Electricity Generation over the Year')

# A1.2)-->
    Worldwise = df[['non_renewable_electricity', 'renewable_electricity']].sum().reset_index()
    Worldwise.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    #Worldwise_Electricity = Worldwise['Percentage'].sum()
    # Worldwise['Percentage'] = round((Worldwise['Percentage'] / Worldwise_Electricity) * 100, 2)
    Worldwide_fig2 = px.pie(Worldwise, values='Percentage', color='Electricity',
                            title='Renewable Vs Non-Renewable Share',hole=0.4)

# A1.3) -->
    Worldwiswe_Non_Renewable = df[
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity']].sum().reset_index()
    Worldwiswe_Non_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)

    Total_Non_Renewable = Worldwiswe_Non_Renewable['Percentage'].sum()
    Worldwiswe_Non_Renewable['Percentage'] = round((Worldwiswe_Non_Renewable['Percentage'] / Total_Non_Renewable) * 100,
                                                  2)
    Worldwide_fig3 = px.bar(Worldwiswe_Non_Renewable, x='Electricity', y='Percentage', color='Electricity',
                            text='Percentage', title='Non Renewable Electricity Share')
# A1.4) -->
    Worldwiswe_Renewable = df[['hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity',
                               'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    Worldwiswe_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Renewable = Worldwiswe_Renewable['Percentage'].sum()
    Worldwiswe_Renewable['Percentage'] = round((Worldwiswe_Renewable['Percentage'] / Total_Renewable) * 100, 2)
    Worldwide_fig4 = px.bar(Worldwiswe_Renewable, x='Electricity', y='Percentage', color='Electricity', text='Percentage',
                            title='Renewable Electricity Share')
# A1.5) -->
    Electricity_per_capita = df[['year', 'electricity_generation', 'population']].groupby('year')[
        ['electricity_generation', 'population']].sum().reset_index()
    Electricity_per_capita['Electricity_per_capita'] = (Electricity_per_capita['electricity_generation'] * 1000000000 / \
                                                       Electricity_per_capita['population'])
    Worldwide_fig5 = px.line(Electricity_per_capita, x='year', y='Electricity_per_capita', markers='year',
                             labels=({'year': 'Year','Electricity_per_capita':'Electricity Per Capita (KWH)'}),title='Electricity Per Capita')

# A1.6)--->

# A1.7) -->
    Electricity_by_other = df.groupby('year')[[
        'coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity', 'hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity', 'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    Worldwide_fig6 = px.line(Electricity_by_other, x='year',
                             y=['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity',
                                'hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity',
                                'other_renewable_exc_biofuel_electricity'],
                             labels=({'year': 'Year', 'value': 'Electricity in (GWH)'}),title='Electricity Generation Over The Year')
# A1.8) -->
    Worldwiswe_fossile = df[['fossile_electricity', 'Non_fossile_electricity']].sum().reset_index()
    Worldwiswe_fossile.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    #Total_fossile = Worldwiswe_fossile['Percentage'].sum()
    #Worldwiswe_fossile['Percentage'] = round((Worldwiswe_fossile['Percentage'] / Total_fossile) * 100, 2)
    Worldwide_fig7 = px.pie(Worldwiswe_fossile, values='Percentage', color='Electricity',
                            title='Fossil Vs Non Fossil Electricity Share',hole=0.4)

    Demand_vs_supply = df.groupby('year')[['electricity_generation', 'electricity_demand']].sum().reset_index()
    Wordwide_fig8 = px.line(Demand_vs_supply, x='year', y=['electricity_generation', 'electricity_demand'],
                            markers='year', labels=({'year': 'Year', 'value': 'Electricity in GWH'}),title='Electricity Generation vs Demand Curve')




# Vis --> 1(A)
    st.plotly_chart(fig)
    st.plotly_chart(Worldwide_fig6)
    st.plotly_chart(Worldwide_fig5)
    st.plotly_chart(Worldwide_fig2)
    st.plotly_chart(Worldwide_fig3)
    st.plotly_chart(Worldwide_fig4)
    st.plotly_chart(Worldwide_fig7)
    st.plotly_chart(Wordwide_fig8)
    
# ------------------------------------------------------------------------------------------------------------(1)
# B1) --->
if User_Menu == 'Worldwide' and Year!='Overall':
    st.header(f'Worldwide Electricity Stats in {Year}')
    st.markdown("""***""")
    st.subheader('Electricity That Mostly Produced From --')
    x1 = df[df['year'] == Year].groupby('country')['coal_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x2 = df[df['year'] == Year].groupby('country')['gas_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x3 = df[df['year'] == Year].groupby('country')['oil_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x4 = df[df['year'] == Year].groupby('country')['nuclear_electricity'].sum().sort_values(ascending=False).head(1).index[0]

    y1 = df[df['year'] == Year].groupby('country')['hydro_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y2 = df[df['year'] == Year].groupby('country')['solar_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y3 = df[df['year'] == Year].groupby('country')['wind_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y4 = df[df['year'] == Year].groupby('country')['biofuel_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info('Coal Electricity')
        st.subheader(x1)
    with col2:
        st.info('Gas Electricity')
        st.subheader(x2)
    with col3:
        st.info('Oil Electricity')
        st.subheader(x3)
    with col4:
        st.info('Nuclear Electricity')
        st.subheader(x4)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info('Hydro Electricity')
        st.subheader(y1)
    with col2:
        st.info('Solar Electricity')
        st.subheader(y2)
    with col3:
        st.info('Wind Electricity')
        st.subheader(y3)
    with col4:
        st.info('Biofuel Electricity')
        st.subheader(y4)
    st.markdown("""***""")

    x=round(df[df['year']==Year]['electricity_generation'].sum()*1000000000/df[df['year']==Year]['population'].sum())
    y = round(df[df['year'] == Year]['electricity_generation'].sum(),2)
    col1, col2= st.columns(2)
    with col1 :
        st.info(f'Electricity per Capita in {Year}')
        st.write(x,'Kwh')
    with col1:
        st.info(f'Total Electricity Generation in {Year}')
        st.write(y,'Gwh')
    st.markdown("""***""")
# B1.1) -->
    tally=df[df['year']==Year]
    Electrity_by_year = df[df['year'] == Year][
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity', 'hydro_electricity',
         'solar_electricity', 'biofuel_electricity', 'wind_electricity',
         'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    fig1 = px.bar(Electrity_by_year, x='index', y=0,labels=({'index':'Electricity Mode','0':'Value in GWH'}),color='index',title=f'Electricity Production by Year {Year}  ')

# B1.2) -->
    Country_wise = df[df['year'] == Year][['non_renewable_electricity', 'renewable_electricity']].sum().reset_index()
    Country_wise.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    #Total_Electricity = Country_wise['Percentage'].sum()
    #Country_wise['Percentage'] = round((Country_wise['Percentage'] / Total_Electricity) * 100, 2)
    fig2 = px.pie(Country_wise,  values='Percentage', color='Electricity',title='Renewable Vs Non_Renewable Electricity Share',hole=0.4)
# B1.3) -->
    Non_Renewable = df[df['year'] == Year][
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity']].sum().reset_index()
    Non_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Non_Renewable = Non_Renewable['Percentage'].sum()
    Non_Renewable['Percentage'] = round((Non_Renewable['Percentage'] / Total_Non_Renewable) * 100, 2)
    fig3 = px.bar(Non_Renewable, x='Electricity', y='Percentage', color='Electricity', text='Percentage',
                  title='Non_Renewable Electricity Share')
# B1.4) -->
    Renewable = df[df['year'] == Year][
        ['hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity',
         'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Renewable = Renewable['Percentage'].sum()
    Renewable['Percentage'] = round((Renewable['Percentage'] / Total_Renewable) * 100, 2)
    fig4 = px.bar(Renewable, x='Electricity', y='Percentage', color='Electricity', text='Percentage',
                  title='Renewable Electricity Share')
# B1.5) -->
    Worldwiswe_fossile = df[df['year'] == Year][
        ['fossile_electricity', 'Non_fossile_electricity']].sum().reset_index()
    Worldwiswe_fossile.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    #Total_fossile = Worldwiswe_fossile['Percentage'].sum()
    #Worldwiswe_fossile['Percentage'] = round((Worldwiswe_fossile['Percentage'] / Total_fossile) * 100, 2)
    Worldwide_fig7 = px.pie(Worldwiswe_fossile, values='Percentage', color='Electricity',
                            title='Fossil Vs Non Fossil Electricity Share',hole=0.4)


    # Vis B1) --->

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
    st.plotly_chart(Worldwide_fig7)

# -------------------------------------------------------------------------------------------------------------(2)

# 3) -----> Continent Wise
if User_Menu=='Continent Wise' :
    Ocean=helper.select_continent(df)
    Continent=st.sidebar.selectbox('SELECT CONTINENT',Ocean)

if User_Menu=='Continent Wise' and Year=='Overall' and Continent!='Overall':
    st.header(f'Electricity Stats of {Continent}')
    st.markdown("""***""")
    st.subheader('Electricity That Mostly Produced From --')
    x1 = df[df['Continent'] == Continent].groupby('country')['coal_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x2 = df[df['Continent'] == Continent].groupby('country')['gas_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x3 = df[df['Continent'] == Continent].groupby('country')['oil_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x4 = df[df['Continent'] == Continent].groupby('country')['nuclear_electricity'].sum().sort_values(ascending=False).head(1).index[0]

    y1 = df[df['Continent'] == Continent].groupby('country')['hydro_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y2 = df[df['Continent'] == Continent].groupby('country')['solar_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y3 = df[df['Continent'] == Continent].groupby('country')['wind_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y4 = df[df['Continent'] == Continent].groupby('country')['biofuel_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info('Coal Electricity')
        st.subheader(x1)
    with col2:
        st.info('Gas Electricity')
        st.subheader(x2)
    with col3:
        st.info('Oil Electricity')
        st.subheader(x3)
    with col4:
        st.info('Nuclear Electricity')
        st.subheader(x4)
    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.info('Hydro Electricity')
        st.subheader(y1)
    with col2:
        st.info('Solar Electricity')
        st.subheader(y2)
    with col3:
        st.info('Wind Electricity')
        st.subheader(y3)
    with col4:
        st.info('Biofuel Electricity')
        st.subheader(y4)
    st.markdown("""***""")
#1 --->
    Electricity_generation_Continentwise = df[df['Continent'] == Continent].groupby('year')[
    'electricity_generation'].sum().reset_index()
    ContinentWise_fig1 = px.line(Electricity_generation_Continentwise, x='year', y='electricity_generation',
                             labels=({'year': 'Year', 'electricity_generation': 'Electricity Generation in (GWH)'}),
                             markers='year', title='Electricity Generation over the Year ')

#2 --->
    Electricity_per_capita_ContinentWise = df[df['Continent']==Continent][['year', 'electricity_generation', 'population']].groupby('year')[['electricity_generation', 'population']].sum().reset_index()
    Electricity_per_capita_ContinentWise['Electricity_per_capita'] = (Electricity_per_capita_ContinentWise['electricity_generation'] * 1000000000 / Electricity_per_capita_ContinentWise['population'])
    Continent_fig5 = px.line(Electricity_per_capita_ContinentWise, x='year', y='Electricity_per_capita', markers='year',labels=({'year': 'Year','Electricity_per_capita':'Electricity Per Capita (KWH)'}),title='Electricity Per Capita ')

# 3-->
    ContinentWise = df[df['Continent']==Continent][['non_renewable_electricity', 'renewable_electricity']].sum().reset_index()
    ContinentWise.rename(columns={'index': 'Electricity', 0: 'Production in GWH'}, inplace=True)
    ContinentWise_fig2=px.pie(ContinentWise,values='Production in GWH',names='Electricity',title='Renewable Vs Non-Renewable Share ',hole=0.4)


# 4--->
    Electricity_by_other_ContinentWise = df[df['Continent']==Continent].groupby('year')[['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity', 'hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity', 'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    Continent_fig6 = px.line(Electricity_by_other_ContinentWise, x='year',y=['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity','hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity','other_renewable_exc_biofuel_electricity'],labels=({'year': 'Year', 'value': 'Electricity in (GWH)'}),title='Elelctricity Generation Mode Over the Year')

#5 -->

    ContinentWise_Non_Renewable = df[df['Continent'] == Continent][
    ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity']].sum().reset_index()
    ContinentWise_Non_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Non_Renewable = ContinentWise_Non_Renewable['Percentage'].sum()
    ContinentWise_Non_Renewable['Percentage'] = round(
    (ContinentWise_Non_Renewable['Percentage'] / Total_Non_Renewable) * 100, 2)
    Continent_fig3 = px.bar(ContinentWise_Non_Renewable, x='Electricity', y='Percentage', color='Electricity',
                        text='Percentage', title='Non Renewable Electricity Share ')
# 6 -->
    ContinentWise_Renewable = df[df['Continent']==Continent][['hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity','other_renewable_exc_biofuel_electricity']].sum().reset_index()
    ContinentWise_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Renewable = ContinentWise_Renewable['Percentage'].sum()
    ContinentWise_Renewable['Percentage'] = round((ContinentWise_Renewable['Percentage'] / Total_Renewable) * 100, 2)
    Continent_fig4 = px.bar(ContinentWise_Renewable, x='Electricity', y='Percentage', color='Electricity', text='Percentage',title='Renewable Electricity Share ')

# 7) -->
    ContinentWise_fossile = df[df['Continent']==Continent][['fossile_electricity', 'Non_fossile_electricity']].sum().reset_index()
    ContinentWise_fossile.rename(columns={'index': 'Electricity', 0: 'Production in GWH'}, inplace=True)
    ContinentWise_fig7=px.pie(ContinentWise_fossile,values='Production in GWH',names='Electricity',title='Fossil Vs Non-Fossil Share',hole=0.4)

    Demand_vs_supply = df[df['Continent']==Continent].groupby('year')[['electricity_generation', 'electricity_demand']].sum().reset_index()
    Continent_fig8 = px.line(Demand_vs_supply, x='year', y=['electricity_generation', 'electricity_demand'],
                            markers='year', labels=({'year': 'Year', 'value': 'Electricity in GWH'}),
                            title='Electricity Generation vs Demand Curve')

    st.plotly_chart(ContinentWise_fig1)
    st.plotly_chart(Continent_fig6)
    st.plotly_chart(Continent_fig5)
    st.plotly_chart(ContinentWise_fig2)
    st.plotly_chart(Continent_fig3)
    st.plotly_chart(Continent_fig4)
    st.plotly_chart(ContinentWise_fig7)
    st.plotly_chart(Continent_fig8)

# -----------------------------------------------------------------------------------------------------------------------(3)

if User_Menu=='Continent Wise' and Year!='Overall' and Continent!='Overall':
    st.header(f'Electricity Stats of {Continent} in {Year}')
    st.markdown("""***""")
    st.subheader('Electricity That Mostly Produced From --')
    x1=df[(df['year'] == Year) & (df['Continent'] == Continent)].groupby('country')['coal_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x2=df[(df['year'] == Year) & (df['Continent'] == Continent)].groupby('country')['gas_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x3=df[(df['year'] == Year) & (df['Continent'] == Continent)].groupby('country')['oil_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    x4=df[(df['year'] == Year) & (df['Continent'] == Continent)].groupby('country')['nuclear_electricity'].sum().sort_values(ascending=False).head(1).index[0]

    y1=df[(df['year'] == Year) & (df['Continent'] == Continent)].groupby('country')['hydro_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y2=df[(df['year'] == Year) & (df['Continent'] == Continent)].groupby('country')['solar_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y3=df[(df['year'] == Year) & (df['Continent'] == Continent)].groupby('country')['wind_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    y4=df[(df['year'] == Year) & (df['Continent'] == Continent)].groupby('country')['biofuel_electricity'].sum().sort_values(ascending=False).head(1).index[0]
    col1, col2, col3, col4 = st.columns(4)
    with col1 :
        st.info('Coal Electricity')
        st.subheader(x1)
    with col2 :
        st.info('Gas Electricity')
        st.subheader(x2)
    with col3 :
        st.info('Oil Electricity')
        st.subheader(x3)
    with col4 :
        st.info('Nuclear Electricity')
        st.subheader(x4)
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.info('Hydro Electricity')
        st.subheader(y1)
    with col2:
        st.info('Solar Electricity')
        st.subheader(y2)
    with col3:
        st.info('Wind Electricity')
        st.subheader(y3)
    with col4:
        st.info('Biofuel Electricity')
        st.subheader(y4)
    st.markdown("""***""")


    x=round(df[(df['year']==Year)&(df['Continent']==Continent)]['electricity_generation'].sum()*1000000000/df[(df['year']==Year)&(df['Continent']==Continent)]['population'].sum())
    y = df[(df['year']==Year)&(df['Continent']==Continent)]['electricity_generation'].sum()
    col1, col2= st.columns(2)
    with col1 :
        st.info(f'Electricity per Capita in {Year}')
        st.write(x,'Kwh')
    with col1:
        st.info(f'Total Electricity Generation in {Year}')
        st.write(y,'Gwh')
    st.markdown("""---""")





# 1) ->
    Electrity_by_year_ContinentWise = df[(df['year'] == Year) & (df['Continent'] == Continent)][
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity', 'hydro_electricity',
         'solar_electricity', 'biofuel_electricity', 'wind_electricity',
         'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    Continent_fig1 = px.bar(Electrity_by_year_ContinentWise, x='index', y=0,
                            labels=({'index': 'Electricity Mode', '0': 'Value in GWH'}), color='index',
                            title='Electricity Generation ')
# 2)->
    ContinentWise = df[(df['year'] == Year) & (df['Continent'] == Continent)][
        ['non_renewable_electricity', 'renewable_electricity']].sum().reset_index()
    ContinentWise.rename(columns={'index': 'Electricity', 0: 'Production in GWH'}, inplace=True)
    ContinentWise_fig2 = px.pie(ContinentWise, values='Production in GWH', names='Electricity',
                                title='Renewable Vs Non-Renewable Share ',hole=0.4)
#3) ->
    ContinentWise_Non_Renewable = df[(df['year'] == Year) & (df['Continent'] == Continent)][
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity']].sum().reset_index()
    ContinentWise_Non_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Non_Renewable = ContinentWise_Non_Renewable['Percentage'].sum()
    ContinentWise_Non_Renewable['Percentage'] = round(
        (ContinentWise_Non_Renewable['Percentage'] / Total_Non_Renewable) * 100, 2)
    Continent_fig3 = px.bar(ContinentWise_Non_Renewable, x='Electricity', y='Percentage', color='Electricity',
                            text='Percentage', title='Non Renewable Electricity Share ')
# 4)->
    ContinentWise_Renewable = df[(df['year'] == Year) & (df['Continent'] == Continent)][
        ['hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity',
         'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    ContinentWise_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Renewable = ContinentWise_Renewable['Percentage'].sum()
    ContinentWise_Renewable['Percentage'] = round((ContinentWise_Renewable['Percentage'] / Total_Renewable) * 100, 2)
    Continent_fig4 = px.bar(ContinentWise_Renewable, x='Electricity', y='Percentage', color='Electricity',
                            text='Percentage', title='Renewable Electricity Share ')
# 5)->
    ContinentWise_fossile = df[(df['year'] == Year) & (df['Continent'] == Continent)][
        ['fossile_electricity', 'Non_fossile_electricity']].sum().reset_index()
    ContinentWise_fossile.rename(columns={'index': 'Electricity', 0: 'Production in GWH'}, inplace=True)
    ContinentWise_fig5 = px.pie(ContinentWise_fossile, values='Production in GWH', names='Electricity',
                                title='Fossil Vs Non-Fossil Share ',color='Electricity',hole=0.4)



# 6)->





    st.plotly_chart(Continent_fig1)
    st.plotly_chart(ContinentWise_fig2)
    st.plotly_chart(Continent_fig3)
    st.plotly_chart(Continent_fig4)
    st.plotly_chart(ContinentWise_fig5)

# --------------------------------------------------------------------------------------------------------------------------(4)

# COUNTRY WISE
if User_Menu=='Country Wise':
    Nation=helper.select_country(df)
    Country=st.sidebar.selectbox('SELECT COUNTRY',Nation)

if User_Menu=='Country Wise' and Year=='Overall' and Country!='Overall':
    st.header(f'Electricity Stats of {Country}')
    st.markdown("""***""")


    # 1 --->
    Electricity_generation_Countrywise = df[df['country'] == Country].groupby('year')[
        'electricity_generation'].sum().reset_index()
    Country_fig1 = px.line(Electricity_generation_Countrywise, x='year', y='electricity_generation',
                           labels=({'year': 'Year', 'electricity_generation': 'Electricity Generation in (GWH)'}),
                           markers='year', title='Electricity Generation over the Year ')

    # 2 --->
    Electricity_per_capita_CountryWise = \
    df[df['country'] == Country][['year', 'electricity_generation', 'population']].groupby('year')[
        ['electricity_generation', 'population']].sum().reset_index()
    Electricity_per_capita_CountryWise['Electricity_per_capita'] = (
                Electricity_per_capita_CountryWise['electricity_generation'] * 1000000000 /
                Electricity_per_capita_CountryWise['population'])
    Country_fig5 = px.line(Electricity_per_capita_CountryWise, x='year', y='Electricity_per_capita', markers='year',
                           labels=({'year': 'Year', 'Electricity_per_capita': 'Electricity Per Capita (KWH)'}),
                           title='Electricity Per Capita ')

    # 3-->
    CountryWise = df[df['country'] == Country][
        ['non_renewable_electricity', 'renewable_electricity']].sum().reset_index()
    CountryWise.rename(columns={'index': 'Electricity', 0: 'Production in GWH'}, inplace=True)
    Country_fig2 = px.pie(CountryWise, values='Production in GWH', names='Electricity',
                          title='Renewable Vs Non-Renewable Share',hole=0.4)

    # 4--->
    Electricity_by_other_CountryWise = df[df['country'] == Country].groupby('year')[
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity', 'hydro_electricity',
         'solar_electricity', 'biofuel_electricity', 'wind_electricity',
         'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    Country_fig6 = px.line(Electricity_by_other_CountryWise, x='year',
                           y=['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity',
                              'hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity',
                              'other_renewable_exc_biofuel_electricity'],
                           labels=({'year': 'Year', 'value': 'Electricity in (GWH)'}),
                           title='Elelctricity Generation Mode Over the Year')


    # 5 -->

    CountryWise_Non_Renewable = df[df['country'] == Country][
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity']].sum().reset_index()
    CountryWise_Non_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Non_Renewable = CountryWise_Non_Renewable['Percentage'].sum()
    CountryWise_Non_Renewable['Percentage'] = round(
        (CountryWise_Non_Renewable['Percentage'] / Total_Non_Renewable) * 100, 2)
    Country_fig3 = px.bar(CountryWise_Non_Renewable, x='Electricity', y='Percentage', color='Electricity',
                          text='Percentage', title='Non Renewable Electricity Share ')


    # 6 -->
    CountryWise_Renewable = df[df['country'] == Country][
        ['hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity',
         'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    CountryWise_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Renewable = CountryWise_Renewable['Percentage'].sum()
    CountryWise_Renewable['Percentage'] = round((CountryWise_Renewable['Percentage'] / Total_Renewable) * 100, 2)
    Country_fig4 = px.bar(CountryWise_Renewable, x='Electricity', y='Percentage', color='Electricity',
                          text='Percentage', title='Renewable Electricity Share ')


    # 7) -->
    CountryWise_fossile = df[df['country'] == Country][
        ['fossile_electricity', 'Non_fossile_electricity']].sum().reset_index()
    CountryWise_fossile.rename(columns={'index': 'Electricity', 0: 'Production in GWH'}, inplace=True)
    Country_fig7 = px.pie(CountryWise_fossile, values='Production in GWH', names='Electricity',
                          title='Fossil Vs Non-Fossil Share',hole=0.4)

    Demand_vs_supply = df[df['country'] == Country].groupby('year')[
        ['electricity_generation', 'electricity_demand']].sum().reset_index()
    Country_fig8 = px.line(Demand_vs_supply, x='year', y=['electricity_generation', 'electricity_demand'],
                             markers='year', labels=({'year': 'Year', 'value': 'Electricity in GWH'}),
                             title='Electricity Generation vs Demand Curve')


    st.plotly_chart(Country_fig1)
    st.plotly_chart(Country_fig6)
    st.plotly_chart(Country_fig5)
    st.plotly_chart(Country_fig2)
    st.plotly_chart(Country_fig3)
    st.plotly_chart(Country_fig4)
    st.plotly_chart(Country_fig7)
    st.plotly_chart(Country_fig8)
    
# --------------------------------------------------------------------------------------------------------------------------(5)

if User_Menu=='Country Wise' and Year!='Overall' and Country!='Overall':
    st.header(f'Electricity Stats of {Country} in {Year}')
    st.markdown("""***""")

    x = round(df[(df['year'] == Year)&(df['country'] == Country)]['electricity_generation'].sum()*1000000000/df[(df['year'] == Year)&(df['country'] == Country)]['population'].sum())
    y = df[(df['year'] == Year)&(df['country'] == Country)]['electricity_generation'].sum()
    col1,col2 = st.columns(2)
    with col1:
        st.info(f'Electricity per Capita in {Year}')
        st.write(x,'kwh')
    with col1:
        st.info(f'Total Electricity Generation in {Year}')
        st.write(y,'Gwh')
    st.markdown("""***""")

    Electrity_by_year_ = df[(df['year'] == Year) & (df['country'] == Country)][
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity', 'hydro_electricity',
         'solar_electricity', 'biofuel_electricity', 'wind_electricity',
         'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    Y_fig1 = px.bar(Electrity_by_year_, x='index', y=0,
                            labels=({'index': 'Electricity Mode', '0': 'Value in GWH'}), color='index',
                            title='Electricity Generation ')
    # 2)->
    ContinentWise = df[(df['year'] == Year) & (df['country'] == Country)][
        ['non_renewable_electricity', 'renewable_electricity']].sum().reset_index()
    ContinentWise.rename(columns={'index': 'Electricity', 0: 'Production in GWH'}, inplace=True)
    ContinentWise_fig2 = px.pie(ContinentWise, values='Production in GWH', names='Electricity',
                                title='Renewable Vs Non-Renewable Share ',hole=0.4)
    # 3) ->
    ContinentWise_Non_Renewable = df[(df['year'] == Year) & (df['country'] == Country)][
        ['coal_electricity', 'gas_electricity', 'oil_electricity', 'nuclear_electricity']].sum().reset_index()
    ContinentWise_Non_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Non_Renewable = ContinentWise_Non_Renewable['Percentage'].sum()
    ContinentWise_Non_Renewable['Percentage'] = round(
        (ContinentWise_Non_Renewable['Percentage'] / Total_Non_Renewable) * 100, 2)
    Continent_fig3 = px.bar(ContinentWise_Non_Renewable, x='Electricity', y='Percentage', color='Electricity',
                            text='Percentage', title='Non Renewable Electricity Share ')
    # 4)->
    ContinentWise_Renewable = df[(df['year'] == Year) & (df['country'] == Country)][
        ['hydro_electricity', 'solar_electricity', 'biofuel_electricity', 'wind_electricity',
         'other_renewable_exc_biofuel_electricity']].sum().reset_index()
    ContinentWise_Renewable.rename(columns={'index': 'Electricity', 0: 'Percentage'}, inplace=True)
    Total_Renewable = ContinentWise_Renewable['Percentage'].sum()
    ContinentWise_Renewable['Percentage'] = round((ContinentWise_Renewable['Percentage'] / Total_Renewable) * 100, 2)
    Continent_fig4 = px.bar(ContinentWise_Renewable, x='Electricity', y='Percentage', color='Electricity',
                            text='Percentage', title='Renewable Electricity Share ')
    # 5)->
    ContinentWise_fossile = df[(df['year'] == Year) & (df['country'] == Country)][
        ['fossile_electricity', 'Non_fossile_electricity']].sum().reset_index()
    ContinentWise_fossile.rename(columns={'index': 'Electricity', 0: 'Production in GWH'}, inplace=True)
    ContinentWise_fig5 = px.pie(ContinentWise_fossile, values='Production in GWH', names='Electricity',
                                title='Fossil Vs Non-Fossil Share ', color='Electricity',hole=0.4)



    # 6)->

    st.plotly_chart(Y_fig1)
    st.plotly_chart(ContinentWise_fig2)
    st.plotly_chart(Continent_fig3)
    st.plotly_chart(Continent_fig4)
    st.plotly_chart(ContinentWise_fig5)

# -------------------------------------------------------------------------------------------------------------------------(6)
