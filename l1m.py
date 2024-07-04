import pandas as pd

# Load the Excel files and add prefixes to the column names
df_all = pd.read_excel('labels_1m_all.xlsx')
df_con = pd.read_excel('labels_1m_con.xlsx')
df_miss = pd.read_excel('labels_1m_miss.xlsx')

df_all = df_all.add_prefix('All_')
df_con = df_con.add_prefix('Con_')
df_miss = df_miss.add_prefix('Miss_')

df_all.rename(columns={'All_RigDateID': 'RigDateID'}, inplace=True)
df_con.rename(columns={'Con_RigDateID': 'RigDateID'}, inplace=True)
df_miss.rename(columns={'Miss_RigDateID': 'RigDateID'}, inplace=True)

# Merge the DataFrames on 'RigDateID'
merged_df = pd.merge(df_all, df_con, on='RigDateID', how='inner')
merged_df = pd.merge(merged_df, df_miss, on='RigDateID', how='inner')

print(merged_df.head()) 
print(merged_df.info())

# Drop specified columns
columns_to_drop = [
    'Miss_Rig', 'Miss_YearMonth', 'Miss_Year', 'Miss_Month',
    'Con_Rig', 'Con_YearMonth', 'Con_Year', 'Con_Month'
]
merged_df.drop(columns_to_drop, axis=1, inplace=True)

# Rename the columns
rename_dict = {
    'All_Rig': 'Rig',
    'All_YearMonth': 'YearMonth',
    'All_Year': 'Year',
    'All_Month': 'Month'
}
merged_df.rename(columns=rename_dict, inplace=True)
print(merged_df.info())

# Merge the DataFrame with the manhour data
df_hr = pd.read_excel('manhour_1m.xlsx')
merged_df = pd.merge(merged_df, df_hr, on='RigDateID', how='inner')

df_1=merged_df.drop([
    'Rig_y', 'YearMonth_y', 'Year_y', 'Month_y'
], axis=1)
rename_columns = {
    'Rig_x': 'Rig',
    'YearMonth_x': 'YearMonth',
    'Year_x': 'Year',
    'Month_x': 'Month'
}
df_1.rename(columns=rename_columns, inplace=True)
print(df_1.info())

# # Delete rows where Manhours_4M or TotalManhours is 0
df_1= df_1[df_1['TotalManhours'] != 0]
df_2=df_1.copy()
print(df_2.info())

# # # Normalize the columns
col_to_normal = [
    'All_TotalEvents', 'All_RiskCalculatedValue', 'All_ActualSeverity',
    'Con_TotalEvents', 'Con_RiskCalculatedValue', 'Con_ActualSeverity',
    'Miss_TotalEvents', 'Miss_RiskCalculatedValue', 'Miss_ActualSeverity'
]
for column in col_to_normal:
    # Calculate per 1000 man-hours
    df_2.loc[:, column] = (df_2[column] / df_2['TotalManhours']) * 1000

print(df_1[col_to_normal].describe().transpose())

top_5=df_2.set_index('RigDateID').nlargest(5, 'All_TotalEvents').transpose()
print(top_5)

df_2.to_excel('labels_1m.xlsx', index=False)