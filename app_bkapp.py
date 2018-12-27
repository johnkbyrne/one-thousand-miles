"""
export FLASK_APP=app.py

"""
import pandas as pd
import io

from flask import Flask, render_template, request, make_response, session, redirect, url_for, jsonify
# from strava_interactivity import selection_change, update, select_weeks, load_weekly, load_data
from bokeh.plotting import figure

from bokeh.server.server import Server
from bokeh.themes import Theme

from bokeh.layouts import layout, widgetbox, column
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool, CustomJS
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool,Range1d
from bokeh.io import curdoc
from bokeh.embed import components, server_session, server_document
from actual_vs_goal_cumulative import actual_goal_cumulative
from stacked_chart import stacked_bar_chart
from weekly_actual_goal import weekly_actual_goal
from static_summary import actual_weekly_vs_goal, summary_cumulative
from bokeh.client import pull_session
from bokeh.resources import INLINE
from bokeh.util.browser import view

from tornado.ioloop import IOLoop

from collections import OrderedDict
from jinja2 import Template

from functools import lru_cache

app = Flask(__name__, template_folder='templates')

def modify_doc(doc):

    @lru_cache()
    def load_data():
        df = pd.read_csv('strava_data.csv', index_col=0)
        return df

    @lru_cache()
    def load_weekly():
        df = pd.read_csv('strava_weekly_data.csv', index_col=0)
        # df['week_number'] = df['week_number'].apply(str)
        return df

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

        # desc.text = f"Week: {week_val}"
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

    # app = Flask(__name__)
    # app.secret_key = 'KEEP_THIS_A SECRET'
    run_data_df = load_data()
    week_data_df = load_weekly()

    all_weeks = list(load_data()['week'].unique())
    all_week_number = list(load_weekly()['week_number'])
    # print(all_week_number)
    X_AXIS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    source = ColumnDataSource(data=load_data())
    weekly_source = ColumnDataSource(data=load_weekly())
    summary_actual = actual_weekly_vs_goal(weekly_source, all_week_number)
    cumulative_actual = summary_cumulative(weekly_source, all_week_number)
    p = weekly_actual_goal(source, X_AXIS)
    week_stacked_bar = stacked_bar_chart(source, X_AXIS)
    weekly_actual_cumulative_fig = actual_goal_cumulative(source, X_AXIS)

    desc = Div(text="Weekly runs", width=800)
    # weeks_runs = Select(title="Choose Week", options=all_weeks, value="Week 01", callback=callback)


    weeks_runs = Select(title="Choose Week",
                        options=all_weeks,
                        value="Week 01",
                        callback=callback)
    # weeks_runs.js_on_change('selected', callback)
    # weeks_runs.js_on_change('value', callback)
    controls = [weeks_runs]
    #
    for control in controls:
        control.on_change("value", lambda attr, old, new: update())


    # source.on_change("selected", selection_change)

    inputs = widgetbox(*controls, sizing_mode="fixed")

    l = layout([[summary_actual],
                [cumulative_actual],
                [desc],
                [weeks_runs],
                [weekly_actual_cumulative_fig],
                [p],
                [week_stacked_bar]], sizing_mode="scale_width")

    # update()
    # curdoc().add_root(l)
    # # curdoc().add_root(column(cumulative_actual))
    # curdoc().title = "Yearly run analysis"

    doc.add_root(l)


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("index.html", script=script, template="Flask")
                            # the_div=div,
							# the_script=script,
							# actual_div=a_div,
							# actual_script=a_script,
                            # layout_script=layout_script,
                            # layout_div=layout_div)


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



# @app.route("/")
# def chart():
    # script, div = components(cumulative_actual)
    # a_script, a_div = components(summary_actual)
    # layout_script, layout_div = components({"weeks_runs": weeks_runs,
    #                                         # "weekly_actual_cumulative_fig": weekly_actual_cumulative_fig,
    #                                         "p" :p,
    #                                         # "week_stacked_bar": week_stacked_bar
    #                                         })
#
#     template = Template('''<!DOCTYPE html>
#     <html lang="en">
#         <head>
#             <meta charset="utf-8">
#             <title>Bokeh Scatter Plots</title>
#             {{ resources }}
#             {{ script|safe }}
#             {{ a_script|safe }}
#             {{ layout_script|safe }}
#             # <style>
#             #     .embed-wrapper {
#             #         display: flex;
#             #         justify-content: space-evenly;
#             #     }
#             # </style>
#         </head>
#         <body>
#             # <div class="embed-wrapper">
#                 {{ div|safe }}
#                 {{ a_div|safe }}
#                 {% for key in layout_div.keys() %}
#                     {{ layout_div[key]|safe }}
#                 {% endfor %}
#             # </div>
#         </body>
#     </html>
#     ''')
#
#     resources = INLINE.render()
#
#     filename = 'templates/index.html'
#
#     html = template.render(resources=resources,
#                            div=div,
#                            script=script,
#                            a_div=a_div,
#                            a_script=a_script,
#                            layout_script=layout_script,
#                            layout_div=layout_div)
#     with io.open(filename, mode='w', encoding='utf-8') as f:
#         f.write(html)
#
#     return render_template('index.html')
#     # return render_template("index.html",
# 	# 						the_div=div,
# 	# 						the_script=script,
# 	# 						actual_div=a_div,
# 	# 						actual_script=a_script,
#     #                         layout_script=layout_script,
#     #                         layout_div=layout_div)
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
