import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class Toss_Impact:

    def __init__(self,data1,data2):
        self.data1=data1
        self.data2=data2
    def toss_impact(self):

        st.header("Toss Impact Analysis")
        completed_matches = self.data1[self.data1['WinningTeam'] != 'No Result'].copy()
        
        
        completed_matches['TossWinMatchWin'] = completed_matches['TossWinner'] == completed_matches['WinningTeam']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            toss_win_rate = (completed_matches['TossWinMatchWin'].sum() / len(completed_matches) * 100).round(2)
            st.metric("Toss Win to Match Win %", f"{toss_win_rate}%")
        
        with col2:
            bat_first_wins = len(completed_matches[
                (completed_matches['TossDecision'] == 'bat') & 
                (completed_matches['TossWinMatchWin'] == True)
            ])
            st.metric("Bat First Wins", bat_first_wins)
        
        with col3:
            field_first_wins = len(completed_matches[
                (completed_matches['TossDecision'] == 'field') & 
                (completed_matches['TossWinMatchWin'] == True)
            ])
            st.metric("Field First Wins", field_first_wins)
        
       
        st.subheader("Toss Decision Impact")
        
        decision_analysis = completed_matches.groupby('TossDecision').agg({
            'TossWinMatchWin': ['count', 'sum']
        })
        decision_analysis.columns = ['Total Matches', 'Wins']
        decision_analysis['Win Percentage'] = (decision_analysis['Wins'] / decision_analysis['Total Matches'] * 100).round(2)
        
        st.dataframe(decision_analysis)
        
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
       
        completed_matches['TossDecision'].value_counts().plot(kind='pie', ax=ax1, autopct='%1.1f%%')
        ax1.set_title('Toss Decision Distribution')
        
       
        decision_analysis['Win Percentage'].plot(kind='bar', ax=ax2)
        ax2.set_title('Win Percentage by Toss Decision')
        ax2.set_ylabel('Win Percentage (%)')
        
        st.pyplot(fig)