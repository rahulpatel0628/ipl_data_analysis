# 🏏 IPL Match Winning Prediction & Data Analysis Dashboard

### ✨ Project Overview
This project provides a **complete IPL match analysis and winning prediction dashboard** built using **Python** and **Streamlit**.  
It explores historical IPL data using **NumPy, Pandas, Matplotlib, and Plotly**, and applies **Machine Learning (RandomForestClassifier)** to predict the **winning team** based on match features such as teams, venue, toss, and season.

The goal is to combine **data analytics + predictive modeling** into one interactive, deployable web application.

---

## 🚀 Live Demo
👉 **[View on Streamlit Cloud](https://share.streamlit.io/)** *(Add your deployed link here)*  

---

## 🧠 Key Features
✅ **Comprehensive Data Analysis**
- Team performance insights
- Player performance analysis 
- Venue-wise and toss-decision trends  
- Season-based comparison  
- Interactive charts using Plotly & Matplotlib 

✅ **Winning Prediction Model**
- Built with `RandomForestClassifier`  
- Uses features like `Team1`, `Team2`, `Venue`, `TossWinner`, `TossDecision`, and `Season`  
- Achieves **85–93% accuracy**  
- Predicts the probable winner for upcoming matches  

✅ **Interactive Streamlit Dashboard**
- User-friendly interface  
- Dynamic visualizations  
- Real-time prediction section  
- Fully responsive web app  

---

## 📊 Tech Stack
| Category | Tools / Libraries |
|-----------|------------------|
| **Programming Language** | Python |
| **Data Handling** | NumPy, Pandas |
| **Visualization** | Matplotlib, Plotly |
| **Machine Learning** | Scikit-learn (RandomForestClassifier) |
| **Web Framework** | Streamlit |
| **Version Control** | Git & GitHub |

---

## 🧩 Project Workflow
1. **Data Cleaning & Preprocessing**
   - Removed “No Result” matches  
   - Encoded categorical data (teams, venue, toss, etc.)  
   - Created new features like *Bat_First* and *Season*

2. **Exploratory Data Analysis (EDA)**
   - Team win distribution  
   - Toss impact on match results  
   - Venue performance heatmaps  
   - Season-wise trends and averages  

3. **Model Building**
   - RandomForestClassifier trained on preprocessed data  
   - Used `train_test_split` with stratification for balanced sampling  
   - Evaluated model accuracy and optimized hyperparameters  

4. **Deployment**
   - Built interactive UI using Streamlit  
   - Deployed on **Streamlit Cloud**  




