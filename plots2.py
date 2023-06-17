import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('electricity.csv')
df_energy = pd.read_csv('global.csv')
df_gdp = pd.read_csv('gdp_reshaped.csv')
df_merged = pd.read_csv('df_merged.csv')
df_continents = pd.read_csv('Countries-Continents.csv')

st.markdown("""
## Power Shifts: A Data Visualization Study on Global Energy Consumption and GDP

The objective of this dashboard is to explore the relationship between a country's energy consumption and its Gross Domestic Product (GDP). By examining energy consumption per capita over time, the correlation between energy consumption and GDP, and the cumulative growth in both these areas, we aim to gain insights into how energy use and economic activity are intertwined. 

Understanding these patterns can inform policy-making, economic forecasts, and sustainability initiatives. It's also a step towards recognizing the balance that needs to be struck between economic growth, energy use, and environmental sustainability.
""")


# Select feature and year using Streamlit's columns
col1, col2 = st.columns(2)

feature = col1.selectbox('Select a feature', ['Energy', 'GDP'], index=0)
year = col2.slider('Select a year', int(min(df_energy['Year'].unique())), int(max(df_energy['Year'].unique())), 2019)

# Filter energy and GDP dataframes
df_energy_filtered = df_energy[df_energy['Year'] == year]
df_gdp_filtered = df_gdp[df_gdp['Year'] == year]

if feature == 'Energy':
    # Energy Consumption per Capita
    choropleth = go.Figure(data=go.Choropleth(
        locations=df_energy_filtered['Code'],
        z=df_energy_filtered['Primary energy consumption per capita (kWh/person)'],
        text=df_energy_filtered['Entity'],
        colorscale='Reds',
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='Energy Consumption<br>(kWh/person)',
    ))

    choropleth.update_layout(
        title=f'Energy Consumption per Capita - {year}',
        geo=dict(showframe=True, showcoastlines=True, projection_type='natural earth')
    )

    st.plotly_chart(choropleth)
    st.write(
        f"_The map shows energy consumption per capita for the year {year}. Select a different year or feature to update the map._")

elif feature == 'GDP':
    # GDP per Capita
    choropleth_gdp = go.Figure(data=go.Choropleth(
        locations=df_gdp_filtered['Code'],
        z=df_gdp_filtered['GDP per capita'],
        text=df_gdp_filtered['Entity'],
        colorscale='Reds',
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='GDP per capita (USD)',
    ))

    choropleth_gdp.update_layout(
        title=f'GDP per Capita - {year}',
        geo=dict(showframe=True, showcoastlines=True, projection_type='natural earth')
    )

    st.plotly_chart(choropleth_gdp)
    st.write(
        f"The map shows GDP per capita for the year {year}. Select a different year or feature to update the map.")


# Title
st.subheader("Exploring Energy Consumption and GDP Relationships")

# Select the plot
plot = st.selectbox('Select a plot', ['Energy Consumption Over Time', 'Energy vs GDP Correlation', 'Cumulative Growth'], index=0)
countries = st.multiselect('Select countries', df_energy['Entity'].unique(), default=['Israel', 'United States', 'New Zealand', 'Germany', 'Japan'])

# Energy Consumption Over Time for Selected Countries
if plot == 'Energy Consumption Over Time':
    line_chart = go.Figure()
    for country in countries:
        df_country = df_energy[df_energy['Entity'] == country]
        line_chart.add_trace(go.Scatter(x=df_country['Year'], y=df_country['Primary energy consumption per capita (kWh/person)'], mode='lines', name=country))

    line_chart.update_layout(title='Energy Consumption Per Capita Over Time', xaxis_title='Year', yaxis_title='Energy Consumption Per Capita (kWh/person)')
    st.plotly_chart(line_chart)
    st.markdown("_This plot shows how energy consumption per capita has changed over time for selected countries._")

# Correlation between Energy Consumption and GDP per Capita
elif plot == 'Energy vs GDP Correlation':
    df_merged_filtered = df_merged[df_merged['Entity'].isin(countries)]

    scatter_plot = px.scatter(
        data_frame=df_merged_filtered,
        x='Primary energy consumption per capita (kWh/person)',
        y='GDP per capita',
        color='Entity',
        hover_name='Entity'
    )

    scatter_plot.update_layout(
        title='Energy Consumption per Capita vs. GDP per Capita',
        xaxis_title='Energy Consumption per Capita (kWh/person)',
        yaxis_title='GDP per Capita'
    )

    st.plotly_chart(scatter_plot)
    st.markdown("_This scatter plot shows the correlation between energy consumption per capita and GDP per capita for selected countries._")

# Cumulative Growth in Energy Consumption and GDP
elif plot == 'Cumulative Growth':
    df_energy_selected = df_energy[df_energy['Entity'].isin(countries)]
    df_gdp_selected = df_gdp[df_gdp['Entity'].isin(countries)]

    df_energy_selected['Cumulative Growth in Energy Consumption'] = (df_energy_selected.groupby('Entity')[
                                                                         'Primary energy consumption per capita (kWh/person)'].pct_change() + 1).cumprod() - 1
    df_gdp_selected['Cumulative Growth in GDP'] = (df_gdp_selected.groupby('Entity')[
                                                       'GDP per capita'].pct_change() + 1).cumprod() - 1

    fig_energy = go.Figure()
    fig_gdp = go.Figure()
    for country in countries:
        df_country_energy = df_energy_selected[df_energy_selected['Entity'] == country]
        df_country_gdp = df_gdp_selected[df_gdp_selected['Entity'] == country]
        fig_energy.add_trace(
            go.Scatter(x=df_country_energy['Year'], y=df_country_energy['Cumulative Growth in Energy Consumption'],
                       mode='lines', name=country))
        fig_gdp.add_trace(
            go.Scatter(x=df_country_gdp['Year'], y=df_country_gdp['Cumulative Growth in GDP'], mode='lines',
                       name=country))

    fig_energy.update_layout(title='Cumulative Growth in Energy Consumption', xaxis_title='Year',
                             yaxis_title='Cumulative Growth')
    fig_gdp.update_layout(title='Cumulative Growth in GDP', xaxis_title='Year', yaxis_title='Cumulative Growth')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_energy, use_container_width=True)
        st.markdown("_This plot shows the cumulative growth in energy consumption for selected countries over time._")

    with col2:
        st.plotly_chart(fig_gdp, use_container_width=True)
        st.markdown("_This plot shows the cumulative growth in GDP for selected countries over time._")


st.markdown("""
## Key Takeaways

Our analysis has revealed a complex relationship between energy consumption and economic activity. We see that more industrialized countries generally consume more commercial energy, reflecting their higher levels of economic activity. Conversely, many developing countries have lower energy consumption, often due to less industrialized economies and reliance on traditional energy sources.

However, energy consumption alone does not fully explain a country's economic status. Other factors such as energy sources, energy efficiency, and energy policies also come into play. Hence, while there's a relationship between energy use and GDP, the dynamics are multifaceted and require further exploration.

It's crucial to consider sustainable energy sources and practices, especially for high-energy-consuming countries, to mitigate the environmental impact. Understanding these data trends is a stepping stone in shaping a sustainable future.
""")


labels = ['Heavy fuel oil', 'Gas/Diesel Oil', 'Coal', 'Natural gas',
          'Wind energy', 'Water energy', 'Biogas', 'Solar energy',
          'Oil shell', 'Residual Heat']

plot_placeholder = st.empty()
st.markdown("_This plot shows the change in energy sources in Israel over time._")
sources = st.multiselect('Select sources to compare', labels, default=['Natural gas', 'Coal', 'Solar energy'])


fig = go.Figure()

df_filtered = df[['Period'] + ['Total ' + source for source in sources]]

for source in sources:
    fig.add_trace(go.Scatter(x=df_filtered['Period'], y=df_filtered['Total ' + source], mode='lines', name=source))

fig.update_layout(title='Energy Sources In Israel Over Time',
                  xaxis_title='Year', yaxis_title='Energy Consumption (MW)')

plot_placeholder.plotly_chart(fig)


st.markdown("""---
Made with ♥ by Yonatan and Noam.\n
Check out more cool projects at: https://github.com/AmaruCrunch

""")

