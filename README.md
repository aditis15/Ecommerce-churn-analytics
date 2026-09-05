# Ecommerce-churn-analytics

## What is this project about?
Businesses lose a lot of revenue because they don't notice when a customer is about to stop buying — by the time they realize, that customer is usually already gone. In this project, I tried to analyze customer purchase data to figure out which customers are likely to stop buying soon, so a business could reach out to them before losing them for good.

## What I built
- Cleaned and worked with a real e-commerce dataset (Online Retail II from Kaggle/UCI)
- Calculated some key things for each customer — how recently they bought something, how often they buy, and how much they've spent overall
- Used a simple rule to flag customers as High/Medium/Low risk of churning
- Also trained a basic machine learning model (logistic regression) to predict churn based on customer behavior
- Wrote code to auto-generate a simple retention message for high-risk customers
- Built an interactive dashboard using Streamlit so all of this is easy to look at and explore

## Tools I used
- Python (pandas for data handling, scikit-learn for the ML model)
- SQL (SQLite) for querying the customer data
- Streamlit and Plotly for the dashboard/visuals

## About the model
I trained a logistic regression model using purchase frequency and total spend as features. It got about 69% accuracy, and correctly identified 82% of customers who actually churned. I focused more on recall (catching actual churners) than overall accuracy, since missing a customer who's about to leave is a bigger loss for a business than wrongly flagging someone who wasn't going to leave anyway.

## How to run it
1. Install the required libraries: `pip install pandas scikit-learn streamlit plotly`
2. Run `main.py` first — this cleans the data, builds the features, and trains the model
3. Then run `streamlit run app.py` to open the dashboard

## Things I'd improve with more time
- Right now this works on historical data all at once (batch processing), not live/real-time data — that's something I'd like to add later
- The model only uses 2 features right now, more behavioral data (like product category, or how often they browse) could make it more accurate
- Eventually I'd like to deploy this online and maybe simulate real-time data updates

This was my first proper data analytics project, and I built it step by step while learning Python, SQL, and basic ML along the way.
