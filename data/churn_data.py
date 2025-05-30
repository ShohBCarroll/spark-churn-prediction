import numpy as np
import pandas as pd
from faker import Faker 

fake = Faker() 

num_rows = 10000000

data = {
    'name': [fake.name() for i in range(num_rows)],
    'CustomerID': [f'CUST_{i:09d}' for i in range(num_rows)],
    'TenureMonths': np.random.randint(1,70, num_rows),
    'MonthlyCharges': np.round(np.random.normal(70, 30, num_rows), 2),
    'email': [fake.email() for i in range(num_rows)],
    'PhoneNumber': [fake.phone_number() for i in range(num_rows)]
}

df = pd.DataFrame(data)

churn_prob = 0.1 + (df['MonthlyCharges']/300) - (df['TenureMonths']/200)
df['Churn'] = (np.random.rand(num_rows) < churn_prob).astype(int)
df['TotalCharges'] = np.round((df['MonthlyCharges']) * (df['TenureMonths']) * np.random.uniform(0.8, 1.2, num_rows), 2)
df.loc[df['TotalCharges'] < 0, 'TotalCharges'] = 0

df.loc[df['MonthlyCharges'] < 0, 'MonthlyCharges'] = df['MonthlyCharges'].median()

df.to_csv('synthetic_churn_data.csv', index=False)
print(f"Generated {num_rows} rows.")

