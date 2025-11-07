import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
class Team_Dashboard:
    def __init__(self,data1,data2):
        self.data1=data1
        self.data2=data2
    def team_dashboard(self):
        st.header("Team Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        
        team1_matches = self.data1['Team1'].value_counts()
        team2_matches = self.data1['Team2'].value_counts()
        total_matches = team1_matches.add(team2_matches, fill_value=0)
        
       
        wins = self.data1[self.data1['WinningTeam'] != 'No Result']['WinningTeam'].value_counts()
        
      
        win_percentage = (wins / total_matches * 100).round(2)
        
        with col1:
            st.metric("Total Teams", len(total_matches))
        with col2:
            st.metric("Total Matches", len(self.data1))
        with col3:
            st.metric("Most Successful Team", wins.index[0] if len(wins) > 0 else "N/A")
        with col4:
            st.metric("Highest Win %", f"{win_percentage.max()}%" if len(win_percentage) > 0 else "N/A")
        
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        
        wins_df = wins.reset_index()
        wins_df.columns = ['Team', 'Wins']
        ax1.bar(wins_df['Team'], wins_df['Wins'])
        ax1.set_title('Total Wins by Team')
        ax1.tick_params(axis='x', rotation=45)
        
        
        win_pct_df = win_percentage.reset_index()
        win_pct_df.columns = ['Team', 'WinPercentage']
        ax2.bar(win_pct_df['Team'], win_pct_df['WinPercentage'])
        ax2.set_title('Win Percentage by Team')
        ax2.tick_params(axis='x', rotation=45)
        
        st.pyplot(fig)
        
        
        st.subheader("Detailed Team Statistics")
        team_stats = pd.DataFrame({
            'Total Matches': total_matches,
            'Wins': wins,
            'Win Percentage': win_percentage
        }).fillna(0).sort_values('Wins', ascending=False)
        
        st.dataframe(team_stats.style.background_gradient(cmap='Blues'))