# spark-churn-prediction
Predictive customer churn analysis using PySpark on Databricks with a large synthetic dataset.

### Table of Content:
1. Project Definition/Goals
2. Data Generation
3. Technology Used
4. Environment Setup
5. How to Run
6. Findings
7. Challenges Encountered 
8. Future Imporvements

## Project Definition/Goals
This project was designed solve the problem of predicting which custmers are going to discontinue their service (churn rate). Businesses need a way to tell which constomers are likely to leave, so that the business may be able to provide incentives for the customers to stay.

The objective of this project is to develop a model using spark that will be able to output whether a customer is going to discontinue the service or not.

## Data Generation
For this project, I wanted to use spark. To justify this, I needed to use a very large dataset. I was not able to find a data set that was large enough to justify the use of spark, so I generated my own data using Faker. 

Under /data, I have the code that I used to generate the data. For this project, I generated 10,000,000 rows of data. This was the schema of the data set:

| Feature         | Data Type | Description                         |
| :-------------- | :-------- | :---------------------------------- |
| name            | String    | Name of the customer                |
| CustomerID      | String    | A unique identifier for the customer |
| TenureMonths    | Integer   | How many months a customer has stayed |
| MonthlyCharges   | Double    | Amount the customer is paying every month |
| email           | String    | Customer email                      |
| PhoneNumber     | String    | Customer phone number               |
| Churn           | String    | 1 if chuned, 0 if otherwise         |
| TotalCharge     | Double    | How much in total the customer has spent |

Note: Churn and TotalCharge was constructed by TenureMonths and MonthlyCharges.



The key feature of this script is the line where each churn probability is defined. This was the code used:


```churn_prob = 0.1 + (df['MonthlyCharges']/300) - (df['TenureMonths']/200)```

This assignes a probability of churnning for each customer based on their monthly charges and tenured months. 

## Technology Used
* PySpark 
* Python version 3.12 
* Databricks CE 
* Pandas 
* Scikit-learn 
* Matplotlib/Seaborn

## Environment Setup

1. Set up your free acount [here](https://community.cloud.databricks.com/login.html?tuuid=fb460278-29ef-4443-85d0-584165afc6bc&scid=701Vp000004h4c4IAA&utm_medium=programmatic&utm_source=google&utm_campaign=22507112156&utm_adgroup=&utm_content=summit&utm_offer=dataaisummit&utm_ad=&utm_term=&gad_source=1&gad_campaignid=22507113074&gclid=EAIaIQobChMI2bnuuZDKjQMVSUhHAR1YqhDyEAAYASAAEgLtA_D_BwE)

2. Once you create your free account, create a cluster under the compute tab. For the runtime, select 14.3 LTS with Scala 2.12 and Spark 3.5.0.

## Project Workflow 
1. Click the "+ New" button and upload the CSV file created by the python script under "/data". Once uploaded, it will be in the "/FileStore/tables/" directory.

2. Create a notebook. Make sure that the cluster that was created is connected to the notebook. Run the code that is under the "/notebook" folder.

## Project Summary
For my project, I used both logistic regression and random forrest classifier. 

These two models used the dataframe created by Spark:

For the logistic regression, these are the calculated statistics:
* Area under ROC (AUC): "0.7535"
* accuracy: "0.8317"
* precision: "0.7780"
* Recall: "0.8317"
* f1 Score: "0.7694"

The statistic that I'd like to focus on is the Area under ROC. Considering that fact that it is above 0.5, we can see that the model is performing better than if the model produced predictions at random. Considering the fact that the ratio of churn and not churn is not faily balanced, it may not be appropriate to take the accuracy metric at face value.

For the random forrest classifier, these are the calculated statistics:
* Area under ROC (AUC): "0.6917"
* accuracy: "0.8323"
* precision: "0.6927"
* Recall: "0.8323"
* f1 Score: "0.7561"

The area under ROC metric for the random forrest classifier shows that this model has better predictive power than random. However, we can see that the logistic regression model performs better.

These two models use another dataframe created by this sql command:

```
SELECT
    CustomerID,
    TenureMonths,
    MonthlyCharges,
    TotalCharges,
    Churn,
    CASE
        WHEN TenureMonths <= 12 THEN 'Low_Tenure'
        WHEN TenureMonths > 12 AND TenureMonths <= 48 THEN 'Mid_Tenure'
        ELSE 'High_Tenure'
    END AS TenureCategory
FROM churn_data
WHERE MonthlyCharges > 0
```

This creates a new variable called TenureCategoty where each user is categorized as "Low_Tenure", "Mid_Tenure", and "High_Tenure".

For the logistic regression, these are the calculated statistics:
* Area under ROC (AUC): "0.7539"
* accuracy: "0.8317"
* precision: "0.7777"
* Recall: "0.8317"
* f1 Score: "0.7691"

We can see from the Area under ROC metric that this model is better at predicting churn than random.

For the random forrest classier model, these are the statistics:
* Area under ROC (AUC): "0.7140"
* accuracy: "0.8323"
* precision: "0.6928"
* Recall: "0.8323"
* f1 Score: "0.7562"

This model is better at predicting churn than random as well.

We can see that the model that performed best under the Area under ROC metric is the logistic regression model using the features created by the sql query.

## Challenges Encountered

The main challenge faced when constructing these models was having good variability in the data. When running the script to create the model, there were not that many distinct probabilities (22 for the first two models and 30 for the next two). Compared to the number of rows, the low number of distinct probabilities may call affect the predictive power of the models.

## Future Improvements

I can use different models such as gradiant boosting to see if it produces better results. I can also use more advanced feature engineering techniques in order to create more ways that the model can distinquish data points and create more accurate classifications.

