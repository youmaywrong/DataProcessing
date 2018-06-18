from os.path import join, dirname
import datetime
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import Select
from bokeh.palettes import Spectral4
from bokeh.plotting import figure

# in de terminal: bokeh serve --show incidents-per-state.py


df = pd.read_csv("stage3.csv")
df = df.copy()

# extract years from dates
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year


def make_plot():
    current_state = state_select.value
    current_df = df[df['state'] == current_state]

    years = ['2014', '2015', '2016', '2017', '2018']
    n_incidents = [count for count in current_df.groupby('year').size()]

    plot = figure()
    plot.xaxis.axis_label = 'Year'
    plot.yaxis.axis_label = 'Incidents'

    plot.line(years, n_incidents, line_width=2)

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
