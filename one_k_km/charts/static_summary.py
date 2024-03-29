import pandas as pd
from bokeh.plotting import figure

from bokeh.models import ColumnDataSource, HoverTool

def summary_cumulative(source, X_AXIS):
    source = source
    X_AXIS = [str(x) for x in X_AXIS]

    km_fig = figure(
                      plot_height=300, plot_width=800,
                      title='Cumulative KMs Run vs Goal KMs',
                      x_axis_label='week_number',
                      y_axis_label='Kms',
                      x_range=X_AXIS,
                      y_range=(0, 1010),
                      toolbar_location=None)


    km_fig.line(
                x='week_number', y='cumulative_weekly_kms',
                color='#9ecae1', line_width=3,
                legend='Cumulative weekly kms',source=source
             )

    km_fig.vbar(
                x='week_number', bottom=0, top='cumulative_weekly_kms',
                color='#084594', width=0.75,
                legend='KMs Run', source=source
                )


    km_fig.line(
                x='week_number', y='cumulative_weekly_goal_kms',
                color='#9ecae1', line_width=3,
                legend='Cumulative goal kms',source=source
                )

    km_fig.legend.location = 'top_left'

    tooltips = [
            ('Cumulative actual Kilometers','@cumulative_weekly_kms'),
            ('Cumulative goal kilometers', '@cumulative_weekly_goal_kms'),
            ('Week number', '@week')
           ]

# Add the HoverTool to the figure
    km_fig.add_tools(HoverTool(tooltips=tooltips))

    return km_fig

def actual_weekly_vs_goal(source, X_AXIS):
    cds_bar = source
    X_AXIS = [str(x) for x in X_AXIS]

    # Create a figure with a datetime type x-axis
    fig = figure(
                    title='Actual KMs Run versus Goal KMs',
                    plot_height=300, plot_width=800,
                    x_axis_label='Week number', y_axis_label='KMs',
                    x_minor_ticks=2,
                    y_range=(0, 50),
                    x_range=X_AXIS,
                    toolbar_location=None
                    )

    # The daily words will be represented as vertical bars (columns)
    fig.vbar(
                x='week_number', bottom=0, top='kms',
                color='#084594', width=0.75,
                legend='KMS Run', source=cds_bar
                )

    # The cumulative sum will be a trend line
    fig.line(
                x='week_number', y='weekly_goal',
                color='#9ecae1', line_width=1,
                legend='Goal KMs', source=cds_bar
                )

    # Put the legend in the upper left corner
    fig.legend.location = 'top_left'

    tooltips = [
                ('Kilometers','@kms'),
                ('Week number', '@week_number'),
               ]

    # Add the HoverTool to the figure
    fig.add_tools(HoverTool(tooltips=tooltips))

    return fig
