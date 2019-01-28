import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

def actual_goal_cumulative(source, x_axis):
    cds_bar = source

    fig = figure(
                    title='Actual KMs versus goal KMs',
                    plot_height=500, plot_width=800,
                    x_axis_label='Week Number', y_axis_label='Cumulative KMs',
                    x_minor_ticks=2, y_range=(0, 50),
                    x_range=x_axis,
                    toolbar_location=None,
                 )

    fig.vbar(
                x='day_of_week', bottom=0, top='weekly_actual_cumulative',
                color='#084594', width=0.75,
                legend='KMs Run', source=cds_bar,
             )


    fig.line(
                x='day_of_week', y='weekly_goal_cumulative',
                color='#9ecae1', line_width=4,
                legend='Goal KMs', source=cds_bar,
             )

    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    tooltips = [
                ('Cumulative Kilometers','@weekly_goal_cumulative'),
                ('Cumulative goal KMS', '@week'),
               ]

    # Add the HoverTool to the figure
    fig.add_tools(HoverTool(tooltips=tooltips))

    return fig
