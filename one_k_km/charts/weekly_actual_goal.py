import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, CDSView, GroupFilter

def weekly_actual_goal(source, X_AXIS):

    source = source

    week_1_view = CDSView(source=source,
                       filters=[GroupFilter(column_name='week', group='week 1.0')])

    p = figure(
        plot_height=300,
        plot_width=800,
        title="Weekly running",
        tools='',
        x_axis_label="Day of the week",
        y_axis_label="KMs",
        toolbar_location="above",
        x_range=X_AXIS,
        x_minor_ticks=2, y_range=(0, 20),
        )

    p.vbar(
                x='day_of_week', bottom=0, top='kms',
                color='#084594', width=0.75,
                legend='Actual', source=source,
             )

    p.line(
                x='day_of_week', y='daily_goal',
                color='#9ecae1', line_width=5,
                legend='Goal', source=source,
             )

    tooltips = [
            ('Kilometers','@kms'),
            ('Week number', '@week'),
           ]

# Add the HoverTool to the figure
    p.add_tools(HoverTool(tooltips=tooltips))

    return p

def total_kms_day(source, X_AXIS):

    source = source

    week_1_view = CDSView(source=source,
                       filters=[GroupFilter(column_name='week', group='week 1.0')])

    p = figure(
        plot_height=300,
        plot_width=800,
        title="Total runs for each day of the week",
        x_axis_label="Day of the week",
        y_axis_label="KMs",
        toolbar_location=None,
        x_range=X_AXIS,
        x_minor_ticks=2, y_range=(0, 350),)

    p.vbar(
                x='day_of_week', bottom=0, top='kms',
                color='#084594', width=0.75,
                legend='Actual', source=source,
             )

    tooltips = [
            ('Kilometers','@kms'),
           ]

           # Add the HoverTool to the figure
    p.add_tools(HoverTool(tooltips=tooltips))

    return p
