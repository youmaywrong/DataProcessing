from os.path import join, dirname
import datetime
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import Select
from bokeh.palettes import Spectral4
from bokeh.plotting import figure

# in de terminal: bokeh serve --show characteristic-incidents-per-state.py

df = pd.read_csv("stage3.csv")
df = df.copy()

# extract years from dates
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

df['incident_characteristics'] = df['incident_characteristics'].str.lower()

def make_plot():
    current_state = state_select.value
    current_df = df[df['state'] == current_state]

    years = ['2014', '2015', '2016', '2017', '2018']

    mass_shootings = current_df[current_df['incident_characteristics'].str.contains("mass shooting") == True]
    armed_robbery = current_df[current_df['incident_characteristics'].str.contains("robbery") == True]
    gang_involvement = current_df[current_df['incident_characteristics'].str.contains("gang") == True]
    domestic_violence = current_df[current_df['incident_characteristics'].str.contains("domestic") == True]

    data = [mass_shootings, armed_robbery, gang_involvement, domestic_violence]
    names = ["Mass Shootings", "Armed Robbery", "Gang Involvement", "Domestic Violence"]

    plot = figure()

    for characteristic, name, color in zip(data, names, Spectral4):
        incidents = [x for x in characteristic.groupby('year').size()]
        if not incidents:
            incidents = 0
        plot.line(years, incidents, line_width=2, color=color, alpha=0.8, legend=name)

    plot.xaxis.axis_label = 'Year'
    plot.yaxis.axis_label = 'Incidents'

    return plot

def update(attr, old, new):
    layout.children[1] = make_plot()


states = sorted(df['state'].unique())
state_select = Select(value='Alabama', title='State', options=states)
state_select.on_change('value', update)

controls = widgetbox(state_select, width=200)
layout = row(controls, make_plot())


curdoc().add_root(layout)
curdoc().title = "Incidents by State"
