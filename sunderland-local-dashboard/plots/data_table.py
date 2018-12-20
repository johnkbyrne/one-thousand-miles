import pandas as pd
from bokeh.core.properties import value
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import widgetbox
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn

class CouncilDataTable(object):
  def __init__(self, dataframe):
    self.dataframe = dataframe
    self.dataframe = self.dataframe[-1:]
    self.source = ColumnDataSource(self.dataframe)
  #
  def transform(self, df):
    # Filter data to only the selected week
    df = df[df["week"] == self.week]
    df.reset_index(inplace=True)
    print(df.head())
    return df[:-1]

  def set_data(self, data):
    self.dataframe = data
    self.source.data = self.source(self.transform(self.dataframe))

  def set_week(self, week):
    self.week = self.weeks[week]
    self.source.data = self.source(self.transform(self.dataframe))

  def plot(self):

    # data = self.source.to_df()

    columns = [
        TableColumn(field="Week commencing", title="Week commencing"),
        TableColumn(field="Weekly visits", title="Weekly Visits"),
        TableColumn(field="Unique visitors", title="Weekly Unique Visits"),
        TableColumn(field="Weekly pageviews", title="Weekly pageviews"),
        TableColumn(field="Average time on page", title="Average time on page")
    ]
    data_table = DataTable(source=self.source, columns=columns, height=100, width=900,row_headers=False)

    return data_table
