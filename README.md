# 📊 Telecom Customer Churn Prediction

A Machine Learning project for predicting customer churn in the telecommunications industry using multiple classification models and an interactive Streamlit dashboard.

## 🚀 Live Demo

🔗 **Streamlit App:** https://telecom-customer-churn-3edenvhrggyzukofwar9ap.streamlit.app/

---

## 📌 Project Overview

Customer churn is a major challenge for telecommunications companies. The goal of this project is to analyze customer behavior, identify factors associated with churn, and build Machine Learning models capable of predicting customers who are likely to leave the service.

The project covers the complete Machine Learning workflow:

**Data Cleaning → Exploratory Data Analysis → Feature Engineering → Model Training → Hyperparameter Tuning → Model Evaluation → Insights → Deployment**

---

## 🎯 Objectives

* Understand the main factors associated with customer churn.
* Perform comprehensive Exploratory Data Analysis (EDA).
* Prepare and preprocess the dataset for Machine Learning.
* Train and compare multiple classification models.
* Tune model hyperparameters.
* Evaluate models using appropriate classification metrics.
* Generate actionable customer churn insights.
* Deploy the prediction model through an interactive Streamlit application.

---

## 📂 Dataset

The project uses the **Telco Customer Churn Dataset** from Kaggle.

🔗 **Dataset:** https://www.kaggle.com/datasets/blastchar/telco-customer-churn

The dataset contains customer demographic information, service subscriptions, contract details, payment methods, tenure, and billing information.

### Target Variable

**Churn**

* `Yes` → Customer churned
* `No` → Customer stayed

The original dataset contains **7,043 customers and 21 features**.

---

## 🔎 Exploratory Data Analysis

The EDA process investigates:

* Churn distribution
* Customer tenure
* Monthly and total charges
* Contract types
* Payment methods
* Internet services
* Customer demographics
* Service subscriptions
* Relationships between customer characteristics and churn

The analysis was used to identify patterns and potential churn drivers before model development.

---

## 🧹 Data Preprocessing

The preprocessing pipeline included:

* Handling missing values
* Converting `TotalCharges` to numeric format
* Encoding categorical variables
* Feature transformation
* Removing unnecessary identifiers such as `customerID`
* Preparing features for Machine Learning
* Scaling features where required

The processed dataset is stored in:

```text
processed_data.csv
```

---

## 🤖 Machine Learning Models

Several classification algorithms were trained and evaluated:

* Logistic Regression
* Decision Tree
* Random Forest
* XGBoost

Hyperparameter tuning was also performed to improve model performance.

### Model Selection

The final model selection was based on classification performance, with particular attention to the ability to identify customers who are likely to churn.

The project includes the trained model artifacts:

```text
best_xgb.pkl
churn_model.pkl
scaler.pkl
```

---

## 📈 Model Evaluation

The models were evaluated using:

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC
* Confusion Matrix

For churn prediction, **Recall for the churn class** is particularly important because missing a customer who is likely to churn can represent a valuable retention opportunity.

The tuned model achieved a ROC-AUC score of approximately:

**0.862**

---

## 💡 Customer Churn Insights

The project investigates customer characteristics that are associated with higher churn risk, helping translate Machine Learning results into business-oriented insights.

The analysis focuses on factors such as:

* Contract type
* Customer tenure
* Monthly charges
* Internet service
* Payment method
* Additional services

These insights can help businesses identify high-risk customer segments and design targeted retention strategies.

---

## 🧠 Model Explainability

Model explainability techniques were used to better understand how customer features contribute to predictions.

The project includes model insights generated during the analysis and provides a foundation for interpreting Machine Learning predictions from a business perspective.

---

## 🖥️ Streamlit Application

The project includes an interactive Streamlit application that allows users to enter customer information and obtain a churn prediction.

The application uses the trained Machine Learning artifacts to provide predictions and churn probability.

### Main Application Features

* Customer information input
* Churn prediction
* Churn probability
* Interactive visualizations
* Model-based insights

---

## 📁 Project Structure

```text
telecom-customer-churn/
│
├── 01_EDA_and_Cleaning.ipynb
├── 02_Modeling.ipynb
├── 03_Insights_and_Saving.ipynb
│
├── app.py
│
├── best_xgb.pkl
├── churn_model.pkl
├── scaler.pkl
│
├── feature_names.json
├── preprocessing_config.json
│
├── processed_data.csv
├── requirements.txt
│
└── README.md
```

---

## 🛠️ Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* XGBoost
* SHAP
* Joblib
* Streamlit
* Jupyter Notebook

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/mohamedaamar744-ux/telecom-customer-churn.git
cd telecom-customer-churn
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Streamlit Application

Run:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📓 Notebooks

### `01_EDA_and_Cleaning.ipynb`

Contains:

* Data loading
* Data inspection
* Data cleaning
* Exploratory Data Analysis
* Initial preprocessing

### `02_Modeling.ipynb`

Contains:

* Feature preparation
* Model training
* Model comparison
* Hyperparameter tuning
* Model evaluation

### `03_Insights_and_Saving.ipynb`

Contains:

* Model insights
* Feature analysis
* Saving trained models
* Saving preprocessing configuration
* Preparing artifacts for deployment

---

## 📌 Future Improvements

Potential improvements include:

* Advanced hyperparameter optimization
* Threshold optimization based on business costs
* Real-time monitoring of model performance
* Improved model explainability
* Automated retraining pipeline
* Deployment using a cloud platform

---

## 👨‍💻 Author

**Mohamed Amar**

Machine Learning & AI Student

---

⭐ If you find this project useful, feel free to explore the notebooks and the Streamlit application.
