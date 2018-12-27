# from flask import Flask, render_template

from jinja2 import Environment, FileSystemLoader

from tornado.web import RequestHandler

import pandas as pd
from bokeh.embed import server_document
from bokeh.layouts import column, layout, widgetbox
from bokeh.models import ColumnDataSource, Slider, Select
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop

from actual_vs_goal_cumulative import actual_goal_cumulative
from stacked_chart import stacked_bar_chart
from weekly_actual_goal import weekly_actual_goal
from static_summary import actual_weekly_vs_goal, summary_cumulative

from functools import lru_cache

from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature

env = Environment(loader=FileSystemLoader('templates'))

class IndexHandler(RequestHandler):
    def get(self):
        template = env.get_template('embed.html')
        script = server_document('http://localhost:5006/bkapp')
        self.write(template.render(script=script, template="Tornado"))

@lru_cache()
def load_data():
    df = pd.read_csv('strava_data.csv', index_col=0)
    return df

@lru_cache()
def load_weekly():
    df = pd.read_csv('strava_weekly_data.csv', index_col=0)
    # df['week_number'] = df['week_number'].apply(str)
    return df

def select_weeks():
    """ Use the current selections to determine which filters to apply to the
    data. Return a dataframe of the selected data
    """
    df = load_data()

    # Determine what has been selected for each widgetd
    week_val = weeks_runs.value

    # Filter by week and weekly_actual_cumulative
    if week_val == "week 01":
        selected = df #[df.week == 'week 01']
    else:
        selected = df[(df.week == week_val)]

    # desc.text = f"Week: {week_val}"
    return selected

def update():
    """ Get the selected data and update the data in the source
    """
    df_active = select_weeks()
    source.data = ColumnDataSource(data=df_active).data

def selection_change(attrname, old, new):
    """ Function will be called when the poly select (or other selection tool)
    is used. Determine which items are selected and show the details below
    the graph
    """
    selected = source.selected["1d"]["indices"]

    df_active = select_weeks()

    if selected:
        data = df_active.iloc[selected, :]
        temp = data.set_index("week").T.reindex(index=col_order)
        details.text = temp.style.render()
    else:
        details.text = "Selection Details"

all_weeks = list(load_data()['week'].unique())
all_week_number = list(load_weekly()['week_number'])
X_AXIS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
source = ColumnDataSource(data=load_data())
weekly_source = ColumnDataSource(data=load_weekly())
summary_actual = actual_weekly_vs_goal(weekly_source, all_week_number)
cumulative_actual = summary_cumulative(weekly_source, all_week_number)
p = weekly_actual_goal(source, X_AXIS)
week_stacked_bar = stacked_bar_chart(source, X_AXIS)
weekly_actual_cumulative_fig = actual_goal_cumulative(source, X_AXIS)

def modify_doc(doc):

    weeks_runs = Select(title="Choose Week",
                        options=all_weeks,
                        value="Week 01")

    def callback(attr, old, new):
        selected = source.selected["1d"]["indices"]

        df_active = select_weeks()

        if selected:
            data = df_active.iloc[selected, :]
            temp = data.set_index("week").T.reindex(index=col_order)
            details.text = temp.style.render()
        else:
            details.text = "Selection Details"

        source.data = ColumnDataSource(data=data).data

    weeks_runs.on_change("value", callback)

    doc.add_root(column(weeks_runs, week_stacked_bar))
    # column(weeks_runs, week_stacked_bar)
    doc.theme = Theme(filename="theme.yaml")

# Setting num_procs here means we can't touch the IOLoop before now, we must
# let Server handle that. If you need to explicitly handle IOLoops then you
# will need to use the lower level BaseServer class.
server = Server({'/bkapp': modify_doc}, num_procs=1, extra_patterns=[('/', IndexHandler)])
server.start()

if __name__ == '__main__':
    from bokeh.util.browser import view

    print('Opening Tornado app with embedded Bokeh application on http://localhost:5006/')

    server.io_loop.add_callback(view, "http://localhost:5006/")
    server.io_loop.start()
