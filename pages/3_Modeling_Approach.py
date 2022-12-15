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

Once functioning, Pycaret recommended a RandomForest regression model with the following hyperparmeter settings:
''')
rf_model = ('''rf2 = RandomForestRegressor(bootstrap=True, ccp_alpha=0.0, criterion='mse',
                      max_depth=None, max_features='auto', max_leaf_nodes=None,
                      max_samples=None, min_impurity_decrease=0.0,
                      min_impurity_split=None, min_samples_leaf=1,
                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                      n_estimators=100, n_jobs=-1, oob_score=True,
                      verbose=0, warm_start=False)''')

st.code(rf_model, language="python")

st.markdown('''
The model was then trained on an 80/20 training/testing split of all scooter data. 
''')

st.subheader('Model Outputs and GitHub LFS')
st.markdown('''

The trained Random Forest model was output using Pickle, packaged with the location dataframes that would be used for mapping. The final Pickle file was over 2.4GB in size. 

This resulted in two issues:
1. Very large files cannot be commited to GitHub via the desktop app. 

Solving this required using GitHub Large File Storage (LFS) and using Git Bash console to connect to the repo, add, commit, and push the file. (Helpful directions <a href='https://medium.com/linkit-intecs/how-to-upload-large-files-to-github-repository-2b1e03723d2'>HERE</a>)

2. GitHub free accounts have a maximum size: 2GB overall
3. GitHub free accounts have 1GB caps on LFS storage and bandwidth

Unfortunately, attempting to push the Pickle file to the GitHub repo maxed out all the limits of GitHub, causing the repo to become locked. The original Streamlit app worked, but updates could not be pushed. 

A completely new repo was setup for the project, and I went back to the drawing board for modeling.

''')
st.subheader('Final Model Selection and Future Steps')
st.markdown('''
Back in Google Colab, I opted to move forward with a simple K-Nearest Neighbors regression model in hopes of a smaller output size. Minor, manual hyperparameter tuning was performed, ultimately landing on the following model setup:
''')
knn_model = ('''knn_model = KNeighborsRegressor(n_neighbors=5, weights="distance")''')

st.code(knn_model, language="python")

st.markdown('''
Further data tweaks were made to the scooter data (grouping hours into ranges, dropping neighborhood as an input field), and the model retrained. When exporting this model, the Pickle file size was around 138MB, a significant reduction, making it feasible to host on GitHub and iterate as needed. 

It was after this, I realized that the model was produced using the downgraded version of sklearn (due to using Pycaret) and was leading to errors in Streamlit. After restarting the Colab notebook and ensuring the correct version of Sklearn, the model was run again and issues resolved. 

If revisiting this app in the future, there are additional steps I would take to improve the results:
1. The scooter data has no negative cases, pretty much ensuring the models will predict at least 1 scooter at every location. I devised a method to generate that data, but given sizing and timing limits, was not able to implement for this demo.
2. Try a trainng/test split based on years, rather than random on combined set. Hopefully 2022 data will be availble soon!
3. Spend more time on understanding input contribution to the model. 
4. Attempt a model that can predict likelihood of a particular brand of scooter will be available. 
''')