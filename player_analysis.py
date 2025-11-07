import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class Player_Analysis:
    def __init__(self,data1,data2):
        self.data1=data1
        self.data2=data2

    def player_analysis(self):
        
        st.header("Player Analysis")
        
        
        players = self.data2['batter'].unique()
        selected_player = st.selectbox("Select Player", players)
        
        if selected_player:
            player_data = self.data2[self.data2['batter'] == selected_player]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_runs = player_data['batsman_run'].sum()
                st.metric("Total Runs", total_runs)
            
            with col2:
                total_matches = player_data['ID'].nunique()
                st.metric("Matches Played", total_matches)
            
            with col3:
                total_sixes = len(player_data[player_data['batsman_run'] == 6])
                st.metric("Total Sixes", total_sixes)
            
            with col4:
                total_fours = len(player_data[player_data['batsman_run'] == 4])
                st.metric("Total Fours", total_fours)
            col5,col6=st.columns(2)

            new_data=player_data.groupby('ID').agg({'batsman_run':['sum']}).reset_index()
            new_data.columns=['ID','Runs']
            with col5:
                st.metric('Total 50:',len(new_data[new_data['Runs']>=50]))
            with col6:
                st.metric('Total 100:',len(new_data[new_data['Runs']>=100]))
            st.subheader(f"Performance against Different Teams")
            
            player_data=pd.merge(player_data,self.data1)
            player_data=player_data.groupby(['BowlingTeam']).sum('batsman_run')
            player_data=player_data['batsman_run']
            player_data=player_data.reset_index()
            player_data.columns=['Team','Total Runs']
            
            st.dataframe(player_data)
            
            
            # st.subheader("Runs Distribution per Match")
            # if not performance_df.empty:
            #     fig = px.histogram(performance_df, x='Runs', nbins=20, 
            #                      title=f"Runs Distribution for {selected_player}")
            #     st.plotly_chart(fig)