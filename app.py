import streamlit as st
import pandas as pd
from utils import plots, search_options, metrics, model

if __name__ == '__main__':
    df = pd.read_csv('data_new.csv', index_col = 0)

    st.title('Greek Used Car Market Stats')
    st.markdown('*This is a simple app that shows statistics about '
                'the greek used car market. The data have been extracted from '
                'Car.gr. An additional feature of this app is that you can add '
                'your car\'s data and get a recommendation '
                'of how much you should sell it.*')
    st.session_state.disabled = False

    st.sidebar.write("# Car sale price suggestion")
    st.sidebar.write('Get a sale price suggestion for your car according to '
                     'it\'s features')
    get_suggestion = st.sidebar.checkbox('Sale Price Suggestion')

    st.sidebar.write('# Search Options')

    st.sidebar.write('View Stats by')
    by_brand = st.sidebar.checkbox('Brand')
    by_model = st.sidebar.checkbox('Model')

    checkboxes = [get_suggestion, by_brand, by_model]
    if by_brand and not by_model and not get_suggestion:
        with st.sidebar.container():
            st.header('Simple Search')
            brand = st.sidebar.selectbox('Choose brand',
                                         [None] + list(df['brand'].unique()))
        with st.sidebar.container():
            st.header('Extensive Search')
            side_col1, side_col2 = st.sidebar.columns(2)
            min_km = side_col1.number_input('Add minimum mileage', step = 1)
            min_price = side_col1.number_input('Add minimum price', step = 1)
            min_cc = side_col1.number_input('Add minimum cc', step = 1)
            min_hp = side_col1.number_input('Add minimum hp', step = 1)

            max_km = side_col2.number_input('Add maximum mileage', step = 1)
            max_price = side_col2.number_input('Add maximum price', step = 1)
            max_cc = side_col2.number_input('Add maximum cc', step = 1)
            max_hp = side_col2.number_input('Add maximum hp', step = 1)

        st.write(f'- ### {brand}')
        st.write(search_options.km_tag(min_km, max_km), '|',
                 search_options.price_tag(min_price, max_price), '|',
                 search_options.displacement_tag(min_cc, max_cc), '|',
                 search_options.hp_tag(min_hp, max_hp))

        col1, col2 = st.columns([2.5, 1])
        if brand is not None:
            col2.write(metrics.brand_metrics(df, brand))
        try:
            fig = plots.brand_bar_chart(df, brand, min_km, max_km, min_price,
                                        max_price, min_cc, max_cc, min_hp,
                                        max_hp)
            col1.plotly_chart(fig, use_container_width = True)
        except:
            pass

        try:
            fig = plots.brand_pie_chart(df, brand, min_km, max_km, min_price,
                                        max_price, min_cc, max_cc, min_hp,
                                        max_hp)
            col1.plotly_chart(fig, use_container_width = True)
        except:
            pass

    elif by_model and not by_brand and not get_suggestion:
        with st.sidebar.container():
            st.header('Simple Search')
            brand = st.sidebar.selectbox('Choose brand',
                                         [None] + list(df['brand'].unique()))
            models = df.query(f'brand == "{brand}"')['model'].unique()
            model = st.sidebar.selectbox('Choose model', [None] + list(models))

        with st.sidebar.container():
            st.header('Extensive Search')
            side_col1, side_col2 = st.sidebar.columns(2)
            min_km = side_col1.number_input('Add minimum mileage', step = 1)
            min_price = side_col1.number_input('Add minimum price', step = 1)
            min_cc = side_col1.number_input('Add minimum cc', step = 1)
            min_hp = side_col1.number_input('Add minimum hp', step = 1)

            max_km = side_col2.number_input('Add maximum mileage', step = 1)
            max_price = side_col2.number_input('Add maximum price', step = 1)
            max_cc = side_col2.number_input('Add maximum cc', step = 1)
            max_hp = side_col2.number_input('Add maximum hp', step = 1)

        st.write(f'- ### {brand} {model}')
        st.write(search_options.km_tag(min_km, max_km), '|',
                 search_options.price_tag(min_price, max_price), '|',
                 search_options.displacement_tag(min_cc, max_cc), '|',
                 search_options.hp_tag(min_hp, max_hp))
        col1, col2 = st.columns([2.5, 1])
        # col2.write(metrics.brand_metrics(df, brand))
        try:
            fig1 = plots.model_histogram_chart(df, brand, model, min_km, max_km,
                                               min_price, max_price, min_cc,
                                               max_cc, min_hp, max_hp)
            col1.plotly_chart(fig1, use_container_width = True)
        except:
            pass

        try:
            fig2 = plots.model_pie_chart(df, brand, model, min_km, max_km,
                                         min_price, max_price, min_cc, max_cc,
                                         min_hp, max_hp)
            col1.plotly_chart(fig2, use_container_width = True)
        except:
            pass

        try:
            fig3 = plots.model_bar_chart(df, brand, model, min_km, max_km,
                                         min_price, max_price, min_cc,
                                         max_cc, min_hp, max_hp)
            col1.plotly_chart(fig3, use_container_width = True)
        except:
            pass

    elif get_suggestion and not by_brand and not by_model:
        st.write('#### Add your car\'s features to get a sale price '
                 'suggestion.')
        col1, col2 = st.columns([1, 1])
        s_brand = col1.selectbox('Choose brand',
                                     [None] + list(df['brand'].unique()))
        s_year = col1.selectbox('Year', range(1900, 2023))
        s_cc = col1.number_input('Engine Displacement (cc)', step = 1)
        s_fuel = col1.selectbox('Fuel Type', df['fuel'].unique())

        models = df.query(f'brand == "{s_brand}"')['model'].unique()
        s_model = col2.selectbox('Choose model', [None] + list(models))
        s_mileage = col2.number_input('Mileage (km)', step = 1)
        s_hp = col2.number_input('Engine Power (hp)', step = 1)
        s_transmission = col2.selectbox('Transmission',
                                        df['transmission'].unique())

        tooltip_text = "The suggestion you get is a rough estimate of the " \
                       "cars market worth, bacause the data used might " \
                       "not be enough."
        suggestion = col1.button('Proceed', help = tooltip_text)
        if suggestion:
            prediction = model.get_prediction(df, s_brand, s_model,
                                                   s_year, s_mileage,
                                                   s_cc, s_hp, s_fuel,
                                                   s_transmission)

            col1.write(f'### Car sale price suggestion for {s_brand} {s_model}:'
                       f' {prediction.astype("int32")} \N{euro sign}')
    elif sum(checkboxes) >= 2:
        st.write(f'#### Please have only one box checked at a time to get a '
                 f'result!')
