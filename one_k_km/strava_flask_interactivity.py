import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox, gridplot
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache

from actual_vs_goal_cumulative import actual_goal_cumulative
from stacked_chart import stacked_bar_chart
from weekly_actual_goal import weekly_actual_goal
from static_summary import actual_weekly_vs_goal, summary_cumulative

from flask import Flask, render_template

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop

app = Flask(__name__)
# this is the bokeh server app that works with running bokeh serve strava_interactivity.py and the
# core that I need to get running encapsulating in a flask or tornado framework

import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache

from actual_vs_goal_cumulative import actual_goal_cumulative
from stacked_chart import stacked_bar_chart
from weekly_actual_goal import weekly_actual_goal
from static_summary import actual_weekly_vs_goal, summary_cumulative

@lru_cache()
def load_data():
    df = pd.read_csv('data/strava_data.csv', index_col=0)
    return df

@lru_cache()
def load_weekly():
    df = pd.read_csv('data/strava_weekly_data.csv', index_col=0)
    # df['week_number'] = df['week_number'].apply(str)
    return df

run_data_df = load_data()
total_kms = run_data_df['kms'].sum()

weekly_source = ColumnDataSource(data=load_weekly())
all_week_number = list(load_weekly()['week_number'])
# summary_actual = actual_weekly_vs_goal(weekly_source, all_week_number)
# cumulative_actual = summary_cumulative(weekly_source, all_week_number)
# l = layout([[summary_actual]], sizing_mode="scale_width")
def modify_doc(doc):
    run_data_df = load_data()
    week_data_df = load_weekly()

    all_weeks = list(load_data()['week'].unique())
    all_week_number = list(load_weekly()['week_number'])
    # print(all_week_number)
    X_AXIS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


    desc = Div(text="Weekly runs", width=800)
    weeks_runs = Select(title="Choose Week", options=all_weeks, value="Week 01")

    source = ColumnDataSource(data=load_data())
    weekly_source = ColumnDataSource(data=load_weekly())

    summary_actual = actual_weekly_vs_goal(weekly_source, all_week_number)
    cumulative_actual = summary_cumulative(weekly_source, all_week_number)
    p = weekly_actual_goal(source, X_AXIS)
    week_stacked_bar = stacked_bar_chart(source, X_AXIS)
    weekly_actual_cumulative_fig = actual_goal_cumulative(source, X_AXIS)

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

        desc.text = f"Week: {week_val}"
        return selected

    def update():
        """ Get the selected data and update the data in the source
        """
        df_active = select_weeks()
        source.data = ColumnDataSource(data=df_active).data

    controls = [weeks_runs]

    for control in controls:
        control.on_change("value", lambda attr, old, new: update())


    inputs = widgetbox(*controls, sizing_mode="fixed")


    charts = [
                summary_actual,
                cumulative_actual,
                desc,
                control,
                weekly_actual_cumulative_fig,
                p,
                week_stacked_bar]

    for chart in charts:
        doc.add_root(column(chart))


    doc.theme = Theme(filename="theme.yaml")


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask",
                            total_kms=total_kms)


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])

    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)
