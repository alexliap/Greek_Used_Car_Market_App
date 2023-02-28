import pandas as pd


def km_search(df: pd.DataFrame, min_km = 0, max_km = 0):
    if max_km != 0:
        return df.query(f'km >= {min_km} & km <= {max_km}')
    else:
        return df.query(f'km >= {min_km}')


def price_search(df: pd.DataFrame, min_price = 0, max_price = 0):
    df = df.query('price != "Ask price"')
    df['price'] = df['price'].values.astype('int32')
    if max_price != 0:
        return df.query(f'price >= {min_price} & price <= {max_price}')
    else:
        return df.query(f'price >= {min_price}')


def cc_search(df: pd.DataFrame, min_cc = 0, max_cc = 0):
    if max_cc != 0:
        return df.query(f'displacement >= {min_cc} & displacement <= {max_cc}')
    else:
        return df.query(f'displacement >= {min_cc}')


def hp_search(df: pd.DataFrame, min_hp = 0, max_hp = 0):
    if max_hp != 0:
        return df.query(f'hp >= {min_hp} & hp <= {max_hp}')
    else:
        return df.query(f'hp >= {min_hp}')


def km_tag(min_km, max_km):
    if min_km != 0 and max_km != 0:
        return f'Mileage: {min_km} - {max_km}'
    elif min_km != 0 and max_km == 0:
        return f'Mileage: from {min_km}'
    elif min_km == 0 and max_km != 0:
        return f'Mileage: to {max_km}'


def price_tag(min_price, max_price):
    if min_price != 0 and max_price != 0:
        return f'Price: {max_price} - {max_price}'
    elif min_price != 0 and max_price == 0:
        return f'Price: from {max_price}'
    elif min_price == 0 and max_price != 0:
        return f'Price: to {max_price}'


def displacement_tag(min_cc, max_cc):
    if min_cc != 0 and max_cc != 0:
        return f'Displacement: {max_cc} - {max_cc}'
    elif min_cc != 0 and max_cc == 0:
        return f'Displacement: from {max_cc}'
    elif min_cc == 0 and max_cc != 0:
        return f'Displacement: to {max_cc}'

def hp_tag(min_hp, max_hp):
    if min_hp != 0 and max_hp != 0:
        return f'Horse Power: {max_hp} - {max_hp}'
    elif min_hp != 0 and max_hp == 0:
        return f'Horse Power: from {max_hp}'
    elif min_hp == 0 and max_hp != 0:
        return f'Horse Power: to {max_hp}'
