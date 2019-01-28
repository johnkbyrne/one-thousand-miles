import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox, gridplot, column, row
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import Select, Div
from bokeh.io import curdoc
from functools import lru_cache

from charts.actual_vs_goal_cumulative import actual_goal_cumulative
from charts.stacked_chart import stacked_bar_chart
from charts.weekly_actual_goal import weekly_actual_goal, total_kms_day
from charts.static_summary import actual_weekly_vs_goal, summary_cumulative

from flask import Flask, render_template

from bokeh.embed import server_document, components
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop

app = Flask(__name__)

@lru_cache()
def load_data():
    df = pd.read_csv('data/strava_data.csv', index_col=0)
    return df

@lru_cache()
def load_weekly():
    df = pd.read_csv('data/strava_weekly_data.csv', index_col=0)

    return df

run_data_df = load_data()
total_kms = run_data_df['kms'].sum()
day_group = run_data_df.groupby('day_of_week').sum()

weekly_source = ColumnDataSource(data=load_weekly())
all_week_number = list(load_weekly()['week_number'])

def modify_doc(doc):

    all_weeks = list(load_data()['week'].unique())
    all_week_number = list(load_weekly()['week_number'])

    X_AXIS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    desc = Div(text="Weekly runs", width=800)
    weeks_runs = Select(title="Choose Week", options=all_weeks, value="week 1.0", width=600)
    source = ColumnDataSource(data=load_data())
    weekly_source = ColumnDataSource(data=load_weekly())

    day_source = ColumnDataSource(data=day_group)

    summary_actual = actual_weekly_vs_goal(weekly_source, all_week_number)
    cumulative_actual = summary_cumulative(weekly_source, all_week_number)
    p = weekly_actual_goal(source, X_AXIS)
    week_stacked_bar = stacked_bar_chart(source, X_AXIS)
    weekly_actual_cumulative_fig = actual_goal_cumulative(source, X_AXIS)
    day_total = total_kms_day(day_source, X_AXIS)

    def select_weeks():
        """ Use the current selections to determine which filters to apply to the
        data. Return a dataframe of the selected data
        """
        df = load_data()

        # Determine what has been selected for each widgetd
        week_val = weeks_runs.value

        # Filter by week
        if week_val == "week 1.0":
            selected = df[df.week == 'week 1.0']
        else:
            selected = df[(df.week == week_val)]

        desc.text = f"Showing data for {week_val}"

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

    charts_all = [summary_actual,
                cumulative_actual]

    for chart_all in charts_all:
        doc.add_root(column(chart_all))

    doc.add_root(column(day_total))

    doc.add_root(gridplot(
        children=[[control,desc], [weekly_actual_cumulative_fig, p]],
        toolbar_location='right',
        sizing_mode='fixed',
        plot_width = 400,
        plot_height = 300,
        merge_tools = True,
        toolbar_options=dict(logo='grey')
    ))

    doc.add_root(column(week_stacked_bar))

@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')


    return render_template(
                            "embed.html",
                            script=script,
                            template="Flask",
                            total_kms=total_kms,
                            )

def bk_worker():
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])

    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    app.run(port=8000)
