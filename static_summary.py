import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache

def summary_cumulative(source, X_AXIS):
    source = source
    X_AXIS = [str(x) for x in X_AXIS]

    km_fig = figure(
                      plot_height=300, plot_width=600,
                      title='cumulative actual distance vs goal actual distance',
                      x_axis_label='week_number',
                      y_axis_label='Kms',
                      x_range=X_AXIS,
                      y_range=(0, 1000),
                      toolbar_location=None)


    km_fig.line(x='week_number', y='cumulative_weekly_kms',
             color='blue', line_width=1,
             legend='Cumulative weekly kms',source=source)

    km_fig.vbar(x='week_number', bottom=0, top='cumulative_weekly_kms',
             color='blue', width=0.75,
             legend='Actual', source=source)


    km_fig.line(x='week_number', y='cumulative_weekly_kms',
             color='red', line_width=1,
             legend='Cumulative goal kms',source=source)

    km_fig.legend.location = 'top_left'

    tooltips = [
            ('Cumulative actual Kilometers','@cumulative_weekly_kms'),
            ('Cumulative goal kilometers', '@cumulative_weekly_kms'),
            ('Week number', '@week')
           ]

# Add the HoverTool to the figure
    km_fig.add_tools(HoverTool(tooltips=tooltips))

    return km_fig

def actual_weekly_vs_goal(source, X_AXIS):
    cds_bar = source
    X_AXIS = [str(x) for x in X_AXIS]
    print('in actual weekly vs goal', X_AXIS)
    # Create a figure with a datetime type x-axis
    fig = figure(title='actual versus goals',
                 plot_height=300, plot_width=600,
                 x_axis_label='Week number', y_axis_label='KMs',
                 x_minor_ticks=2,
                 y_range=(0, 50),
                 x_range=X_AXIS,
                 toolbar_location=None)

    # The daily words will be represented as vertical bars (columns)
    fig.vbar(x='week_number', bottom=0, top='kms',
             color='blue', width=0.75,
             legend='Actual', source=cds_bar)

    # The cumulative sum will be a trend line
    fig.line(x='week_number', y='weekly_goal',
             color='red', line_width=1,
             legend='Goal', source=cds_bar)

    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    tooltips = [
                ('Kilometers','@kms'),
                ('Week number', '@week_number'),
               ]

    # Add the HoverTool to the figure
    fig.add_tools(HoverTool(tooltips=tooltips))

    return fig
