import streamlit as st

with st.sidebar:
    st.image('scooter.jpg')

st.title("Scooter Buddy: Modeling Approach")
st.markdown("""---""")

st.header("Data Cleansing")
st.subheader("Scooter Data")
st.markdown('''
The scooter data was transformed in the following ways to support the modeling: 
1. The 2019, 2020 and 2021 datasets were combined into a single data frame. Columns were the same except for the primary ID column.
2. Date transformations were performed to break down the PollDate in to component fields (Year, Month, Hour, Day of Week, Day of Year).
3. Scooter data for "trail" centerlines was dropped since they were not in the MPLS data.
4. Numeric hours were converted into text ranges. This was done because poll times were not consistent across the years
5. Duplicate records were created due to time bucketing and were dropped. 
6. Brand field was converted to one-hot-encoding. Hour ranges were changed to ordinalEncoding. All numeric fields were optimized and uneeded fields dropped. 
''')
st.header('Model Selection')
st.subheader('Pycaret')
st.markdown('''
As a starting point, Pycaret was brough to bear in an attempt to simplify the model selection process, optimized for RMSE. 

Initial setup of Pycaret within the Google Colab notebook was not clean, as Sklearn needed to be downgraded to a lower version for Pycaret to function. This would create later conflicts with sklearn versions in Streamlit.

Once functioning, Pycaret recommended a RandomForest regression model with the following settings:
''')
rf_model = ('''rf2 = RandomForestRegressor(bootstrap=True, ccp_alpha=0.0, criterion='mse',
                      max_depth=None, max_features='auto', max_leaf_nodes=None,
                      max_samples=None, min_impurity_decrease=0.0,
                      min_impurity_split=None, min_samples_leaf=1,
                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                      n_estimators=100, n_jobs=-1, oob_score=True,
                      verbose=0, warm_start=False)''')

st.code(rf_model, language="python")

st.subheader('Model Outputs and GitHub LFS')
st.markdown('''
The scooter data was transformed in the following ways to support the modeling: 
1. The 2019, 2020 and 2021 datasets were combined into a single data frame. Columns were the same except for the primary ID column.
2. Date transformations were performed to break down the PollDate in to component fields (Year, Month, Hour, Day of Week, Day of Year).
3. Scooter data for "trail" centerlines was dropped since they were not in the MPLS data.
4. Numeric hours were converted into text ranges. This was done because poll times were not consistent across the years
5. Duplicate records were created due to time bucketing and were dropped. 
6. Brand field was converted to one-hot-encoding. Hour ranges were changed to ordinalEncoding. All numeric fields were optimized and uneeded fields dropped. 
''')
st.subheader('Final Model Selection and Future Steps')
st.markdown('''
The scooter data was transformed in the following ways to support the modeling: 
1. The 2019, 2020 and 2021 datasets were combined into a single data frame. Columns were the same except for the primary ID column.
2. Date transformations were performed to break down the PollDate in to component fields (Year, Month, Hour, Day of Week, Day of Year).
3. Scooter data for "trail" centerlines was dropped since they were not in the MPLS data.
4. Numeric hours were converted into text ranges. This was done because poll times were not consistent across the years
5. Duplicate records were created due to time bucketing and were dropped. 
6. Brand field was converted to one-hot-encoding. Hour ranges were changed to ordinalEncoding. All numeric fields were optimized and uneeded fields dropped. 
''')
