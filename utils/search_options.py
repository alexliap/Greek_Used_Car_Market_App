import pandas as pd


def km_search(df: pd.DataFrame, min_km = 0, max_km = 0):
    """
    A dataframe slicing is performed by restricting the km column
    :param df: Dataframe data
    :param min_km: Search option for minimum mileage
    :param max_km: Search option for maximum mileage
    :return: dataframe
    """
    if max_km != 0:
        return df.query(f'km >= {min_km} & km <= {max_km}')
    else:
        return df.query(f'km >= {min_km}')


def price_search(df: pd.DataFrame, min_price = 0, max_price = 0):
    """
    A dataframe slicing is performed by restricting the price column
    :param df: Dataframe data
    :param min_price: Search option for minimum price
    :param max_price: Search option for maximum price
    :return: dataframe
    """
    df = df.query('price != "Ask price"')
    df['price'] = df['price'].values.astype('int32')
    if max_price != 0:
        return df.query(f'price >= {min_price} & price <= {max_price}')
    else:
        return df.query(f'price >= {min_price}')


def cc_search(df: pd.DataFrame, min_cc = 0, max_cc = 0):
    """
    A dataframe slicing is performed by restricting the cc column
    :param df: Dataframe data
    :param min_cc: Search option for minimum displacement
    :param max_cc: Search option for maximum displacement
    :return: dataframe
    """
    if max_cc != 0:
        return df.query(f'displacement >= {min_cc} & displacement <= {max_cc}')
    else:
        return df.query(f'displacement >= {min_cc}')


def hp_search(df: pd.DataFrame, min_hp = 0, max_hp = 0):
    """
    A dataframe slicing is performed by restricting the cc column
    :param df: Dataframe data
    :param min_hp: Search option for minimum hp
    :param max_hp: Search option for maximum hp
    :return: dataframe
    """
    if max_hp != 0:
        return df.query(f'hp >= {min_hp} & hp <= {max_hp}')
    else:
        return df.query(f'hp >= {min_hp}')


def km_tag(min_km, max_km):
    """
    A string which shows the restriction that is being applied on search
    :param min_km: Search option for minimum mileage
    :param max_km: Search option for maximum mileage
    :return: search tag (string)
    """
    if min_km != 0 and max_km != 0:
        return f'Mileage: {min_km} - {max_km} km'
    elif min_km != 0 and max_km == 0:
        return f'Mileage: from {min_km} km'
    elif min_km == 0 and max_km != 0:
        return f'Mileage: to {max_km} km'


def price_tag(min_price, max_price):
    """
    A string which shows the restriction that is being applied on search
    :param min_price: Search option for minimum price
    :param max_price: Search option for maximum price
    :return: search tag (string)
    """
    if min_price != 0 and max_price != 0:
        return f'Price: {min_price} - {max_price} \N{euro sign}'
    elif min_price != 0 and max_price == 0:
        return f'Price: from {min_price} \N{euro sign}'
    elif min_price == 0 and max_price != 0:
        return f'Price: to {max_price} \N{euro sign}'


def displacement_tag(min_cc, max_cc):
    """
    A string which shows the restriction that is being applied on search
    :param min_cc: Search option for minimum displacement
    :param max_cc: Search option for maximum displacement
    :return: search tag (string)
    """
    if min_cc != 0 and max_cc != 0:
        return f'Displacement: {min_cc} - {max_cc} cc'
    elif min_cc != 0 and max_cc == 0:
        return f'Displacement: from {min_cc} cc'
    elif min_cc == 0 and max_cc != 0:
        return f'Displacement: to {max_cc} cc'


def hp_tag(min_hp, max_hp):
    """
    A string which shows the restriction that is being applied on search
    :param min_hp: Search option for minimum horsepower
    :param max_hp: Search option for maximum horsepower
    :return: search tag (string)
    """
    if min_hp != 0 and max_hp != 0:
        return f'Horse Power: {min_hp} - {max_hp} hp'
    elif min_hp != 0 and max_hp == 0:
        return f'Horse Power: from {min_hp} hp'
    elif min_hp == 0 and max_hp != 0:
        return f'Horse Power: to {max_hp} hp'
