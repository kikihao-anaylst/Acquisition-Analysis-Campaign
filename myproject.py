import pandas as pd
client_data = pd.read_csv("datasets/client_data.csv")
print("Client data shape",client_data.shape)
print(client_data.head())
deposit_data = pd.read_csv('datasets/deposit_data.csv')
print('deposit data shape',deposit_data.shape)
print(deposit_data.head())
calendar_data = pd.read_csv('datasets/calendar_data.csv')
print('deposit data shape',deposit_data.shape)
print(deposit_data.head())

df_merged = client_data.merge(deposit_data, on='client_id')
df = df_merged.merge(calendar_data,left_on ='deposit_date',right_on='gregorian_date',copy=False)
print(df.head())

df.drop(columns='gregorian_date',inplace=True)

print(df['client_geographical_region'].value_counts())
print(df['client_age'].describe())
print(df['client_residence_status'].value_counts())

print(calendar_data['month_name'].value_counts())
print(df['deposit_type'].value_counts())
print(df['deposit_cadence'].value_counts())
print(df['deposit_date'].min(),df['deposit_date'].max())

df['deposit_date']=pd.to_datetime(df['deposit_date'])

from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (10,7)

deposit_amount_by_month = df.groupby(by=df['month_name'])['deposit_amount'].sum()


print(deposit_amount_by_month)
plt.plot(deposit_amount_by_month)
plt.title('deposit amount by month')
plt.ylabel('Deposit amount')
plt.xlabel('month')
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.show()
deposit_amount_by_month_st1 = df.groupby("month_name")["deposit_amount"].sum()

plt.plot(
    deposit_amount_by_month_st1.index,
    deposit_amount_by_month_st1.values
)
plt.title("Actual Deposit Amount per Month")
plt.xlabel("Month")
plt.ylabel("Deposit Amount")
plt.grid(True)
plt.show()

df_actual_only = df[df["deposit_type"] == "Actual Deposit"]

# Compute total deposit per month
monthly_actual = df_actual_only.groupby("month_name")["deposit_amount"].sum().sort_index()

print("Actual Deposit Amounts Per Month:")
print(monthly_actual)


pre_avg = deposit_amount_by_month_st1[["Month 1", "Month 2"]].mean()
print("Pre-campaign average:", pre_avg)

delta_m3 = deposit_amount_by_month_st1["Month 3"] - pre_avg
print("Delta Month 3:", delta_m3)

delta_m4 = deposit_amount_by_month_st1["Month 4"] - pre_avg
print("Delta Month 4:", delta_m4)

delta_m5 = deposit_amount_by_month_st1["Month 5"] - pre_avg
print("Delta Month 5:", delta_m5)

total_gain = delta_m3 + delta_m4 + delta_m5
print("Total campaign lift:", total_gain)

estimated_revenue = total_gain * 0.18

print("Estimated revenue (18% service fee):", estimated_revenue)
clients_before = df[df["month_name"].isin(["Month 1", "Month 2"])]["client_id"].unique()
clients_during = df[df["month_name"] == "Month 3"]["client_id"].unique()
clients_after = df[df["month_name"].isin(["Month 4", "Month 5"])]["client_id"].unique()
new_clients_during = set(clients_during) - set(clients_before)
new_clients_after = set(clients_after) - set(clients_before) - set(clients_during)

print("New clients during campaign:", len(new_clients_during))
print("New clients after campaign:", len(new_clients_after))

monthly_counts = df_actual_only.groupby("month_name").size()
monthly_counts.plot(title="Number of Actual Deposits per Month")
plt.xlabel("Month")
plt.ylabel("Count")
plt.grid(True)
plt.show()

