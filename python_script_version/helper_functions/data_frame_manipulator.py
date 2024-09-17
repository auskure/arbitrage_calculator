import pandas as pd
import numpy as np

def df_trade_signal_includer(df_combined,
                                ct_open_gemini,
                                ct_open_reuters,
                                buy_signal_gemini,
                                buy_signal_reuters,
                                ct_buy_gemini_sell_reuters):
    #including the trade signal to buy gemini and sell reuters

    temp_frame = pd.DataFrame(np.where(df_combined[ct_open_gemini] > df_combined[ct_open_reuters], 
                                       buy_signal_gemini, 
                                       buy_signal_reuters))
    temp_frame.index = df_combined.index
    temp_frame.columns = [ct_buy_gemini_sell_reuters]
    
    df_combined = pd.concat([df_combined, temp_frame], axis= 1)

    return df_combined

def df_money_earned(df_combined,
                    ct_absolute_difference,
                    ct_trade_volume,
                    ct_total_tax,
                    ct_nett_money_earned):
    #including the column to show how much money would be earned per trade

    temp_frame = pd.DataFrame(df_combined[ct_absolute_difference] * df_combined[ct_trade_volume] 
                              - df_combined[ct_total_tax])
    temp_frame.index = df_combined.index
    temp_frame.columns = [ct_nett_money_earned]
    df_combined = pd.concat([df_combined, temp_frame], axis = 1)

    return df_combined


def df_go_or_no_go_signal(df_combined,
                            ct_nett_money_earned,
                            minimum_earned_per_trade,
                            ct_trade_volume,
                            minimum_volume_per_trade,
                            trade_signal_positive,
                            trade_signal_negative,
                            ct_execute_trade):

    #include the go or no go signals. The trade will only happen if we earn money
    #0 means no go
    #1 means go

    temp_selection = np.logical_and((df_combined[ct_nett_money_earned] > minimum_earned_per_trade),  
                                    (df_combined[ct_trade_volume] > minimum_volume_per_trade))

    temp_frame = pd.DataFrame(np.where(temp_selection,
                                       trade_signal_positive,
                                       trade_signal_negative))
    temp_frame.index = df_combined.index
    temp_frame.columns = [ct_execute_trade]
    df_combined = pd.concat([df_combined, temp_frame], axis= 1)

    return df_combined


def df_output_writer(result_file, 
                      theoretical_max, 
                      orders_fulfilled, 
                      output_theoretical_max = "Theoretical Max: {:.2f}\n",
                      output_orders_fulfilled = "\norder fulfilled output below \n\n",
                      to_round_value = 2,
                      output_string = "Completed successfully! Check {}",
                      result_folder = "./results/"):


    toWrite = open(result_folder + result_file, 'w')
    toWrite.write(output_theoretical_max.format(theoretical_max))
    toWrite.write(output_orders_fulfilled)
    toWrite.write(orders_fulfilled.round(to_round_value).to_string())
    print(output_string.format(result_folder + result_file))
