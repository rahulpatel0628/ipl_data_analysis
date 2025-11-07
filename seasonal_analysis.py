import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

class Seasonal_Analysys:

    def __init__(self,data1,data2):
        self.data1=data1
        self.data2=data2
    def seasonal_analysis(self):
        st.header("Seasonal Analysis")
        
        season=self.data1['Season'].unique()
        selected_season=st.selectbox("Select Season",season)

        selected_data=self.data1[self.data1['Season']==selected_season]

        col1,col2=st.columns(2)

        with col1:
            winner=selected_data[selected_data['MatchNumber']=='Final']['WinningTeam'].to_list()[0]
            st.metric("Champion Team:",winner)
        with col2:
            Final_data=selected_data[selected_data['MatchNumber']=='Final']
            if (Final_data['Team1']==winner).to_list()[0]:
                runner_up=Final_data['Team2'].to_list()[0]
            else:
                runner_up=Final_data['Team1'].to_list()[0]
            st.metric("Runner Up:",runner_up)

        #Find top batsman
        new_data=pd.merge(self.data2,selected_data)
        top_10=new_data.groupby('batter').agg({'batsman_run':'sum'}).reset_index().sort_values(ascending=False,by='batsman_run').head(10)
        st.subheader(f"Top 10 Run Scorer in {selected_season}")
        fig=px.bar(top_10,x='batter',y='batsman_run',title=f'top 10 run scorer in {selected_season}')
        st.plotly_chart(fig)
        
        six=new_data[new_data['batsman_run']==6]
        top_10_six=six.groupby('batter').agg({'batsman_run':'count'}).reset_index().sort_values(ascending=False,by='batsman_run').head(10)
        fig=px.bar(top_10_six,x='batter',y='batsman_run',title=f'top 10 six hitter in {selected_season}')
        st.plotly_chart(fig)

        Four=new_data[new_data['batsman_run']==4]
        top_10_four=Four.groupby('batter').agg({'batsman_run':'count'}).reset_index().sort_values(ascending=False,by='batsman_run').head(10)
        fig=px.bar(top_10_four,x='batter',y='batsman_run',title=f'top 10 four hitter in {selected_season}')
        st.plotly_chart(fig)
        
        #Tot 10 wicket tacker
        wicket=new_data[new_data['isWicketDelivery']==1]
        top_10_wicket=wicket.groupby('bowler').agg({'isWicketDelivery':'count'}).reset_index().sort_values(ascending=False,by='isWicketDelivery').head(10)
        fig=px.bar(top_10_wicket,x='bowler',y='isWicketDelivery',title=f'top 10 wicket tacker in {selected_season}')
        st.plotly_chart(fig)
        # champion_df = pd.DataFrame(champions)
        
        # st.subheader("Season Overview")
        # st.dataframe(season_stats)
        
        # if not champion_df.empty:
        #     st.subheader("Season Champions")
        #     st.dataframe(champion_df)
            
            
        #     fig = px.bar(champion_df, x='Season', y='Wins', color='Champion',
        #                 title='Champion Teams by Season')
        #     st.plotly_chart(fig)
    