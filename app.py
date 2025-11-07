import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')



st.set_page_config(
    page_title="IPL Data Analysis",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)



class IPLAnalysis:
    def __init__(self, data):
        self.data = data()
        self.match_data = self.data.copy()
    
    def team_dashboard(self):
        
        st.header("🏏 Team Dashboard")
        
        
        col1, col2, col3, col4 = st.columns(4)
        
        
        team1_matches = self.match_data['Team1'].value_counts()
        team2_matches = self.match_data['Team2'].value_counts()
        total_matches = team1_matches.add(team2_matches, fill_value=0)
        
       
        wins = self.match_data[self.match_data['WinningTeam'] != 'No Result']['WinningTeam'].value_counts()
        
      
        win_percentage = (wins / total_matches * 100).round(2)
        
        with col1:
            st.metric("Total Teams", len(total_matches))
        with col2:
            st.metric("Total Matches", len(self.match_data))
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
    
    def player_analysis(self):
        """Comprehensive player analysis"""
        st.header("👤 Player Analysis")
        
        
        players = self.data['batter'].unique()
        selected_player = st.selectbox("Select Player", players)
        
        if selected_player:
            player_data = self.data[self.data['batter'] == selected_player]
            
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
            
            
            st.subheader(f"Performance against Different Teams")
            
         
            player_performance = []
            for match_id in player_data['ID'].unique():
                match = player_data[player_data['ID'] == match_id].iloc[0]
                batter_team = match['batter']
                team1 = match['Team1']
                team2 = match['Team2']
                opposition = team2 if batter_team == team1 else team1
                
                runs_in_match = player_data[player_data['ID'] == match_id]['batsman_run'].sum()
                player_performance.append({
                    'Opposition': opposition,
                    'Runs': runs_in_match
                })
            
            performance_df = pd.DataFrame(player_performance)
            if not performance_df.empty:
                team_performance = performance_df.groupby('Opposition').agg({
                    'Runs': ['sum', 'mean', 'count']
                }).round(2)
                team_performance.columns = ['Total Runs', 'Average', 'Matches']
                st.dataframe(team_performance.sort_values('Total Runs', ascending=False))
            
            
            st.subheader("Runs Distribution per Match")
            if not performance_df.empty:
                fig = px.histogram(performance_df, x='Runs', nbins=20, 
                                 title=f"Runs Distribution for {selected_player}")
                st.plotly_chart(fig)
    
    def toss_analysis(self):
        """Toss impact analysis"""
        st.header("🎯 Toss Impact Analysis")
        
        
        completed_matches = self.match_data[self.match_data['WinningTeam'] != 'No Result'].copy()
        
        
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
    
    def venue_analysis(self):
        """Venue performance analysis"""
        st.header("🏟️ Venue Analysis")
        
        
        venue_stats = self.match_data.groupby('Venue').agg({
            'ID': 'count',
            'WinningTeam': lambda x: (x != 'No Result').sum()
        }).rename(columns={'ID': 'Total Matches', 'WinningTeam': 'Completed Matches'})
        
        
        venue_wins = self.match_data[self.match_data['WinningTeam'] != 'No Result']
        venue_team_wins = venue_wins.groupby(['Venue', 'WinningTeam']).size().reset_index(name='Wins')
        
        st.subheader("Venue Statistics")
        st.dataframe(venue_stats.sort_values('Total Matches', ascending=False))
        
        
        top_venues = venue_stats.nlargest(10, 'Total Matches').index
        top_venue_data = venue_stats.loc[top_venues]
        
        fig = px.bar(top_venue_data, x=top_venue_data.index, y='Total Matches',
                     title='Top 10 Venues by Number of Matches')
        st.plotly_chart(fig)
    
    def winning_prediction(self):
        """Match winning prediction model"""
        st.header("🔮 Winning Prediction")
        
       
        prediction_data = self.match_data[self.match_data['WinningTeam'] != 'No Result'].copy()
        
        if len(prediction_data) < 10:
            st.warning("Not enough data for prediction model")
            return
        
       
        features = ['Team1', 'Team2', 'Venue', 'TossWinner', 'TossDecision']
        
        
        le_team = LabelEncoder()
        le_venue = LabelEncoder()
        le_decision = LabelEncoder()
        
        all_teams = pd.concat([prediction_data['Team1'], prediction_data['Team2']]).unique()
        le_team.fit(all_teams)
        
        prediction_data['Team1_encoded'] = le_team.transform(prediction_data['Team1'])
        prediction_data['Team2_encoded'] = le_team.transform(prediction_data['Team2'])
        prediction_data['Venue_encoded'] = le_venue.fit_transform(prediction_data['Venue'])
        prediction_data['TossWinner_encoded'] = le_team.transform(prediction_data['TossWinner'])
        prediction_data['TossDecision_encoded'] = le_decision.fit_transform(prediction_data['TossDecision'])
        prediction_data['Target'] = le_team.transform(prediction_data['WinningTeam'])
        
       
        X = prediction_data[['Team1_encoded', 'Team2_encoded', 'Venue_encoded', 
                           'TossWinner_encoded', 'TossDecision_encoded']]
        y = prediction_data['Target']
        
        
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)
        
        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        st.metric("Model Accuracy", f"{accuracy * 100:.2f}%")
        
        
        st.subheader("Predict Match Outcome")
        
        col1, col2 = st.columns(2)
        
        with col1:
            team1 = st.selectbox("Team 1", all_teams)
            venue = st.selectbox("Venue", prediction_data['Venue'].unique())
        
        with col2:
            team2 = st.selectbox("Team 2", [t for t in all_teams if t != team1])
            toss_winner = st.selectbox("Toss Winner", [team1, team2])
            toss_decision = st.selectbox("Toss Decision", ['bat', 'field'])
        
        if st.button("Predict Winner"):
            
            input_data = pd.DataFrame({
                'Team1_encoded': [le_team.transform([team1])[0]],
                'Team2_encoded': [le_team.transform([team2])[0]],
                'Venue_encoded': [le_venue.transform([venue])[0]],
                'TossWinner_encoded': [le_team.transform([toss_winner])[0]],
                'TossDecision_encoded': [le_decision.transform([toss_decision])[0]]
            })
            
            
            probabilities = model.predict_proba(input_data)[0]
            teams = le_team.classes_
            
            
            result_df = pd.DataFrame({
                'Team': teams,
                'Win Probability': probabilities
            }).sort_values('Win Probability', ascending=False)
            
            st.subheader("Prediction Results")
            
            for _, row in result_df.head().iterrows():
                if row['Win Probability'] > 0:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"{row['Team']}")
                    with col2:
                        st.write(f"{row['Win Probability'] * 100:.1f}%")
                    
                    
                    st.progress(float(row['Win Probability']))
    
    def seasonal_analysis(self):
        """Season-wise analysis"""
        st.header("📈 Seasonal Analysis")
        
       
        season_stats = self.match_data.groupby('Season').agg({
            'ID': 'count',
            'WinningTeam': lambda x: (x != 'No Result').sum()
        }).rename(columns={'ID': 'Total Matches', 'WinningTeam': 'Completed Matches'})
        
        
        champions = []
        for season in self.match_data['Season'].unique():
            season_matches = self.match_data[self.match_data['Season'] == season]
            
            wins = season_matches[season_matches['WinningTeam'] != 'No Result']['WinningTeam'].value_counts()
            if len(wins) > 0:
                champions.append({'Season': season, 'Champion': wins.index[0], 'Wins': wins.iloc[0]})
        
        champion_df = pd.DataFrame(champions)
        
        st.subheader("Season Overview")
        st.dataframe(season_stats)
        
        if not champion_df.empty:
            st.subheader("Season Champions")
            st.dataframe(champion_df)
            
            
            fig = px.bar(champion_df, x='Season', y='Wins', color='Champion',
                        title='Champion Teams by Season')
            st.plotly_chart(fig)
    
    def player_of_match_analysis(self):
        """Player of the Match analysis"""
        st.header("⭐ Player of the Match Analysis")
        
        
        potm_counts = self.match_data['Player_of_Match'].value_counts().head(15)
        
        fig = px.bar(potm_counts, x=potm_counts.index, y=potm_counts.values,
                     title='Top 15 Player of the Match Award Winners')
        st.plotly_chart(fig)
        
        
        potm_team = self.match_data.groupby(['WinningTeam', 'Player_of_Match']).size().reset_index(name='Count')
        top_potm_team = potm_team.groupby('WinningTeam').apply(
            lambda x: x.nlargest(1, 'Count')
        ).reset_index(drop=True)
        
        st.subheader("Top Player of the Match by Team")
        st.dataframe(top_potm_team)

def main():
    st.title("🏏 IPL Cricket Data Analysis")
    st.markdown('<div class="main-header">Comprehensive IPL Tournament Analysis</div>', unsafe_allow_html=True)
    
    
    uploaded_file = st.file_uploader("Upload IPL Dataset (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            
            data = pd.read_csv(uploaded_file)
            st.success(f"Data loaded successfully! Shape: {data.shape}")
            
            
            analyzer = IPLAnalysis(data)
            
            
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
                analyzer.team_dashboard()
            elif analysis_type == "Player Analysis":
                analyzer.player_analysis()
            elif analysis_type == "Toss Impact Analysis":
                analyzer.toss_analysis()
            elif analysis_type == "Venue Analysis":
                analyzer.venue_analysis()
            elif analysis_type == "Seasonal Analysis":
                analyzer.seasonal_analysis()
            elif analysis_type == "Player of Match Analysis":
                analyzer.player_of_match_analysis()
            elif analysis_type == "Winning Prediction":
                analyzer.winning_prediction()
            
            
            with st.expander("View Raw Data"):
                st.dataframe(data.head(100))
                
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
    else:
        st.info("Please upload a CSV file to begin analysis")
        
        
        st.subheader("Expected Data Format")
        st.write("""
        The CSV file should contain the following columns:
        - ID: Match identifier
        - Season: Tournament season
        - Matchnumber: Match number
        - Team1, Team2: Competing teams
        - Venue: Match venue
        - TossWinner: Team that won the toss
        - TossDecision: Decision after winning toss (bat/field)
        - WinningTeam: Match winner
        - Player_of_Match: Man of the match
        - batter, bowler, non-striker: Player information
        - batsman_run: Runs scored by batsman
        - extra_run: Extra runs
        - total_run: Total runs in delivery
        - isWicketDelivery: Whether wicket fell
        - Player_out: Player dismissed
        """)

if __name__ == "__main__":
    main()