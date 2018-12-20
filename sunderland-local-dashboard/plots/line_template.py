from bokeh.core.properties import value
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, RadioButtonGroup, DatetimeTicker, ContinuousTicker, FixedTicker
from bokeh.plotting import figure

class CouncilLineChart(object):
  def __init__(self, dataframe, columns, chart_title):
    self.columns = columns
    self.chart_title = chart_title
    self.dataframe = dataframe
    self.source = ColumnDataSource(self.dataframe)

  # def transform(self, df):
  #   # df = df[df["idp"] == self.idp]
  #   # df.reset_index(inplace=True)
  #   # df = df[df['segment_name'] == self.segment]
  #   # return df
  #   pass
  #
  # def set_idp(self, idp):
  #   # self.idp = self.idps[idp]
  #   # self.source.data = ColumnDataSource.from_df(self.transform(self.dataframe))
  #   pass
  #
  # def set_segment(self, segment):
  #   # self.segment = self.segments[segment]
  #   # self.source.data = ColumnDataSource.from_df(self.transform(self.dataframe))
  #   pass

  def get_lines(self, column, p, colour):
      p.line(x='Week commencing', y=column, source=self.source, color=colour, line_width=2, legend=value(column))
      return p


  def plot(self):
    p = figure(x_axis_type="datetime", title=self.chart_title, plot_height=500, plot_width=900, tools="")
    colours = ["#2E358B", "#D53880", "#DF3034", "#F47738", "#FFBF47", "#28A197", "#006435"]
    clr = 0
    for column in self.columns:

        self.get_lines(column, p, colours[clr])
        clr+=1

    p.legend.click_policy="hide"
    # line_ticks = range(1, len(self.dataframe)+1)
    # line_ticks = [float(x) for x in line_ticks]

    # p.xaxis.ticker = FixedTicker(ticks=line_ticks)
    # p.xaxis.ticker = [1,2,3,4]
    # p.xaxis.ticker
    # idp_selector = RadioButtonGroup(labels=self.idps, active=0)
    # idp_selector.on_click(self.set_idp)
    # segment_selector = RadioButtonGroup(labels=self.segments, active=0)
    # segment_selector.on_click(self.set_segment)
    return p
