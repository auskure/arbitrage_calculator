import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def plot_price_change_graph(price_gemini,
                            price_reuters,
                            gemini_index_title,
                            reuters_index_title,
                            gemini_price_title,
                            reuters_price_title,
                            trade_volume_title,
                            figure_length = 8, 
                            figure_breadth = 4,
                            figure_dpi = 200,
                            gemini_legend_title = 'Gemini BTC',
                            reuters_legend_title = 'Reuters BTC',
                            figure_title = 'BTC Opening Prices',
                            figure_save_name = 'priceComparison.png',
                            result_folder = './results/',
                            output_string = 'Price change graph successfully saved in {}'):

    


    figure(figsize=(figure_length, figure_breadth), dpi=figure_dpi)


    plt.plot(price_gemini, label = gemini_legend_title)
    plt.plot(price_reuters, label = reuters_legend_title)
    plt.title(figure_title)
    plt.legend()
    plt.savefig(result_folder + figure_save_name)
    print(output_string.format(result_folder + figure_save_name))