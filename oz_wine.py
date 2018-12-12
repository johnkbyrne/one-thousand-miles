

import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models.widgets import Slider, Select, TextInput, Div
from bokeh.models import WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.io import curdoc
from functools import lru_cache


# In[13]:


wine_csv = 'https://raw.githubusercontent.com/chris1610/pbpython/master/data/Aussie_Wines_Plotting.csv'


# In[34]:


@lru_cache()
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/chris1610/pbpython/master/data/Aussie_Wines_Plotting.csv', index_col=0)
    return df


# In[15]:


# Column order for displaying the details of a specific review
col_order = ["price", "points", "variety", "province", "description"]

all_provinces = [
    "All", "South Australia", "Victoria", "Western Australia",
    "Australia Other", "New South Wales", "Tasmania"
]


# In[16]:


desc = Div(text="All Provinces", width=800)
province = Select(title="Province", options=all_provinces, value="All")
price_max = Slider(start=0, end=900, step=5, value=200, title="Maximum Price")
title = TextInput(title="Title Contains")
details = Div(text="Selection Details:", width=800)


# In[18]:


source = ColumnDataSource(data=load_data(wine_csv))


# In[19]:


hover = HoverTool(tooltips=[
    ("title", "@title"),
    ("variety", "@variety"),
])
TOOLS = [
    hover, BoxZoomTool(), LassoSelectTool(), WheelZoomTool(), PanTool(),
    ResetTool(), SaveTool()
]


# In[23]:


p = figure(
    plot_height=600,
    plot_width=700,
    title="Australian Wine Analysis",
    tools=TOOLS,
    x_axis_label="points",
    y_axis_label="price (USD)",
    toolbar_location="above")

p.circle(
    y="price",
    x="points",
    source=source,
    color="variety_color",
    size=7,
    alpha=0.4)


# In[24]:


def select_reviews():
    """ Use the current selections to determine which filters to apply to the
    data. Return a dataframe of the selected data
    """
    df = load_data()

    # Determine what has been selected for each widgetd
    max_price = price_max.value
    province_val = province.value
    title_val = title.value

    # Filter by price and province
    if province_val == "All":
        selected = df[df.price <= max_price]
    else:
        selected = df[(df.province == province_val) & (df.price <= max_price)]

    # Further filter by string in title if it is provided
    if title_val != "":
        selected = selected[selected.title.str.contains(title_val, case=False) == True]

    # Example showing how to update the description
    desc.text = "Province: {} and Price < {}".format(province_val, max_price)
    return selected


# In[25]:


def update():
    """ Get the selected data and update the data in the source
    """
    df_active = select_reviews()
    source.data = ColumnDataSource(data=df_active).data


# In[39]:


def selection_change(attrname, old, new):
    """ Function will be called when the poly select (or other selection tool)
    is used. Determine which items are selected and show the details below
    the graph
    """
    selected = source.selected["1d"]["indices"]
    
    df_active = select_reviews()
    
    if selected:
        data = df_active.iloc[selected, :]
        temp = data.set_index("title").T.reindex(index=col_order)
        details.text = temp.style.render()
    else:
        details.text = "Selection Details"
        
        
    


# In[40]:


controls = [province, price_max, title]

for control in controls:
    control.on_change("value", lambda attr, old, new: update())


# In[41]:


source.on_change("selected", selection_change)


# In[42]:


inputs = widgetbox(*controls, sizing_mode="fixed")
l = layout([[desc], [inputs, p], [details]], sizing_mode="fixed")


# In[43]:


update()
curdoc().add_root(l)
curdoc().title = "Australian Wine Analysis"


# In[ ]:




