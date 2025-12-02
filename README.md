# Acquisition-Analysis-Campaign
**Overview**
The company ran a recent marketing campaign to promote the value proposition of how the debt relief program helps people achieve financial freedom. Assume the cost of this campaign was $5 million. There are five months of data in the datasets provided. Let’s say campaign took place over the course of the third month. We want to show the marketing, sales and operations teams just how successful this campaign was.

Analysis
Customers
  - Age
print(df['client_age'].describe())
This content is only supported in a Lark Docs
  - Geography
print(df['client_geographical_region'].value_counts())
This content is only supported in a Lark Docs
  - Rent or Own
print(df['client_residence_status'].value_counts())
This content is only supported in a Lark Docs
  - Amount per month
Deposit
  - Total amount per month
This content is only supported in a Lark Docs
[Image]
  
  - Actual deposit
  - Schedual deposit
This content is only supported in a Lark Docs
  
  
This content is only supported in a Lark Docs
[Image]
Earnings
  - Total amount of earnings per month
Costs
  - 5million
**Q1**
**What metric to assess the success of the campaign**
1. New joiners after the campaign and New actual deposit invested after the campaign
Indicator: 
1.  Month-over-Month (MoM) Growth Rate . During the campaign, 11544 new joiners registered and deposited the actual amount, which grew by 33.24%. 
2. ROI is -0.95%
3. LTV Average Customer LTV
Based on Freedom's business model, a successful marketing campaign must achieve two things: Acquire Clients and Generate Revenue.
1. Acquisition Efficiency: Incremental New Clients
  - Calculation: (Total New Clients in Month 3, 4, 5) - (Average Monthly New Clients in Month 1, 2) $\times$ 3.
  - Rationale: Focuses on the additional clients brought in by the campaign, excluding the baseline (organic) growth.
2. Profitability: Marketing Return on Investment (Marketing ROI)
  - $$ROI = \frac{(\text{Settlement Fee Revenue}) - (\text{Campaign Cost} + \text{Ongoing Client Cost})}{\text{Campaign Cost}}$$
  - Calculation Challenges: You must assume industry statistics as instructed in the project brief to estimate revenue and costs:
    - Assumption 1 (Revenue): Settlement Fee Percentage (e.g., assume Freedom collects 15%-25% of the settled amount as fees).
    - Assumption 2 (Cost): Ongoing Cost per Client (e.g., assume a monthly operational cost per client).
  - Core Logic: Revenue is proportional to the total deposit amount. Therefore, you can estimate incremental revenue by comparing the incremental total deposits from Month 3-5.
3. Client Quality: Trend Change in Average Customer Lifetime Value (LTV)
  - You can indirectly assess LTV change by comparing the average monthly deposit amount of new clients acquired in Month 3-5 with those acquired in Month 1-2. A higher average deposit suggests higher LTV and healthier clients.

df_actual_only = df[df["deposit_type"] == "Actual Deposit"]

# Compute total deposit per month
monthly_actual = df_actual_only.groupby("month_name")["deposit_amount"].sum().sort_index()

print("Actual Deposit Amounts Per Month:")
print(monthly_actual)

clients_before = df[df["month_name"].isin(["Month 1", "Month 2"])]["client_id"].unique()
clients_during = df[df["month_name"] == "Month 3"]["client_id"].unique()
clients_after = df[df["month_name"].isin(["Month 4", "Month 5"])]["client_id"].unique()
new_clients_during = set(clients_during) - set(clients_before)
new_clients_after = set(clients_after) - set(clients_before) - set(clients_during)

print("New clients during campaign:", len(new_clients_during))
print("New clients after campaign:", len(new_clients_after))
 Month-over-Month (MoM) Growth Rate 
This content is only supported in a Lark Docs
This content is only supported in a Lark Docs
[Image]
2. ROI analysis 
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
This content is only supported in a Lark Docs
3. Total gain every month
**Q2**
**What strategy can be used for further campaign**
Geographical Region Analysis (client_geographical_region):
- Calculate the Customer Acquisition Cost (CAC) by region: Which region has the highest client conversion rate?
- Recommendation: Shift future marketing budgets towards geographical regions with the highest return on investment.
Client Age Analysis (client_age):
- Calculate the Average Deposit Amount across different age groups: Which age group represents the highest quality clients (i.e., highest average deposit)?
- Recommendation: Tailor content delivery specifically to the age group with the highest LTV.
Residence Status Analysis (client_residence_status):
- Compare acquisition efficiency and deposit behavior between "Renters" and "Owners."
- Recommendation: If owners show more stable or higher deposits, focus marketing efforts on the population segment with property ownership.
1. Identify the real target customers
2. Decrease the budget
**Q3**
**What if the campaign is postponed by 3 months**
Core Idea: Utilizing Trend Forecasting
Since you only have five months of data, to predict Month 6, you must either build a time series model (though data points are few) or simply use linear/average trend extrapolation.
1. Establish Baseline Trend:
  - Calculate the natural growth trend from Month 1 to Month 5 excluding the campaign's impact.
  - How to exclude the campaign's impact? Assume that without the campaign, Month 3's data would follow the same natural decay trend as Month 4 and Month 5. Or, more simply, use only Month 1 and Month 2 data to extrapolate the no-intervention baseline for Month 3, 4, 5, and 6.
2. Forecast Month 6 Baseline Result:
  - Use Month 1 and Month 2 data (or a more complex trend model) to predict the natural expected value for new clients and total deposits in Month 6 ($Base_6$).
3. Apply Campaign Effect:
  - Linearly add the incremental effect of the campaign ($\Delta_{campaign}$, e.g., incremental new clients, incremental deposits) calculated in Question 1 to the predicted Month 6 baseline value.
4. $$\text{Month 6 Campaign Result} = Base_6 + \Delta_{campaign}$$
5. Calculate Incremental Number:
  - The final incremental number is the difference between the Month 6 Campaign result and the Month 3 Campaign result (the result you obtained in Question 1).
6. $$\text{Incremental Change} = (\text{Month 6 Campaign Result}) - (\text{Month 3 Campaign Result})$$
Breaking the 'No Clue' Barrier: The focus must be on calculating $\Delta_{campaign}$. Once you have this "effect increment," you can apply it to the baseline forecast of any month.
