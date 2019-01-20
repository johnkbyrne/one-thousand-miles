import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache

def stacked_bar_chart(source, x_axis):

    source = source

    stack_kms_goals = figure(x_range=x_axis,
                             plot_height=300,
                             plot_width=800,
                             title="runs by day",
                             toolbar_location=None,
                             tools="",
                             x_axis_label='Day of the week',
                             y_axis_label='KMS',)

    colors = ['#9ecae1', '#084594']
    km_type = ['weekly_actual_cumulative', 'diff_actual_vs_total']

    stack_kms_goals.vbar_stack(km_type,
                                x='day_of_week',
                                width=0.9,
                                color=colors,
                                source=source)

    stack_kms_goals.y_range.start = 0
    stack_kms_goals.x_range.range_padding = 0.1
    stack_kms_goals.xgrid.grid_line_color = None
    stack_kms_goals.axis.minor_tick_line_color = None
    stack_kms_goals.outline_line_color = None
    stack_kms_goals.legend.location = "top_left"
    stack_kms_goals.legend.orientation = "horizontal"
    tooltips = [
            ('Actual KMS','@weekly_actual_cumulative'),
            ('Completed of total', '@diff_actual_vs_total'),
           ]

# Add the HoverTool to the figure
    stack_kms_goals.add_tools(HoverTool(tooltips=tooltips))
    return stack_kms_goals
