import pandas as pd
import numpy as np

# 1. INVENTORY SAMPLE DATA (Simulated Warehouse Data)
# In professional practice, this data could be loaded from an Excel/CSV file using pd.read_excel()
data = {
    'Item_Code': ['A001', 'A002', 'A003', 'A004', 'A005', 'A006', 'A007'],
    'Item_Name': ['M8 Steel Bolt', '2HP Electric Motor', '10m Copper Cable', 'Proximity Sensor', 'Shell Lubricant 1L', 'Brass Nut', 'Pipe Clamp'],
    'Annual_Usage_Qty': [5000, 150, 800, 300, 1200, 15000, 450],
    'Unit_Cost_IDR': [1500, 4500000, 75000, 250000, 95000, 400, 3500],
    'Avg_Daily_Demand': [15, 0.5, 2.5, 1.0, 3.5, 45, 1.5],
    'Lead_Time_Days': [5, 30, 7, 14, 4, 5, 3],
    'Demand_Std_Dev': [3.0, 0.1, 0.5, 0.2, 0.8, 8.0, 0.4] # Demand variability
}

df = pd.DataFrame(data)

# =========================================================================
# 2. ABC ANALYSIS (Based on Annual Value)
# =========================================================================
df['Annual_Value_IDR'] = df['Annual_Usage_Qty'] * df['Unit_Cost_IDR']

# Sort by annual value from highest to lowest
df = df.sort_values(by='Annual_Value_IDR', ascending=False).reset_index(drop=True)

# Calculate cumulative value and percentage
df['Cumulative_Value_IDR'] = df['Annual_Value_IDR'].cumsum()
total_value = df['Annual_Value_IDR'].sum()
df['Cumulative_Percentage'] = (df['Cumulative_Value_IDR'] / total_value) * 100

# Classification rules:
# Class A: ~70-80% value contribution (High Priority)
# Class B: ~15-20% value contribution (Medium Priority)
# Class C: ~5-10%  value contribution (Low Priority)
def classify_abc(percentage):
    if percentage <= 75:
        return 'A'
    elif percentage <= 95:
        return 'B'
    else:
        return 'C'

df['ABC_Class'] = df['Cumulative_Percentage'].apply(classify_abc)

# =========================================================================
# 3. SAFETY STOCK & REORDER POINT (ROP) CALCULATION
# =========================================================================
# Using 95% Service Level (standard Z-Score = 1.65)
Z_SCORE = 1.65 

# Formula when lead time is fixed but demand varies:
# Safety Stock = Z * (Demand Std Dev * sqrt(Lead Time))
df['Safety_Stock'] = np.ceil(Z_SCORE * df['Demand_Std_Dev'] * np.sqrt(df['Lead_Time_Days']))

# Reorder Point (ROP) Formula:
# ROP = (Avg Daily Demand * Lead Time) + Safety Stock
df['Reorder_Point_ROP'] = np.ceil((df['Avg_Daily_Demand'] * df['Lead_Time_Days']) + df['Safety_Stock'])

# =========================================================================
# 4. SHOWING RESULTS
# =========================================================================
print("=== INVENTORY ANALYSIS & MATERIAL CONTROL RESULTS ===")
print(df[['Item_Code', 'Item_Name', 'ABC_Class', 'Safety_Stock', 'Reorder_Point_ROP']])
