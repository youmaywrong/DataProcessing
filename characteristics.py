from os.path import join, dirname
import datetime
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import Select, DatetimeTickFormatter, Panel, Tabs
from bokeh.plotting import figure
import numpy as np

# in de terminal: bokeh serve --show characteristics.py

df = pd.read_csv("stage3.csv")
df = df.copy()

# extract years from dates
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# convert to lower case for easy filtering
df['incident_characteristics'] = df['incident_characteristics'].str.lower()


def make_plot():
    # get selected state
    current_state = state_select.value
    current_df = df[df['state'] == current_state]

    # get selected characteristic
    current_char = characteristic_select.value
    relevant_incidents = current_df[current_df['incident_characteristics'].str.contains(characteristics[current_char]['keyword']) == True]

    # define years
    years = [2014, 2015, 2016, 2017]

    # count all incidents that match the selected values
    n_incidents = []
    for year in years:
        if year in relevant_incidents['year'].unique():
            n_incidents.append(relevant_incidents[relevant_incidents['year'] == year]['incident_id'].count())
        # make sure 0 is plotted too
        else:
            n_incidents.append(0)


    plot = figure(plot_width=500, plot_height=500)
    plot.line(['2014', '2015', '2016', '2017'], n_incidents, line_width=2, alpha=0.8, legend=current_state)

    # style plot title
    plot.title.text=current_char + " in " + current_state
    plot.title.text_font_size='25px'
    plot.title.align='center'

    # plot x axis
    plot.xaxis.axis_label = 'Year'
    plot.x_range.start = 2014
    plot.x_range.end = 2017

    # plot y axis
    plot.yaxis.axis_label = 'Incidents'
    plot.y_range.start = 0

    return plot


# update plot with newly selected values
def update(attr, old, new):
    layout.children[1] = make_plot()

# define list of states to select
states = sorted(df['state'].unique())

# create select menu for states
state_select = Select(value='Alabama', title='State', options=states)
state_select.on_change('value', update)

# define incident characteristics with the words that are used for filtering
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

# create select menu for incident characteristics
characteristic_select = Select(value='Mass Shootings', title='Characteristic', options=sorted(characteristics.keys()))
characteristic_select.on_change('value', update)

# add select menus and plot to current document
controls = widgetbox([state_select, characteristic_select], width=200)
layout = row(controls, make_plot())
tab1 = Panel(child=layout, title="Incidents by State")

########################################################################

# test tabs
test_select = Select(value='A', options=['A', 'B', 'C'])

p2 = figure(plot_width=500, plot_height=500)
p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
p2.title.text='Testing Tabs'
p2.title.text_font_size='25px'
p2.title.align='center'
layout2 = row(test_select, p2)
tab2 = Panel(child=layout2, title="line")

tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)
curdoc().title = "Incidents by State"
