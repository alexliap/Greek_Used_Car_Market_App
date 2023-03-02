import numpy as np
import plotly.express as px
from .search_options import *


def brand_bar_chart(df, brand, min_km = 0, max_km = 0, min_price = 0,
                    max_price = 0, min_cc = 0, max_cc = 0, min_hp = 0,
                    max_hp = 0):
    """
    Produces bar chart for the 'search by brand' page showing most popular
    brand's models.
    :param df: Dataframe Data
    :param brand: Brand of choice
    :param min_km: Search option for minimum mileage
    :param max_km: Search option for maximum mileage
    :param min_price: Search option for minimum price
    :param max_price: Search option for maximum price
    :param min_cc: Search option for minimum displacement
    :param max_cc: Search option for maximum displacement
    :param min_hp: Search option for minimum horsepower
    :param max_hp: Search option for maximum horsepower
    :return: figure (bar chart)
    """
    if brand is not None:
        """
        Search by km, price, cc, hp. 
        """
        df = km_search(df, min_km, max_km)
        df = price_search(df, min_price, max_price)
        df = cc_search(df, min_cc, max_cc)
        df = hp_search(df, min_hp, max_hp)
        """
        Group by brand df by model.
        """
        dummy = df[df['brand'] == brand].groupby(['model'],
                                                 as_index = False).size().sort_values(ascending = False, by = 'size')
        dummy.reset_index(drop = True, inplace = True)
        """
        Make sure that 'Unknown' model category is not the first shown in chart.
        """
        top_car = 0
        if dummy['model'][top_car] == 'Unknown':
            top_car = 1
        """
        Increase the models represented by 'Other' category in chart if the 
        most popular model has less then 50 counts.
        """
        if dummy['size'][top_car] >= 50:
            dummy['ignored'] = dummy['size'] < np.round(0.1 * dummy['size'][top_car])
        else:
            dummy['ignored'] = dummy['size'] < np.round(0.3 * dummy['size'][top_car])
        """
        Produce the chart.
        """
        dummy['ignored'][dummy['model'] == 'Unknown'] = True
        dummy.loc[len(dummy)] = ['Other',
                                 sum(dummy['size'][dummy['ignored'] == True]),
                                 False]
        fig = px.bar(dummy, x = dummy['model'][dummy['ignored'] == False],
                     y = dummy['size'][dummy['ignored'] == False],
                     title = f'{brand} Models Popularity',
                     color = dummy['model'][dummy['ignored'] == False],
                     width = 600,
                     height = 500)
        fig.update_layout(xaxis_title = f"{brand} Models",
                          yaxis_title = "Number of Vehicles",
                          legend_title = "Models", title = {'x': 0},
                          xaxis_type = 'category')
        return fig
    else:
        pass


def brand_pie_chart(df, brand, min_km = 0, max_km = 0, min_price = 0,
                    max_price = 0, min_cc = 0, max_cc = 0, min_hp = 0,
                    max_hp = 0):
    """
    Produces pie chart for the 'search by brand' page showing the percentage
    share of brand's models.
    :param df: Dataframe Data
    :param brand: Brand of choice
    :param min_km: Search option for minimum mileage
    :param max_km: Search option for maximum mileage
    :param min_price: Search option for minimum price
    :param max_price: Search option for maximum price
    :param min_cc: Search option for minimum displacement
    :param max_cc: Search option for maximum displacement
    :param min_hp: Search option for minimum horsepower
    :param max_hp: Search option for maximum horsepower
    :return: figure (pie chart)
    """
    if brand is not None:
        """
        Search by km, price, cc, hp. 
        """
        df = km_search(df, min_km, max_km)
        df = price_search(df, min_price, max_price)
        df = cc_search(df, min_cc, max_cc)
        df = hp_search(df, min_hp, max_hp)
        """
        Group by brand df by model.
        """
        dummy = df[df['brand'] == brand].groupby(['model'],
                                                 as_index = False).size().sort_values(ascending = False, by = 'size')
        dummy.reset_index(drop = True, inplace = True)
        """
        Make sure that 'Unknown' model category is not the first shown in chart.
        """
        top_car = 0
        if dummy['model'][top_car] == 'Unknown':
            top_car = 1
        """
        Increase the models represented by 'Other' category in chart if the 
        most popular model has less then 50 counts.
        """
        if dummy['size'][top_car] >= 50:
            dummy['ignored'] = dummy['size'] < np.round(0.1 * dummy['size'][top_car])
        else:
            dummy['ignored'] = dummy['size'] < np.round(0.3 * dummy['size'][top_car])
        """
        Produce the chart.
        """
        dummy['ignored'][dummy['model'] == 'Unknown'] = True
        dummy.loc[len(dummy)] = ['Other',
                                 sum(dummy['size'][dummy['ignored'] == True]),
                                 False]
        fig = px.pie(dummy, values = dummy['size'][dummy['ignored'] == False],
                     names = dummy['model'][dummy['ignored'] == False],
                     title = f'Population Share of {brand} Models', width = 600,
                     height = 500)
        fig.update_traces(textposition = 'inside', textinfo = 'percent+label')
        fig.update_layout(legend_title = "Models", title = {'x': 0})

        return fig
    else:
        pass


def model_histogram_chart(df, brand: str, model: str, min_km, max_km,
                          min_price, max_price, min_cc, max_cc, min_hp, max_hp):
    """
    Produces histogram for the 'search by model' page showing price
    distribution of certain car model.
    :param df: Dataframe Data
    :param brand: Brand of choice
    :param model: Car model
    :param min_km: Search option for minimum mileage
    :param max_km: Search option for maximum mileage
    :param min_price: Search option for minimum price
    :param max_price: Search option for maximum price
    :param min_cc: Search option for minimum displacement
    :param max_cc: Search option for maximum displacement
    :param min_hp: Search option for minimum horsepower
    :param max_hp: Search option for maximum horsepower
    :return: figure (histogram)
    """
    if model is not None:
        """
        Search by km, price, cc, hp. 
        """
        df = km_search(df, min_km, max_km)
        df = price_search(df, min_price, max_price)
        df = cc_search(df, min_cc, max_cc)
        df = hp_search(df, min_hp, max_hp)
        """
        Create df by quering brand and model.
        Ignoring rows where price equals 'Ask price'.
        And converting price column to int.
        """
        dummy = df.query(f'brand == "{brand}"').query(f'model == "{model}"')
        dummy = dummy.query('price != "Ask price"')
        """
        Produce the chart.
        """
        fig = px.histogram(dummy, x = 'price', nbins = 20, color = 'fuel',
                           width = 800, height = 400)
        fig.update_layout(
            xaxis_title = f'{brand} {model} Price Distribution (\N{euro sign})',
            yaxis_title = "Number of Vehicles", legend_title = 'Fuel')

        return fig
    else:
        pass


def model_pie_chart(df, brand: str, model: str, min_km, max_km, min_price,
                    max_price, min_cc, max_cc, min_hp, max_hp):
    """
    Produces pie chart for the 'search by model' page showing the population
    percentage of a car model by fuel.
    :param df: Dataframe Data
    :param brand: Brand of choice
    :param model: Car model
    :param min_km: Search option for minimum mileage
    :param max_km: Search option for maximum mileage
    :param min_price: Search option for minimum price
    :param max_price: Search option for maximum price
    :param min_cc: Search option for minimum displacement
    :param max_cc: Search option for maximum displacement
    :param min_hp: Search option for minimum horsepower
    :param max_hp: Search option for maximum horsepower
    :return: figure (histogram)
    """
    if model is not None:
        """
        Search by km, price, cc, hp. 
        """
        df = km_search(df, min_km, max_km)
        df = price_search(df, min_price, max_price)
        df = cc_search(df, min_cc, max_cc)
        df = hp_search(df, min_hp, max_hp)
        """
        Create df by quering brand and model.
        Ignoring rows where price equals 'Ask price'.
        And converting price column to int.
        """
        dummy = df.query(f'brand == "{brand}"').query(f'model == "{model}"')
        dummy = dummy.query('price != "Ask price"')
        dummy['price'] = dummy['price'].values.astype('int32')
        """
        Produce the chart.
        """
        fig = px.pie(dummy, values = dummy.groupby(['fuel', ]).size(),
                     names = dummy.groupby(['fuel', ]).size().index,
                     title = f'{brand} {model} Population Share w.r.t. Fuel',
                     width = 600, height = 500,
                     hover_data = {'Mean Price (\N{euro sign}) ': np.round(
                         dummy.groupby(['fuel'])['price'].mean())})
        fig.update_traces(textposition = 'inside', textinfo = 'percent+label')
        fig.update_layout(legend_title = "Fuel", title = {'x': 0})

        return fig
    else:
        pass


def model_bar_chart(df, brand: str, model: str, min_km, max_km, min_price,
                          max_price, min_cc, max_cc, min_hp, max_hp):
    """
    Produces bar chart for the 'search by model' page showing the population
    of a car model by fuel and transmission.
    :param df: Dataframe Data
    :param brand: Brand of choice
    :param model: Car model
    :param min_km: Search option for minimum mileage
    :param max_km: Search option for maximum mileage
    :param min_price: Search option for minimum price
    :param max_price: Search option for maximum price
    :param min_cc: Search option for minimum displacement
    :param max_cc: Search option for maximum displacement
    :param min_hp: Search option for minimum horsepower
    :param max_hp: Search option for maximum horsepower
    :return: figure (histogram)
    """
    if model is not None:
        """
        Search by km, price, cc, hp. 
        """
        df = km_search(df, min_km, max_km)
        df = price_search(df, min_price, max_price)
        df = cc_search(df, min_cc, max_cc)
        df = hp_search(df, min_hp, max_hp)
        """
        Create df by quering brand and model.
        Ignoring rows where price equals 'Ask price'.
        And converting price column to int.
        """
        dummy = df.query(f'brand == "{brand}"').query(f'model == "{model}"')
        dummy = dummy.query('price != "Ask price"')
        """
        Produce the chart.
        """
        fig = px.histogram(dummy, x = 'fuel', width = 600, height = 500,
                           title = f'{brand} {model} Population Share w.r.t. '
                                   f'Fuel/Transmission',
                           color = 'transmission', text_auto = True)
        fig.update_layout(xaxis_title = "Fuel",
                          yaxis_title = "Number of Vehicles",
                          legend_title = "Transmission Type",
                          title = {'x': 0})

        return fig
    else:
        pass
