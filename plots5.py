import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import plotly.express as px
from plotly.subplots import make_subplots

# Important constants
ENTITY = 'Entity'
YEAR = 'Year'
ENERGY = 'Energy'
GDP = 'GDP'
CODE = 'Code'
COLOR_BAR_ENERGY = 'Energy Consumption<br>(kWh/person)'
COLOR_BAR_GDP = 'GDP<br>(USD)'
COLOR_SCALE_ENERGY = 'Reds'
COLOR_SCALE_GDP = 'Blues'
SELECTED_COUNTRY_DEFAULT = 'Israel'
# Constants for trends chart
TITLE_ENERGY = 'Energy Consumption'
TITLE_GDP = 'GDP'
AXIS_TYPE_ENERGY = '(kWh/person)'
AXIS_TYPE_GDP = 'USD'

# Constants for dropdown menus
PLOT_OPTIONS = ['Energy Consumption Over Time', 'Energy vs GDP Correlation', 'Cumulative Growth']
PLOT_DEFAULT = PLOT_OPTIONS[0]
COUNTRIES_DEFAULT = ['United States', 'Germany', 'Japan']

# Page settings
st.set_page_config(layout="wide")

# Load data
df_merged = pd.read_csv('df_merged.csv')
df_energy_source = pd.read_csv('energy-consumption-by-source-and-country.csv')

# Display objective of dashboard
st.markdown("""
## Power Shifts: A Data Visualization Study on Global Energy Consumption and GDP

The objective of this dashboard is to explore the relationship between a country's energy consumption and its Gross 
Domestic Product (GDP). By examining energy consumption per capita over time, the correlation between energy 
consumption and GDP, and the cumulative growth in both these areas, we aim to gain insights into how energy use and 
economic activity are intertwined. 

Understanding these patterns can inform policy-making, economic forecasts, and sustainability initiatives. It's also a step towards recognizing the balance that needs to be struck between economic growth, energy use, and environmental sustainability.
""")

# User input
selected_country = SELECTED_COUNTRY_DEFAULT

# Create Streamlit layout
col1, col2 = st.columns([2, 1])
col11, col12 = col1.columns(2)

feature = col11.selectbox('Select a feature', [ENERGY, GDP], index=0)
year = col12.slider('Select a year', int(df_merged[YEAR].min()), int(df_merged[YEAR].max()), 2019)

# Filter dataframe for the selected year
df_filtered = df_merged[df_merged[YEAR] == year]

# Create choropleth and scatter plots based on the selected feature
if feature == ENERGY:
    data_var = ENERGY
    title_suffix = TITLE_ENERGY
    color_bar = COLOR_BAR_ENERGY
    color_scale = COLOR_SCALE_ENERGY

else:  # feature == 'GDP'
    data_var = GDP
    title_suffix = TITLE_GDP
    color_bar = COLOR_BAR_GDP
    color_scale = COLOR_SCALE_GDP

# plot choropleth
choropleth = go.Figure(data=go.Choropleth(
    locations=df_filtered[CODE],
    z=df_filtered[data_var],
    text=df_filtered[ENTITY],
    colorscale=color_scale,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title=color_bar,
))

choropleth.update_layout(
    title=f'{title_suffix} per Capita - {year}',
    geo=dict(showframe=True, showcoastlines=True, projection_type='natural earth'),
    # autosize=False,
    #width=750,
    # height=500,

)

with col1:
    selected_point = plotly_events(choropleth, override_width="100%")
    st.write(
        f"_The map shows {title_suffix.lower()} per capita for the year {year}. Select a different year or feature to "
        f"update the map. Click on a country to see the change in {title_suffix.lower()} over the years_")

if selected_point:
    ind = selected_point[0]['pointIndex']
    selected_country = df_filtered.iloc[ind][ENTITY]

# Filter data for selected country and 'World'
data_selected = df_merged[df_merged[ENTITY] == selected_country]
data_world = df_merged[df_merged[ENTITY] == 'World']

# Create subplots for energy and GDP trends
fig = make_subplots(rows=2, cols=1, vertical_spacing=0.2, subplot_titles=(TITLE_ENERGY, TITLE_GDP))

# Add traces for energy and GDP trends for the selected country and the world
for row, (title, variable, axis_type, color) in enumerate([(TITLE_ENERGY, ENERGY, AXIS_TYPE_ENERGY, 'red'),
                                                           (TITLE_GDP, GDP, AXIS_TYPE_GDP, 'blue')], start=1):
    fig.add_trace(
        go.Scatter(
            x=data_selected[YEAR],
            y=data_selected[variable],
            mode='lines',
            name=f'{selected_country} {title}',
            line=dict(color=color)
        ),
        row=row, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=data_world[YEAR],
            y=data_world[variable],
            mode='lines',
            name=f'World Average',
            line=dict(dash='dot', color=color)
        ),
        row=row, col=1
    )

# Update layout and y-axes titles
fig.update_layout(height=570, width=300, title_text=f"Trends in Energy and GDP in {selected_country}")
fig.update_yaxes(title_text=f'{TITLE_ENERGY}-{AXIS_TYPE_ENERGY}', row=1, col=1)
fig.update_yaxes(title_text=f'{TITLE_GDP}-{AXIS_TYPE_GDP}', row=2, col=1)

fig.update_layout(showlegend=False, legend=dict(
    yanchor="bottom",
    y=-0.4,
    xanchor="left",
    x=0.01
))

with col2:
    st.markdown('\n')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f'_The above charts show the change in energy consumption and GDP per capita in {selected_country} '
                'over the years. To select another country, click on the map._')

# Select the plot and countries
st.subheader("Exploring Energy Consumption and GDP Relationships")
col1, col2 = st.columns(2)

# Centered selectbox and multiselect
with col1:
    st.write("")  # For vertical spacing
    plot = st.selectbox('Select a plot', PLOT_OPTIONS, index=0)

with col2:
    st.write("")  # For vertical spacing
    countries = st.multiselect('Select countries', df_merged[ENTITY].unique(), default=COUNTRIES_DEFAULT)

# Filter the merged DataFrame for the selected countries
df_selected = df_merged[df_merged[ENTITY].isin(countries)]

# Energy Consumption Over Time for Selected Countries
if plot == 'Energy Consumption Over Time':
    line_chart = go.Figure()
    for country in countries:
        df_country = df_selected[df_selected[ENTITY] == country]
        line_chart.add_trace(go.Scatter(x=df_country[YEAR], y=df_country[ENERGY], mode='lines', name=country))

    line_chart.update_layout(title='Energy Consumption Per Capita Over Time', xaxis_title='Year',
                             yaxis_title='Energy Consumption Per Capita (kWh/person)')

    st.plotly_chart(line_chart, use_container_width=True)
    st.markdown("""_This line chart displays per capita energy consumption over time (x-axis) for selected countries. 
    Each line represents a country, showing how its energy consumption has evolved._""")


# Correlation between Energy Consumption and GDP per Capita
elif plot == 'Energy vs GDP Correlation':

    df_selected = df_selected[df_selected[YEAR] > 1980].sort_values(by=YEAR)
    scatter_plot = px.scatter(df_selected, x=ENERGY, y=GDP, color=ENTITY, hover_name=ENTITY,
                              animation_frame=YEAR, animation_group=ENTITY,
                              range_y=[df_selected[GDP].min(), df_selected[GDP].max()],
                              range_x=[df_selected[ENERGY].min(), df_selected[ENERGY].max()],
                              size='Population')

    scatter_plot.update_layout(title='Energy Consumption per Capita vs. GDP per Capita',
                               xaxis_title='Energy Consumption per Capita (kWh/person)',
                               yaxis_title='GDP per Capita')

    st.plotly_chart(scatter_plot, use_container_width=True)
    st.markdown("""_This scatter plot shows the relationship between per capita energy consumption (x-axis) and GDP (
    y-axis) over time. Each dot represents a country in a given year, colored uniquely per country. The size of the 
    dot indicates the population size. By hovering over a dot, you can see detailed data for that point. The 
    animation feature allows you to observe how these variables have changed over time across different countries._""")



# Cumulative Growth in Energy Consumption and GDP
elif plot == 'Cumulative Growth':
    df_selected['Cumulative Growth in Energy'] = (df_selected.groupby(ENTITY)[ENERGY].pct_change() + 1).cumprod() - 1
    df_selected['Cumulative Growth in GDP'] = (df_selected.groupby(ENTITY)[GDP].pct_change() + 1).cumprod()

    fig_energy = go.Figure()
    fig_gdp = go.Figure()

    for country in countries:
        df_country = df_selected[df_selected[ENTITY] == country]
        fig_energy.add_trace(
            go.Scatter(x=df_country[YEAR], y=df_country['Cumulative Growth in Energy'],
                       mode='lines', name=country))
        fig_gdp.add_trace(
            go.Scatter(x=df_country[YEAR], y=df_country['Cumulative Growth in GDP'], mode='lines',
                       name=country))

    fig_energy.update_layout(title='Cumulative Growth in Energy Consumption', xaxis_title='Year',
                             yaxis_title='Cumulative Growth')
    fig_gdp.update_layout(title='Cumulative Growth in GDP', xaxis_title='Year', yaxis_title='Cumulative Growth')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_energy, use_container_width=True)


    with col2:
        st.plotly_chart(fig_gdp, use_container_width=True)

    st.markdown("""
    _These plots depict cumulative growth of energy consumption and GDP over time (x-axis) for selected countries. 
    Each line signifies a country, showcasing its economic and energy growth._
    """)

# Section header
st.markdown("""
## Energy Sources

Thus far, we've explored the relationship between energy consumption, GDP, and population. We've discovered that more industrialized countries consume more commercial energy, reflecting their higher economic activity levels. Conversely, many developing countries consume less energy due to less industrialized economies and reliance on traditional energy sources. 

Next, we'll examine the types of energy sources that different countries rely on. Understanding this is essential for creating sustainable energy policies and practices. 
""")

df_energy_source = df_energy_source.drop('Total Consumption', axis=1)
selected_country = st.selectbox('Select a country:', df_energy_source[ENTITY].unique(), index=44)

df_country = df_energy_source[df_energy_source[ENTITY] == selected_country]
fig = go.Figure()
for column in df_country.columns[3:]:
    fig.add_trace(go.Scatter(x=df_country[YEAR], y=df_country[column], mode='lines', stackgroup='one', name=column))
fig.update_layout(title=f'Energy Consumption by Source in {selected_country} Over Time', xaxis=dict(title='Year'),
                  yaxis=dict(title='Energy Consumption - TWh'), )
st.plotly_chart(fig, use_container_width=True)
st.markdown(
    "_This stacked area plot shows the energy consumption from various sources over time in the selected country. The area covered by each color represents the amount of energy consumed from each source._")

df = df_energy_source
countries = df[ENTITY].unique()
years = sorted(df[YEAR].unique())
col1, col2 = st.columns(2)
selected_countries = col1.multiselect('Select countries', countries, default=COUNTRIES_DEFAULT)
selected_year = col2.slider('Select a year', min_value=int(min(years)), max_value=int(max(years)), value=2019, key=10)

df_combined = pd.DataFrame()
for country in selected_countries:
    df_country = df[(df[ENTITY] == country) & (df[YEAR] == selected_year)].copy()
    total_consumption = df_country.iloc[:, 3:].sum(axis=1)
    df_country.iloc[:, 3:] = df_country.iloc[:, 3:].div(total_consumption,
                                                        axis=0) * 100  # Multiply by 100 to convert to percentage
    df_melted = df_country.melt(id_vars=[ENTITY, 'Code', YEAR], var_name='Source', value_name='Percentage')
    df_combined = pd.concat([df_combined, df_melted], ignore_index=True)

fig = px.bar(df_combined, x='Source', y='Percentage', color=ENTITY, barmode='group',
             title=f'Energy Consumption as Percentage of Total Use in {selected_year}')
fig.update_yaxes(title_text='Percentage (%)')  # Change y-axis title to show it's in percentage
st.plotly_chart(fig, use_container_width=True)
st.markdown("_This bar chart shows the breakdown of energy consumption from various sources as a percentage of total "
            "energy use in the selected year for the chosen countries. Each bar represents a different energy source, "
            "and the height of the bars indicates the percentage of total energy consumption that source comprises._")

st.markdown("""
## Key Takeaways

1. More industrialized countries tend to consume more commercial energy, reflecting their higher levels of economic activity.
2. Energy consumption does not fully explain a country's economic status, as factors such as energy sources, energy efficiency, and energy policies also come into play.
3. The type of energy sources a country relies on varies significantly, which is an essential consideration when forming sustainable energy policies and practices.
4. Analyzing energy trends over time can help us understand how a country's energy consumption pattern changes and where it might be heading.

---
Made with ♥ by Yonatan and Noam.\n
Check out more cool projects at: https://github.com/AmaruCrunch
""")
