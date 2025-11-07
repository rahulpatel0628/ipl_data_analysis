import streamlit as st
import pandas as pd
import numpy as np
from team_dashboard import Team_Dashboard 
from player_analysis import Player_Analysis
from toss_impact import Toss_Impact
from venue_analysis import Venue_Analysis
from seasonal_analysis import Seasonal_Analysys
from player_of_match_analysis import Player_OF_MATCH
from winning_prediction import WinningPrediction
st.set_page_config(
    page_title="IPL Data Analysis",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🏏 IPL Cricket Data Analysis")
    st.markdown('<div class="main-header">Comprehensive IPL Tournament Analysis</div>', unsafe_allow_html=True)
    
    
    data1=pd.read_csv("match.csv")
    data2=pd.read_csv("ball_by_ball_run.csv")
    
   
    st.sidebar.title("Navigation")
    analysis_type = st.sidebar.selectbox(
                "Select Analysis Type",
                [
                    "Team Dashboard",
                    "Player Analysis", 
                    "Toss Impact Analysis",
                    "Venue Analysis",
                    "Seasonal Analysis",
                    "Player of Match Analysis",
                    "Winning Prediction"
                ]
            )
    if analysis_type == "Team Dashboard":
                TD=Team_Dashboard(data1,data2)
                TD.team_dashboard()
    elif analysis_type == "Player Analysis":
                PA=Player_Analysis(data1,data2)
                PA.player_analysis()
    elif analysis_type == "Toss Impact Analysis":
                TI=Toss_Impact(data1,data2)
                TI.toss_impact()
    elif analysis_type == "Venue Analysis":
                VA=Venue_Analysis(data1,data2)
                VA.venue_analysis()
    elif analysis_type == "Seasonal Analysis":
                SA=Seasonal_Analysys(data1,data2)
                SA.seasonal_analysis()
    elif analysis_type == "Player of Match Analysis":
                POM=Player_OF_MATCH(data1,data2)
                POM.player_of_match()
    elif analysis_type == "Winning Prediction":
                WP=WinningPrediction(data1,data2)
                WP.winning_prediction()
            
    with st.expander("View Raw Data"):
                st.dataframe(data1.head(100))
                st.dataframe(data2.head(100))
                
        
if __name__ == "__main__":
    main()