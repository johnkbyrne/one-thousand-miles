
# coding: utf-8

# In[1]:


import pandas as pd
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache


# In[10]:


@lru_cache()
def load_data():
    df = pd.read_csv('strava_data.csv', index_col=0)
    return df


# In[11]:


run_data_df = load_data()


# In[91]:


# all_weeks = list(set(list(load_data()['week'])))
all_weeks = list(load_data()['week'].unique())
X_AXIS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


# In[92]:


desc = Div(text="Weekly runs", width=800)
weeks_runs = Select(title="Runs", options=all_weeks, value="All")


# In[93]:


source = ColumnDataSource(data=load_data())


# In[94]:


hover = HoverTool(tooltips=[
    ("Week", "@week"),
    ("Kilometers", "@kms"),
])
TOOLS = [
    hover, BoxZoomTool(), LassoSelectTool(), WheelZoomTool(), PanTool(),
    ResetTool(), SaveTool()
]


# In[95]:


p = figure(
    plot_height=600,
    plot_width=700,
    title="Weekly running",
    tools=TOOLS,
    x_axis_label="kms",
    y_axis_label="day od the week",
    toolbar_location="above", 
    x_range=X_AXIS,
    x_minor_ticks=2, y_range=(0, 15),)

p.vbar(x='day_of_week', bottom=0, top='kms', 
         color='blue', width=0.75, 
         legend='Actual', source=source)


# In[96]:


def select_weeks():
    """ Use the current selections to determine which filters to apply to the
    data. Return a dataframe of the selected data
    """
    df = load_data()

    # Determine what has been selected for each widgetd
#     cumulative_week_val = weeks_runs.value
    week_val = weeks_runs.value
#     kilometers_val = kms.value

    # Filter by week and weekly_actual_cumulative
    if week_val == "week 01":
        selected = df[df.week == 'week 01'] 
    else:
        selected = df[(df.week == week_val)]

    # Further filter by string in title if it is provided
#     if title_val != "":
#         selected = selected[selected.title.str.contains(title_val, case=False) == True]

#     # Example showing how to update the description
    desc.text = f"Week: {week_val}"
    return selected


# In[97]:


def update():
    """ Get the selected data and update the data in the source
    """
    df_active = select_weeks()
    source.data = ColumnDataSource(data=df_active).data


# In[98]:


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


    
    


# In[99]:



controls = [weeks_runs]

for control in controls:
    control.on_change("value", lambda attr, old, new: update())

source.on_change("selected", selection_change)

inputs = widgetbox(*controls, sizing_mode="fixed")
l = layout([[desc], [weeks_runs, p]], sizing_mode="fixed")


# In[100]:


update()
curdoc().add_root(l)
curdoc().title = "Yearly run analysis"

