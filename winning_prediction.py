import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
class WinningPrediction:
    def __init__(self,data1,data2):
        self.data1=data1
        self.data2=data2
    def winning_prediction(self):
        st.header("IPL Winning Team Prediction")

        
        data = self.data1[self.data1['WinningTeam'] != 'No Result'].copy()

        if len(data) < 10:
            st.warning("Not enough data available for training.")
            return

       
        features = ['Team1', 'Team2', 'Venue', 'TossWinner', 'TossDecision']
        target = 'WinningTeam'

        
        encoders = {}
        for col in features + [target]:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            encoders[col] = le

        
        X = data[features]
        y = data[target]

        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        
        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=12,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        
        accuracy = accuracy_score(y_test, y_pred)
        st.metric("Model Accuracy", f"{accuracy * 100:.2f}%")

        st.divider()
        st.subheader("🎯 Predict Match Outcome")

        
        team1 = st.selectbox("Select Team 1", encoders['Team1'].classes_)
        team2 = st.selectbox("Select Team 2", [t for t in encoders['Team2'].classes_ if t != team1])
        venue = st.selectbox("Select Venue", encoders['Venue'].classes_)
        toss_winner = st.selectbox("Toss Winner", [team1, team2])
        toss_decision = st.selectbox("Toss Decision", ['bat', 'field'])

        if st.button("Predict Winner"):
           
            input_df = pd.DataFrame({
                'Team1': [encoders['Team1'].transform([team1])[0]],
                'Team2': [encoders['Team2'].transform([team2])[0]],
                'Venue': [encoders['Venue'].transform([venue])[0]],
                'TossWinner': [encoders['TossWinner'].transform([toss_winner])[0]],
                'TossDecision': [encoders['TossDecision'].transform([toss_decision])[0]],
            })

            
            pred_encoded = model.predict(input_df)[0]
            winner = encoders['WinningTeam'].inverse_transform([pred_encoded])[0]

            st.success(f"🏆 Predicted Winner: **{winner}**")
