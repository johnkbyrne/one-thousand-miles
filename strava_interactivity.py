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

@lru_cache()
def load_data():
    df = pd.read_csv('strava_data.csv', index_col=0)
    return df

run_data_df = load_data()

all_weeks = list(load_data()['week'].unique())
X_AXIS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


desc = Div(text="Weekly runs", width=800)
weeks_runs = Select(title="Choose Week", options=all_weeks, value="Week 01")

source = ColumnDataSource(data=load_data())
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

controls = [weeks_runs]

for control in controls:
    control.on_change("value", lambda attr, old, new: update())

source.on_change("selected", selection_change)

inputs = widgetbox(*controls, sizing_mode="fixed")
l = layout([[desc],
            [weeks_runs],
            [weekly_actual_cumulative_fig],
            [p],
            [week_stacked_bar]], sizing_mode="scale_width")

update()
curdoc().add_root(l)
curdoc().title = "Yearly run analysis"
