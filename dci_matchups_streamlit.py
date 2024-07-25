import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon,
            """
            <style>
            [data-testid="stElementToolbar"] {
                display: none;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

data = pd.read_csv('dci_historic.csv')
corps_list = sorted(list(set(list(data['Corps']))))
#class_list = sorted(list(set(list(data['Class']))))
st.title("DCI Historical Matchups App")
st.write("This app allows you to view historic matchup data between two corps in Drum Corps International competition. After selecting two corps in the dropdowns below, you will see information about on the last time that each corps beat each other in head to head competition at the same show.")

row_input = st.columns((1,2))
with row_input[0]:
    #class_ = st.radio('Select the class of both corps', ['World/Div 1', )
    corps1 = st.selectbox('Select Corps 1', corps_list, placeholder='', index=None)
    corps2 = st.selectbox('Select Corps 2', corps_list, placeholder='', index=None)

if (corps1 is not None and corps2 is not None):
    data = pd.read_csv('dci_historic.csv')
    filtered = data[['Year', 'Corps', 'Date', 'Show Name', 'Total Score', 'Place']]
    filter_string = 'Corps=="'+corps1+'" or Corps=="'+corps2+'"'
    filtered = filtered.query(filter_string)
    filtered = filtered[filtered.groupby(['Date', 'Show Name'])[['Date', 'Show Name']].transform('size') > 1]
    
    corps1_wins = 0
    corps2_wins = 0
    ties = 0
    
    c1_list = list(filtered['Corps'])[::2]
    c1_scores = list(filtered['Total Score'])[::2]
    
    c2_list = list(filtered['Corps'])[1::2]
    c2_scores = list(filtered['Total Score'])[1::2]

    for x in range(len(c1_list)):
        if c1_list[x] == corps1 and (c1_scores[x] > c2_scores[x]):
            corps1_wins += 1
        elif c1_list[x] == corps2 and (c1_scores[x] > c2_scores[x]):
            corps2_wins += 1
        elif c1_list[x] == corps1 and (c1_scores[x] == c2_scores[x]):
            ties += 1
        elif c1_list[x] == corps2 and (c1_scores[x] == c2_scores[x]):
            ties += 1
    
    last_20 = pd.DataFrame({'Date': list(filtered['Date'])[::2][:20],
                           'Show': list(filtered['Show Name'])[::2][:20],
                           'Winning Corps': c1_list[:20],
                           'Winning Corps Score': list(filtered['Total Score'])[::2][:20],
                           'Losing Corps': c2_list[:20],
                           'Losing Corps Score': list(filtered['Total Score'])[1::2][:20]})
    
    if (corps1 is not None and corps2 is not None):
        st.write('Number of wins by', corps1, ':', '**'+str(corps1_wins)+'**')
        st.write('Number of wins by', corps2, ':', '**'+str(corps2_wins)+'**')
        st.write('Number of ties:', '**'+str(ties)+'**')
    
    if (corps1 is not None and corps2 is not None):
        if corps1 not in c1_list:
            st.write(corps1, 'has never beaten', corps2)
        else:
            last_c1 = filtered.iloc[(c1_list.index(corps1))*2, :]
            st.write("The last win by", corps1, "was on", last_c1['Date'], "at", last_c1['Show Name']+';', 
                     corps1, "finished with a score of", str(last_c1['Total Score']), 'while', corps2, 
                     'finished with a score of', str(filtered.iloc[(c1_list.index(corps1))*2+1, :]['Total Score']))
        
        if corps2 not in c1_list:
            st.write(corps2, 'has never beaten', corps1)
        else:
            last_c2 = filtered.iloc[(c1_list.index(corps2))*2, :]
            st.write("The last win by", corps2, "was on", last_c2['Date'], "at", last_c2['Show Name']+';', 
                     corps2, "finished with a score of", str(last_c2['Total Score']), 'while', corps1, 
                     'finished with a score of', str(filtered.iloc[(c1_list.index(corps2))*2+1, :]['Total Score']))
    
        #st.dataframe(last_20, hide_index=True, width=1000, height=750)
        st.subheader("Last 20 Matchups")
        st.write(last_20.to_html(index=False, justify='left'), unsafe_allow_html=True)



# [theme]
# primaryColor="#bf2a25"
# backgroundColor="#e6e6e6"
# secondaryBackgroundColor="#ffffff"
# textColor="#11364d"

#st.dataframe(last_20, hide_index=True, width=1000, height=750)
#st.write(styled_df.to_html(), unsafe_allow_html=True)


