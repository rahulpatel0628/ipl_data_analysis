import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
class Player_OF_MATCH:

    def __init__(self,data1,data2):
        self.data1=data1
        self.data2=data2
    def player_of_match(self):
        st.header("Player of the Match Analysis")
        
        
        potm_counts = self.data1['Player_of_Match'].value_counts().head(15)
        
        fig = px.bar(potm_counts, x=potm_counts.index, y=potm_counts.values,
                     title='Top 15 Player of the Match Award Winners')
        st.plotly_chart(fig)
        
        
        potm_team = self.data1.groupby(['WinningTeam', 'Player_of_Match']).size().reset_index(name='Count')
        top_potm_team = potm_team.groupby('WinningTeam').apply(
            lambda x: x.nlargest(1, 'Count')
        ).reset_index(drop=True)
        
        st.subheader("Top Player of the Match by Team")
        st.dataframe(top_potm_team)
