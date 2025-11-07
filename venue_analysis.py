import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

class Venue_Analysis:

    def __init__(self,data1,data2):
        self.data1=data1
        self.data2=data2
    def venue_analysis(self):
        st.header("Venue Analysis")
        
        
        venue_stats = self.data1.groupby('Venue').agg({
            'ID': 'count',
            'WinningTeam': lambda x: (x != 'No Result').sum()
        }).rename(columns={'ID': 'Total Matches', 'WinningTeam': 'Completed Matches'})
        
        
        venue_wins = self.data1[self.data1['WinningTeam'] != 'No Result']
        venue_team_wins = venue_wins.groupby(['Venue', 'WinningTeam']).size().reset_index(name='Wins')
        
        st.subheader("Venue Statistics")
        st.dataframe(venue_stats.sort_values('Total Matches', ascending=False))
        
        
        top_venues = venue_stats.nlargest(10, 'Total Matches').index
        top_venue_data = venue_stats.loc[top_venues]
        
        fig = px.bar(top_venue_data, x=top_venue_data.index, y='Total Matches',
                     title='Top 10 Venues by Number of Matches')
        st.plotly_chart(fig)