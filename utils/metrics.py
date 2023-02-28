import pandas as pd
import numpy as np


def brand_metrics(df: pd.DataFrame, brand: str):
    dummy = df.query(f'brand == "{brand}"')
    pop = f'Number of used {brand} cars: {len(dummy)}'
    dummy = dummy.query('price != "Ask price"')
    dummy['price'] = dummy['price'].values.astype('int32')
    mean_price = f'Mean Price for a used {brand} car: ' \
                 f'{np.round(dummy["price"].mean()).astype("int32")}'
    max_price = f'Max Price for a used {brand} car: {dummy["price"].max()}'
    min_price = f'Min Price for a used {brand} car: {dummy["price"].min()}'

    return '\n \n'.join([pop, mean_price, max_price, min_price])
