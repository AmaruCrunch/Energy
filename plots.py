import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('electricity.csv')
# Filter the data for the year 2017
df_2017 = df[df['Period'] == 2014]

# Define the labels and values for the pie chart
labels = ['Heavy fuel oil', 'Gas/Diesel Oil', 'Coal', 'Natural gas', 'Renewbles energy', 'Wind energy', 'Water energy', 'Biogas', 'Solar energy', 'Oil shell', 'Residual Heat']
values = df_2017[['Total Heavy fuel oil', 'Total Gas/Diesel Oil', 'Total Coal', 'Total Natural gas', 'Total Renewbles energy', 'Total Wind energy', 'Total Water energy', 'Total Biogas', 'Total Solar energy', 'Total Oil shell', 'Total Residual Heat']].values.flatten()

# Define the parent labels and values for the outer rim
parent_labels = ['Fossil fuels', 'Fossil fuels', 'Fossil fuels', 'Fossil fuels', 'Renewable energy', 'Renewable energy', 'Renewable energy', 'Renewable energy', 'Renewable energy', 'Fossil fuels', 'Fossil fuels']
parent_values = df_2017[['Total fossil fuels', 'Total fossil fuels', 'Total fossil fuels', 'Total fossil fuels', 'Total Renewbles energy', 'Total Renewbles energy', 'Total Renewbles energy', 'Total Renewbles energy', 'Total Renewbles energy', 'Total fossil fuels', 'Total fossil fuels']].values.flatten()

# Create the pie chart
fig = go.Figure()

fig.add_trace(go.Sunburst(
    labels=parent_labels+labels,
    parents=[""]*len(parent_labels)+parent_labels,
    values=parent_values.tolist()+values.tolist(),
    hovertemplate='<b>%{label} </b> <br> Energy Consumption: %{value}',
    branchvalues="total",
))

fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))

fig.show()