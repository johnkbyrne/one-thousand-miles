import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache

def actual_goal_cumulative(source, x_axis):
    cds_bar = source

    # Create a figure with a datetime type x-axis
    fig = figure(title='actual versus goals',
                 plot_height=500, plot_width=800,
                 x_axis_label='Week Number', y_axis_label='Cumulative KMs',
                 x_minor_ticks=2, y_range=(0, 50),
                 x_range=x_axis,
                 toolbar_location=None,
                 )

    # The daily words will be represented as vertical bars (columns)
    fig.vbar(x='day_of_week', bottom=0, top='weekly_actual_cumulative',
             color='#084594', width=0.75,
             legend='Actual', source=cds_bar)

    # The cumulative sum will be a trend line
    fig.line(x='day_of_week', y='weekly_goal_cumulative',
             color='#9ecae1', line_width=4,
             legend='Goal', source=cds_bar)

    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    tooltips = [
                ('Cumulative Kilometers','@weekly_goal_cumulative'),
                ('Cumulative goal KMS', '@week'),
               ]

    # Add the HoverTool to the figure
    fig.add_tools(HoverTool(tooltips=tooltips))

    return fig
