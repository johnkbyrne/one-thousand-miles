import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache

def weekly_actual_goal(source, X_AXIS):

    source = source

    hover = HoverTool(tooltips=[
        ("Week", "@week"),
        ("Kilometers", "@kms"),
    ])
    TOOLS = [
        hover, BoxZoomTool(), LassoSelectTool(), WheelZoomTool(), PanTool(),
        ResetTool(), SaveTool()
    ]

    p = figure(
        plot_height=300,
        plot_width=600,
        title="Weekly running",
        tools='',
        x_axis_label="Day of the week",
        y_axis_label="day of the week",
        toolbar_location="above",
        x_range=X_AXIS,
        x_minor_ticks=2, y_range=(0, 15),)

    p.vbar(x='day_of_week', bottom=0, top='kms',
             color='blue', width=0.75,
             legend='Actual', source=source)

    p.line(x='day_of_week', y='daily_goal',
             color='red', line_width=5,

             legend='Goal', source=source)

    tooltips = [
            ('Kilometers','@kms'),
            ('Week number', '@week'),
           ]

# Add the HoverTool to the figure
    p.add_tools(HoverTool(tooltips=tooltips))

    return p
