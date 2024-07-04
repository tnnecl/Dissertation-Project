import pandas as pd
import numpy as np

# Load the Excel files
file1_path = 'abn_lead_raw.xlsx'
file2_path = 'pob_lead.xlsx'

# Read the Excel files 
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)

# # Merge the dataframes on the 'RigDateID' column
merged_df = pd.merge(df1, df2, on='RigDateID')

# Display the first few rows and the information of the merged dataframe
print(merged_df.head())

print(merged_df.info())


# Drop the columns 'Rig_Name', 'Year_y', 'Month_y', 'YearMonth_y' and rename the columns 'Year_x', 'Month_x', 'YearMonth_x'
df = merged_df.drop(['Rig_Name', 'Year_y', 'Month_y', 'YearMonth_y'], axis=1)

df.rename(columns={
    'Year_x': 'Year',
    'Month_x': 'Month',
    'YearMonth_x': 'YearMonth'
}, inplace=True)

df_1 = df[df['ManDays'] != 0]
df_2=df_1.copy()
print(df_1.info())

# Display rows where TotalCards is 0
cols_to_display = ['Rig', 'Year', 'Month', 'YearMonth', 'RigDateID', 'ManDays', 'TotalCards', 'Unsafe_Action', 'Low_Risk', 'RollingCrewStability']
filtered_df = df_1[df_1['TotalCards'] == 0][cols_to_display]
print(filtered_df)

# df_1.to_excel('features_lead.xlsx', index=False)


# # Percentize the columns
cols_to_per = [
    'Unsafe_Action', 'Unsafe_Condition', 'Unsafe_Condition_Cor',
    'Positive_Observation', 'Negative_Observation', 'Active_Action_Taken',
    'Low_Risk', 'Medium_Risk', 'High_Risk'
]
for col in cols_to_per:
    df_2[col] = df_2.apply(lambda row: row[col] / row['TotalCards'] if row['TotalCards'] != 0 else 0, axis=1)

cols_to_normalize = [
    'RollingPositionStability', 'RollingRigStability', 'RollingCrewStability'
]
for col in cols_to_normalize:
    df_2[col] = df_2.apply(lambda row: (row[col] / row['TotalEmployees']) if row['TotalEmployees'] != 0 else 0, axis=1)

top_5=df_2.set_index('RigDateID').nlargest(5, 'Normalized_Cards').transpose()
print(top_5)




# Calculate Alpha and Beta 
columns_to_process = ['Normalized_Cards', 'Negative_Observation']
for column in columns_to_process:
    # Mean and standard deviation for the column
    C_avg = df_2[column].mean()
    C_stdev = df_2[column].std()
    n = len(df_2[column])
    
    # Adding Alpha and Beta columns using lambda functions
    df_2[column + '_Alpha'] = df_2[column].apply(lambda x: (x - (C_avg + C_stdev)) / C_stdev)
    df_2[column + '_Beta'] = df_2[column].apply(lambda x: np.sqrt((x - C_avg)**2 / n) / C_stdev)


print(df_2.info())

# #Merge features and labels

label_4m=pd.read_excel('labels_4m.xlsx')
label_1m=pd.read_excel('labels_1m.xlsx')

df_4m= df_2.merge(label_4m, on='RigDateID', how='inner')
# print(df_4m.info())
df_4m= df_4m.drop(['Rig_y', 'Year_y', 'Month_y', 'YearMonth_y'], axis=1)
df_4m.rename(columns={
    'Rig_x': 'Rig',
    'Year_x': 'Year',
    'Month_x': 'Month',
    'YearMonth_x': 'YearMonth'
}, inplace=True)
print(df_4m.info())
df_4m.to_excel('lead_4m.xlsx', index=False)

df_1m= df_2.merge(label_1m, on='RigDateID', how='inner')
# print(df_1m.info())
df_1m= df_1m.drop(['Rig_y', 'Year_y', 'Month_y', 'YearMonth_y'], axis=1)
df_1m.rename(columns={
    'Rig_x': 'Rig',
    'Year_x': 'Year',
    'Month_x': 'Month',
    'YearMonth_x': 'YearMonth'
}, inplace=True)
print(df_1m.info())
df_1m.to_excel('lead_1m.xlsx', index=False)