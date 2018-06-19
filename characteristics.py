from os.path import join, dirname
import datetime
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import Select, DatetimeTickFormatter
from bokeh.plotting import figure
import numpy as np

# in de terminal: bokeh serve --show characteristics.py

df = pd.read_csv("stage3.csv")
df = df.copy()

# extract years from dates
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

df['incident_characteristics'] = df['incident_characteristics'].str.lower()

def make_plot():
    current_state = state_select.value
    current_df = df[df['state'] == current_state]

    current_char = characteristic_select.value
    relevant_incidents = current_df[current_df['incident_characteristics'].str.contains(characteristics[current_char]['keyword']) == True]

    years = [2014, 2015, 2016, 2017]

    n_incidents = []
    for year in years:
        if year in relevant_incidents['year'].unique():
            n_incidents.append(relevant_incidents[relevant_incidents['year'] == year]['incident_id'].count())
        else:
            n_incidents.append(0)


    plot = figure(plot_width=500, plot_height=500)

    plot.line(['2014', '2015', '2016', '2017'], n_incidents, line_width=2, alpha=0.8, legend=current_state)

    # style plot title
    plot.title.text=current_char + " in " + current_state
    plot.title.text_font_size='25px'
    plot.title.align='center'

    plot.xaxis.axis_label = 'Year'
    plot.yaxis.axis_label = 'Incidents'
    plot.y_range.start = 0
    plot.x_range.start = 2014
    plot.x_range.end = 2017

    return plot

def update(attr, old, new):
    layout.children[1] = make_plot()


states = sorted(df['state'].unique())
state_select = Select(value='Alabama', title='State', options=states)
state_select.on_change('value', update)

characteristics = {
    'Mass Shootings': {
        'keyword': 'mass shooting',
    },
    'Armed Robbery': {
        'keyword': 'robbery',
    },
    'Gang Involvement': {
        'keyword': 'gang',
    },
    'Domestic Violence': {
        'keyword': 'domestic',
    }
}

characteristic_select = Select(value='Mass Shootings', title='Characteristic', options=sorted(characteristics.keys()))
characteristic_select.on_change('value', update)


controls = widgetbox([state_select, characteristic_select], width=200)
layout = row(controls, make_plot())


curdoc().add_root(layout)
curdoc().title = "Incidents by State"
