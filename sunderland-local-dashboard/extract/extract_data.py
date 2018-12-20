import pandas as pd
import pygsheets
import json

class ExtractFromSheets:

    def get_data_from_sheets(self, sheet_key):

        gc = pygsheets.authorize(service_file='./creds/verify-local-dashboards-3faefa0420fa.json')

        sh = gc.open_by_key(sheet_key)

        wks = sh.worksheet_by_title('Form responses 1')

        sheets_df = wks.get_as_df(has_header=True, index_colum=None, start=None, end=None, numerize=True)
        # sheets_df.rename(columns={'Weekly Visits ': 'Weekly Visits',
        #                         'Weekly Unique Visits ': 'Weekly Unique Visits',
        #                         'Weekly pageviews': 'Weekly pageviews'
        #                         })
        
        return sheets_df
