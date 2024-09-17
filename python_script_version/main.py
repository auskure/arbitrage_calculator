import pandas as pd
import numpy as np

from helper_functions.data_frame_manipulator import df_trade_signal_includer, df_money_earned, df_go_or_no_go_signal, df_output_writer
from helper_functions.dataset_reader import read_in_datasets
from helper_functions.graph_plotter import plot_price_change_graph


#variables declaration
trading_fees = 2 #as a percentage
minimum_earned_per_trade = 1 #minimum amount of money to earn per trade
minimum_volume_per_trade = 5 #minimum amount of volume required for each trade

#dataset location declaration
main_data_location = '../data/BTCPrices.xlsx'
price_sheet_gemini = 'Gemini'
price_sheet_reuters = 'Reuters'

buy_signal_gemini = 0 #signal to buy Gemini and sell in Reuters
buy_signal_reuters = 1 #signal to buy in Reuters and sell in Gemini
trade_signal_positive = 1 #signal to go ahead with the trade
trade_signal_negative = 0 #signal to not continue with the trade

#variables for data cleaning and formatting
index_title_gemini = 'Date (EST)'
index_title_reuters = 'Time'

price_title_gemini = 'Open'
price_title_reuters = 'Open'
trade_volume_title = 'Volume'

#variable for analysis, where CT stands for column title
ct_open_gemini = 'Gemini_Open'
ct_open_reuters = 'Reuters_Open'
ct_trade_volume = 'Trade_Volume'
ct_absolute_difference = 'Absolute_Difference'
ct_total_tax = 'Total_Tax'
ct_buy_gemini_sell_reuters = 'BuyGemSellReuOrder'
ct_nett_money_earned = 'Money_Earned'
ct_execute_trade = 'Execute'

#output file
result_file = "calculation.txt"


trading_fees = trading_fees/100 #converting into percentages

#reading in datasets
df_gemini, df_reuters = read_in_datasets(main_data_location, 
                                            price_sheet_gemini, 
                                            price_sheet_reuters,
                                            index_title_gemini,
                                            index_title_reuters)

#extracting relevant columns of dataframe
price_gemini = df_gemini[price_title_gemini]
price_reuters = df_reuters[price_title_reuters]
trade_volume = df_gemini[trade_volume_title]

plot_price_change_graph(price_gemini,
                        price_reuters,
                        index_title_gemini,
                        index_title_reuters,
                        price_title_gemini,
                        price_title_reuters,
                        trade_volume_title)


#calculating theoretical max earnings
theoretical_max = sum(abs(price_gemini - price_reuters) * trade_volume)


#creating the main dataframe
#taking fees into account. For this analysis, we are assuming a 2% fee on both the buy and sell side
df_combined = pd.concat([price_gemini,
                         price_reuters,
                         trade_volume,
                         abs(price_gemini - price_reuters),
                         trading_fees * (price_gemini + price_reuters)], axis = 1) 

df_combined.columns = [ct_open_gemini, 
                       ct_open_reuters, 
                       ct_trade_volume, 
                       ct_absolute_difference, 
                       ct_total_tax]

#include the trade signals. 
df_combined = df_trade_signal_includer(df_combined,
                                        ct_open_gemini,
                                        ct_open_reuters,
                                        buy_signal_gemini,
                                        buy_signal_reuters,
                                        ct_buy_gemini_sell_reuters)


#include the amount of money earned post commission fees, per trade
df_combined = df_money_earned(df_combined,
                                ct_absolute_difference,
                                ct_trade_volume,
                                ct_total_tax,
                                ct_nett_money_earned)

#include the go or no go signal
df_combined = df_go_or_no_go_signal(df_combined,
                                    ct_nett_money_earned,
                                    minimum_earned_per_trade,
                                    ct_trade_volume,
                                    minimum_volume_per_trade,
                                    trade_signal_positive,
                                    trade_signal_negative,
                                    ct_execute_trade)

#check which orders are fulfilled
orders_fulfilled = df_combined.loc[df_combined[ct_execute_trade] == trade_signal_positive]


#writing essential outputs to a text file
df_output_writer(result_file, theoretical_max, orders_fulfilled)
