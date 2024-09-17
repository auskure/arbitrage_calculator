import pandas as pd

def read_in_datasets(main_data_location, 
                    gemini_price_sheet, 
                    reuters_price_sheet,
                    gemini_index_title,
                    reuters_index_title):

    df_Gemini = pd.read_excel(main_data_location, sheet_name = gemini_price_sheet, na_values = None)
    df_Reuters = pd.read_excel(main_data_location, sheet_name = reuters_price_sheet)

    df_Gemini = df_Gemini.set_index(gemini_index_title)
    df_Reuters = df_Reuters.set_index(reuters_index_title)

    return df_Gemini, df_Reuters