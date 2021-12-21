import json
import streamlit as st
import numpy as np
import pandas as pd
import time

with st.expander("Choose the file"):
        json_data = st.file_uploader("Choose a file",type='json')
        if json_data is not None:
            raw_data = json_data.getvalue()
            data = json.loads(raw_data)
            source = data['Server']
            source_symbols = source[16]['ConfigSymbols']
            i = 0
            
            symbol_list = len(source[16]['ConfigSymbols'])
            symbol = []
            data_dict = {'symbol': [], 'description': [],
                            'currencybase': [], 'currencyprofit': []}
            while i < int(symbol_list):
                    source1 = source[16]['ConfigSymbols'][i]['Symbol']
                    source2 = source[16]['ConfigSymbols'][i]['Description']
                    source3 = source[16]['ConfigSymbols'][i]['CurrencyBase']
                    source4 = source[16]['ConfigSymbols'][i]['CurrencyProfit']
                    symbol.append(source1)
                    data_dict['description'].append(source2)
                    data_dict['currencybase'].append(source3)
                    data_dict['currencyprofit'].append(source4)
                    i += 1
def main():
    if json_data != None:
        st.title("Metatrader symbols")
        options = st.selectbox("Select the Symbol", symbol)
        counts = symbol.index(options)
        # st.write(counts)
        # st.write(symbol_list)
        col1, col2 = st.columns(2)
        with col1:
            selected_data={'Symbol':options,"Description":data_dict['description'][counts],"CurrencyBase":data_dict['currencybase'][counts],"CurrencyProfit":data_dict['currencyprofit'][counts]}
            st.subheader("Details")
            st.write('**Symbol :**', options)
            st.write('**Description :**  ', data_dict['description'][counts])
            st.write('**CurrencyBase :**  ', data_dict['currencybase'][counts])
            st.write('**CurrencyProfit :** ', data_dict['currencyprofit'][counts])
        with col2:
            with st.expander("Edit"):
                symbol_change = st.text_input('Symbol :', options, key=1)
                description = st.text_input(
                    'Description :  ', data_dict['description'][counts], key=2)
                currencybase = st.text_input(
                    'CurrencyBase :  ', data_dict['currencybase'][counts], key=3)
                currencyprofit = st.text_input(
                    'CurrencyProfit : ', data_dict['currencyprofit'][counts], key=4)
                if st.button("APPLY CHANGES"):


                    with st.spinner(text='Updating..'):
                        source[16]['ConfigSymbols'][counts]['Symbol'] = symbol_change
                        source[16]['ConfigSymbols'][counts]['Description'] = description
                        source[16]['ConfigSymbols'][counts]['CurrencyBase'] = currencybase
                        source[16]['ConfigSymbols'][counts]['CurrencyProfit'] = currencyprofit
                        f = open('webapp1.json', 'w', encoding='utf-8')
                        json.dump(data, f)
                        f.close()
                    st.success("Changes done 👍")
                    time.sleep(0.5)
                    st.experimental_rerun()
            with st.expander("Add new symbol"):
                    symbol_new = st.text_input('Symbol :',key=5)
                    description_new = st.text_input(
                    'Description :  ',key=6)
                    currencybase_new = st.text_input(
                    'CurrencyBase :  ', key=7)
                    currencyprofit_new = st.text_input(
                    'CurrencyProfit : ',  key=8)
                    if st.button('ADD'):
                        add_dict={"Symbol":symbol_new, "Description":description_new,"CurrencyBase":currencybase_new,"CurrencyProfit":currencyprofit_new}
                        source[16]['ConfigSymbols'].append(add_dict)
                        json_file=open('webapp1.json', 'w') 
                        json.dump(data, json_file, 
                            indent=4,  
                            separators=(',',': '))
                        json_file.close()
                        st.success("Changes done 👍")
                        time.sleep(0.5)
                        st.experimental_rerun()
            with st.expander("Delete the Selected Symbol"):
                #st.subheader()
                st.write('**Symbol :**', options)
                st.write('**Description :**  ', data_dict['description'][counts])
                st.write('**CurrencyBase :**  ', data_dict['currencybase'][counts])
                st.write('**CurrencyProfit :** ', data_dict['currencyprofit'][counts])
                if st.button("Delete",key=3):
                    for i in range(symbol_list):
                        if source_symbols[i]['Symbol'] == selected_data['Symbol']:
                            source_symbols.pop(i)
                            break
                    json_file1=open('webapp1.json', 'w') 
                    json.dump(data, json_file1, 
                                indent=4,  
                                separators=(',',': '))
                    json_file1.close()
                    st.success("Changes done 👍")
                    time.sleep(0.5)
                    st.experimental_rerun()

        st.header("Compare symbols")
        with st.expander("Compare"):
            multisymbols = st.multiselect(
                "Select any TWO or THREE symbols", symbol)
            # st.write(len(multisymbols))
            no_of_symbols = len(multisymbols)

            column1, column2, column3 = st.columns(3)
            if no_of_symbols > 3:
                st.warning("⚠ Select only two or three options")
            else:
                for i in range(no_of_symbols):
                    column = f'column{i+1}'
                    columns_i = eval(column)
                    with columns_i:
                        st.subheader(multisymbols[i])
                        index_option = symbol.index(multisymbols[i])
                        st.write('**Symbol :**', multisymbols[i])
                        st.write('**Description :**  ',
                                data_dict['description'][index_option])
                        st.write('**CurrencyBase :**  ',
                                data_dict['currencybase'][index_option])
                        st.write('**CurrencyProfit :** ',
                                data_dict['currencyprofit'][index_option])
        with st.expander("Data in json file"):
            st.write("Description")
            st.write(data_dict['description'])


        hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                border-top:5px
                </style>
                """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
