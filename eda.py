
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy import stats
from scipy.stats import mannwhitneyu

# Load the Excel files
file1_path = 'all_1m.xlsx'
file2_path = 'all_4m.xlsx'
file3_path = 'lead_1m.xlsx'
file4_path = 'lead_4m.xlsx'


# Read the Excel files 
df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)
df3 = pd.read_excel(file3_path)
df4 = pd.read_excel(file4_path)

# print(df2.info())

features=['Normalized_Cards',
    'Unsafe_Action',
    'Unsafe_Condition',
    'Unsafe_Condition_Cor',
    'Positive_Observation',
    'Negative_Observation',
    'Active_Action_Taken',
    'Low_Risk',
    'Medium_Risk',
    'High_Risk',
    'RollingPositionStability',
    'RollingRigStability',
    'RollingCrewStability',
    'Normalized_Cards_Alpha',
    'Normalized_Cards_Beta'
]
labels1m=[
    'All_TotalEvents',
    'All_RiskCalculatedValue',
    'All_ActualSeverity',
    'Con_TotalEvents',
    'Con_RiskCalculatedValue',
    'Con_ActualSeverity',
    'Miss_TotalEvents'
    ,'Miss_RiskCalculatedValue',
    'Miss_ActualSeverity'
]
labels4m=[
   'All_TotalEvents_4M',
   'All_RiskCalculated_4M',
   'All_ActualSeverity_4M',
   'Con_TotalEvents_4M',
   'Con_RiskCalculated_4M',
   'Con_ActualSeverity_4M',
   'Miss_TotalEvents_4M'
   ,'Miss_RiskCalculated_4M',
   'Miss_ActualSeverity_4M'
]

# print(df1['Rig'].nunique())

colors = sns.color_palette("Reds", 3)

# Show the summary statistics of safety features
# print(df1[features].describe().transpose())
# print(df3[features].describe().transpose())



# # Create heatmaps
# corr1 = df1[features].corr()
# corr2 = df3[features].corr()

# plt.figure(figsize=(14, 12))
# plt.rcParams['font.family'] = 'Times New Roman'
# cmap = sns.color_palette("Reds", as_cmap=True)
# sns.heatmap(corr2, annot=True, fmt='.2f', cmap=cmap, linewidths=0.5, annot_kws={"size": 10, "fontfamily": "Times New Roman"},cbar=False)
# plt.xticks(fontsize=12, fontname='Times New Roman')
# plt.yticks(fontsize=12, fontname='Times New Roman')
# plt.show()



# Draw the boxplot of safety features
df1_melted = df1.melt(value_vars=['Low_Risk', 'Medium_Risk', 'High_Risk'],
                      var_name='Risk_Level', value_name='Cards Percentage')
df3_melted = df3.melt(value_vars=['Low_Risk', 'Medium_Risk', 'High_Risk'],
                      var_name='Risk_Level', value_name='Cards Percentage')

fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

# Plot for All Employees
sns.boxplot(x='Risk_Level', y='Cards Percentage', data=df1_melted, ax=axes[0], palette=colors)
axes[0].set_title('All Employees', fontsize=16, fontname='Times New Roman')
axes[0].set_xlabel('')
axes[0].set_ylabel('Cards Percentage', fontsize=14, fontname='Times New Roman')
axes[0].tick_params(axis='both', which='major', labelsize=12)
for label in axes[0].get_xticklabels():
    label.set_fontname('Times New Roman')
for label in axes[0].get_yticklabels():
    label.set_fontname('Times New Roman')

# Annotate the boxes for All Employees
risk_levels = df1_melted['Risk_Level'].unique()
for i, level in enumerate(risk_levels):
    med = round(df1_melted[df1_melted['Risk_Level'] == level]['Cards Percentage'].median(), 2)
    axes[0].text(i, med, f'{med:.2f}', ha='center', va='center', fontsize=10, color='white', fontname='Times New Roman')

# Plot for Rig Leaders
sns.boxplot(x='Risk_Level', y='Cards Percentage', data=df3_melted, ax=axes[1], palette=colors)
axes[1].set_title('Rig Leaders', fontsize=16, fontname='Times New Roman')
axes[1].set_xlabel('')
axes[1].set_ylabel('Cards Percentage', fontsize=14, fontname='Times New Roman')
axes[1].tick_params(axis='both', which='major', labelsize=12)
for label in axes[1].get_xticklabels():
    label.set_fontname('Times New Roman')
for label in axes[1].get_yticklabels():
    label.set_fontname('Times New Roman')

# Annotate the boxes for Rig Leaders
for i, level in enumerate(risk_levels):
    med = round(df3_melted[df3_melted['Risk_Level'] == level]['Cards Percentage'].median(), 2)
    axes[1].text(i, med, f'{med:.2f}', ha='center', va='center', fontsize=10, color='white', fontname='Times New Roman')

plt.tight_layout()
plt.show()


# Draw the barplot of safety incidents by consequence type

# incident_counts_1_month = {
#     'All Incidents': df1['All_TotalEvents'].sum(),
#     'Incidents With Consequence': df1['Con_TotalEvents'].sum(),
#     'Incidents Without Consequence': df1['Miss_TotalEvents'].sum()
# }
# incident_counts_4_months = {
#     'All Incidents': df2['All_TotalEvents_4M'].sum(),
#     'Incidents With Consequence': df2['Con_TotalEvents_4M'].sum(),
#     'Incidents Without Consequence': df2['Miss_TotalEvents_4M'].sum()
# }

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# ax1.bar(incident_counts_1_month.keys(), incident_counts_1_month.values(), color=colors)
# ax1.set_title('1 Month Data', fontname='Times New Roman')
# ax1.set_xlabel('')
# ax1.set_ylabel('Count of Incidents', fontname='Times New Roman')
# ax1.tick_params(axis='both', which='major', labelsize=10)
# for label in ax1.get_xticklabels():
#     label.set_fontname('Times New Roman')
# for label in ax1.get_yticklabels():
#     label.set_fontname('Times New Roman')

# # Plot for 4 months data
# ax2.bar(incident_counts_4_months.keys(), incident_counts_4_months.values(), color=colors)
# ax2.set_title('4 Months Data', fontname='Times New Roman')
# ax2.set_xlabel('')
# ax2.set_ylabel('Count of Incidents', fontname='Times New Roman')
# ax2.tick_params(axis='both', which='major', labelsize=10)
# for label in ax2.get_xticklabels():
#     label.set_fontname('Times New Roman')
# for label in ax2.get_yticklabels():
#     label.set_fontname('Times New Roman')

# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.show()





# Boxplot of safety features by Total Events

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
# # Plot for 1-month data
# sns.boxplot(data=df1[['All_TotalEvents', 'Con_TotalEvents', 'Miss_TotalEvents']], ax=ax1, palette=colors[::-1])
# ax1.set_title('1 Month Data', fontname='Times New Roman')
# ax1.set_xlabel('')
# ax1.set_ylabel('Count of Normalized Events', fontname='Times New Roman')
# ax1.tick_params(axis='both', which='major', labelsize=10)
# for label in ax1.get_xticklabels():
#     label.set_fontname('Times New Roman')
# for label in ax1.get_yticklabels():
#     label.set_fontname('Times New Roman')
# # Plot for 4-months data
# sns.boxplot(data=df2[['All_TotalEvents_4M', 'Con_TotalEvents_4M', 'Miss_TotalEvents_4M']], ax=ax2, palette=colors[::-1])
# ax2.set_title('4 Months Data', fontname='Times New Roman')
# ax2.set_xlabel('')
# ax2.set_ylabel('Count of Normalized Events', fontname='Times New Roman')
# ax2.tick_params(axis='both', which='major', labelsize=10)
# for label in ax2.get_xticklabels():
#     label.set_fontname('Times New Roman')
# for label in ax2.get_yticklabels():
#     label.set_fontname('Times New Roman')

# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.show()

# show1m=labels1m+['RigDateID','TotalManhours']
# top_5=df1[show1m].set_index('RigDateID').nlargest(5, 'All_TotalEvents').transpose()
# print(top_5)



# Boxplot of safety features by Actual Severity

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
# # Plot for 1-month data
# sns.boxplot(data=df1[['All_ActualSeverity', 'Con_ActualSeverity', 'Miss_ActualSeverity']], ax=ax1, palette=colors[::-1])
# ax1.set_title('1 Month Data', fontname='Times New Roman')
# ax1.set_xlabel('')
# ax1.set_ylabel('Normalized Severity', fontname='Times New Roman')
# ax1.tick_params(axis='both', which='major', labelsize=10)
# for label in ax1.get_xticklabels():
#     label.set_fontname('Times New Roman')
# for label in ax1.get_yticklabels():
#     label.set_fontname('Times New Roman')
# # Plot for 4-months data
# sns.boxplot(data=df2[['All_ActualSeverity_4M', 'Con_ActualSeverity_4M', 'Miss_ActualSeverity_4M']], ax=ax2, palette=colors[::-1])
# ax2.set_title('4 Months Data', fontname='Times New Roman')
# ax2.set_xlabel('')
# ax2.set_ylabel('Normalized Severity', fontname='Times New Roman')
# ax2.tick_params(axis='both', which='major', labelsize=10)
# for label in ax2.get_xticklabels():
#     label.set_fontname('Times New Roman')
# for label in ax2.get_yticklabels():
#     label.set_fontname('Times New Roman')

# plt.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.show()

# show1m=labels1m+['RigDateID','TotalManhours']
# top_5=df1[show1m].set_index('RigDateID').nlargest(5, 'All_ActualSeverity').transpose()
# print(top_5)




# Scatter plots of safety features vs Events

# features1 = [
#     'Normalized_Cards', 'Unsafe_Action', 'Unsafe_Condition', 'Unsafe_Condition_Cor',
#     'Positive_Observation', 'Negative_Observation', 'Active_Action_Taken',
#     'Low_Risk', 'Medium_Risk', 'High_Risk', 'RollingCrewStability',
#     'Normalized_Cards_Alpha', 'Normalized_Cards_Beta'
# ]
# event_columns = ['All_TotalEvents_4M', 'Con_TotalEvents_4M', 'Miss_TotalEvents_4M']

# for feature in features:
#     fig, axes = plt.subplots(1, 3, figsize=(18, 7))
    
#     for i, event_col in enumerate(event_columns):
#         ax = axes[i]
#         sns.scatterplot(x=df2[feature], y=df2[event_col], color='#FF3333', label='All Employees', ax=ax)
#         sns.scatterplot(x=df4[feature], y=df4[event_col], color='#FFA5A5', label='Rig Leaders', ax=ax)
        
#         # Add trend lines
#         z2 = np.polyfit(df2[feature], df2[event_col], 1)
#         p2 = np.poly1d(z2)
#         ax.plot(df2[feature], p2(df2[feature]), color='#FF3333', linestyle='dashed')
        
#         z4 = np.polyfit(df4[feature], df4[event_col], 1)
#         p4 = np.poly1d(z4)
#         ax.plot(df4[feature], p4(df4[feature]), color='#FFA5A5', linestyle='dashed')
        
#         ax.set_xlabel(feature, fontsize=12, fontname='Times New Roman')
#         ax.set_ylabel(event_col, fontsize=12, fontname='Times New Roman')
#         ax.grid(color='lightgray', linestyle='dashed')
#         ax.spines['top'].set_visible(False)
#         ax.spines['right'].set_visible(False)
#         ax.spines['left'].set_position('zero')
#         ax.spines['bottom'].set_position('zero')
#         ax.get_legend().remove()

#     legend_ax = fig.add_axes([0.1, 0.05, 0.8, 0.05])  
#     legend_ax.axis('off') 
#     handles, labels = ax.get_legend_handles_labels()
#     legend_ax.legend(handles, labels, loc='center right', fontsize=10, prop={'family': 'Times New Roman'}, ncol=2)

#     plt.tight_layout()
#     plt.subplots_adjust(bottom=0.2)
#     plt.rc('font', family='Times New Roman')
#     plt.show()


# top_5=df1.set_index('RigDateID').nlargest(5, 'All_TotalEvents').transpose()
# print(top_5)



#### Histograms of safety features
# from collections import Counter
# fi_file = 'WordsCloud.xlsx'
# All1m_fi = pd.read_excel(fi_file, sheet_name='all-1m').iloc[:-1, ]
# All4m_fi = pd.read_excel(fi_file, sheet_name='all-4m').iloc[:-1, ]
# lead1m_fi = pd.read_excel(fi_file, sheet_name='lead-1m').iloc[:-1, ]
# lead4m_fi = pd.read_excel(fi_file, sheet_name='lead-4m').iloc[:-1, ]

# feature_importance = All1m_fi.groupby('name')['fi'].sum().reset_index()
# import matplotlib.font_manager as fm
# # Convert the aggregated importance into a dictionary
# importance_dict = dict(zip(feature_importance['name'], feature_importance['fi']))
# # print(importance_dict)
# word_freq = Counter(importance_dict)
# sorted_items = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)
# features, importances = zip(*sorted_items)

# # Normalize the importances for color mapping
# norm = plt.Normalize(min(importances), max(importances))

# # Create a color map (red gradient)
# colors = plt.cm.Reds(norm(importances))

# # Plot the word cloud using matplotlib
# fig, ax = plt.subplots(figsize=(10, 5))
# bars = ax.barh(features, importances, color=colors)

# # Add a color bar
# sm = plt.cm.ScalarMappable(cmap='Reds', norm=norm)
# sm.set_array([])
# plt.colorbar(sm, orientation='vertical', label='Importance')

# ax.set_xlabel('Feature Importance')
# plt.gca().invert_yaxis()  # Invert y-axis to have the highest importance on top
# plt.show()




###  Statistical Tests

# alpha = 0.05
# fi_file = 'WordsCloud EDA.xlsx'
# All1m_fi = pd.read_excel(fi_file, sheet_name='all-1m').iloc[:, 1]
# All4m_fi = pd.read_excel(fi_file, sheet_name='all-4m').iloc[:, 1]
# lead1m_fi = pd.read_excel(fi_file, sheet_name='lead-1m').iloc[:, 1]
# lead4m_fi = pd.read_excel(fi_file, sheet_name='lead-4m').iloc[:, 1]

###  All Employees 1 month dataset
# Hypothesis 1: Beta feature

# all1m_beta = 0.0146086
# t_stat, p_value = stats.ttest_1samp(All1m_fi,all1m_beta)
# one_tailed_p_value = p_value / 2
# print(round(t_stat,5), round(one_tailed_p_value,10))

# if t_stat > 0 and one_tailed_p_value < alpha:
#     print("Reject the null hypothesis. The feature Beta's mean importance is statistically greater than the overall mean importance.")
# else:
#     print("Fail to reject the null hypothesis. The feature Beta's mean importance is not statistically greater than the overall mean importance.")
# # Hypothesis 2: crew stability feature
# all1m_crew = 0.0064326
# t_stat, p_value = stats.ttest_1samp(All1m_fi,all1m_crew)
# one_tailed_p_value = p_value / 2
# print(round(t_stat,5),round(one_tailed_p_value,10) )

# if t_stat > 0 and one_tailed_p_value < alpha:
#     print("Reject the null hypothesis. The feature Crew Stability's mean importance is statistically greater than the overall mean importance.")
# else:
#     print("Fail to reject the null hypothesis. The feature Crew Stability's mean importance is not statistically greater than the overall mean importance.")


###  All Employees 4 month dataset
# Hypothesis 1: Beta feature

# all4m_beta = 0.01877383
# t_stat, p_value = stats.ttest_1samp(All4m_fi,all4m_beta)
# one_tailed_p_value = p_value / 2
# print(round(t_stat,5), round(one_tailed_p_value,10))

# if t_stat > 0 and one_tailed_p_value < alpha:
#     print("Reject the null hypothesis. The feature Beta's mean importance is statistically greater than the overall mean importance.")
# else:
#     print("Fail to reject the null hypothesis. The feature Beta's mean importance is not statistically greater than the overall mean importance.")
# # Hypothesis 2: crew stability feature
# all4m_crew = 0.01174048
# t_stat, p_value = stats.ttest_1samp(All4m_fi,all4m_crew)
# one_tailed_p_value = p_value / 2
# print(round(t_stat,5),round(one_tailed_p_value,10) )

# if t_stat > 0 and one_tailed_p_value < alpha:
#     print("Reject the null hypothesis. The feature Crew Stability's mean importance is statistically greater than the overall mean importance.")
# else:
#     print("Fail to reject the null hypothesis. The feature Crew Stability's mean importance is not statistically greater than the overall mean importance.")


# # ###  Rig Leaders 1 month dataset
# # Hypothesis 1: Beta feature

# lead1m_beta = 0.0070185
# t_stat, p_value = stats.ttest_1samp(lead1m_fi,lead1m_beta)
# one_tailed_p_value = p_value / 2
# print(round(t_stat,5), round(one_tailed_p_value,10))

# if t_stat > 0 and one_tailed_p_value < alpha:
#     print("Reject the null hypothesis. The feature Beta's mean importance is statistically greater than the overall mean importance.")
# else:
#     print("Fail to reject the null hypothesis. The feature Beta's mean importance is not statistically greater than the overall mean importance.")
# # Hypothesis 2: crew stability feature
# lead1m_crew = 0.003094072
# t_stat, p_value = stats.ttest_1samp(lead1m_fi,lead1m_crew)
# one_tailed_p_value = p_value / 2
# print(round(t_stat,5),round(one_tailed_p_value,10) )

# if t_stat > 0 and one_tailed_p_value < alpha:
#     print("Reject the null hypothesis. The feature Crew Stability's mean importance is statistically greater than the overall mean importance.")
# else:
#     print("Fail to reject the null hypothesis. The feature Crew Stability's mean importance is not statistically greater than the overall mean importance.")



# # ###  Rig Leaders 4 month dataset
# # Hypothesis 1: Beta feature

# lead4m_beta = 0.00767572
# t_stat, p_value = stats.ttest_1samp(lead4m_fi,lead4m_beta)
# one_tailed_p_value = p_value / 2
# print(round(t_stat,5), round(one_tailed_p_value,10))

# if t_stat > 0 and one_tailed_p_value < alpha:
#     print("Reject the null hypothesis. The feature Beta's mean importance is statistically greater than the overall mean importance.")
# else:
#     print("Fail to reject the null hypothesis. The feature Beta's mean importance is not statistically greater than the overall mean importance.")
# # Hypothesis 2: crew stability feature
# lead4m_crew= 0.00493983
# t_stat, p_value = stats.ttest_1samp(lead4m_fi,lead4m_crew)
# one_tailed_p_value = p_value / 2
# print(round(t_stat,5),round(one_tailed_p_value,10) )

# if t_stat > 0 and one_tailed_p_value < alpha:
#     print("Reject the null hypothesis. The feature Crew Stability's mean importance is statistically greater than the overall mean importance.")
# else:
#     print("Fail to reject the null hypothesis. The feature Crew Stability's mean importance is not statistically greater than the overall mean importance.")



# ##### Mann-Whitney U test for hypothesis 3 testing 
# def cohen_d(x, y):
#     nx = len(x)
#     ny = len(y)
#     dof = nx + ny - 2
#     pooled_std = np.sqrt(((nx - 1) * np.std(x, ddof=1) ** 2 + (ny - 1) * np.std(y, ddof=1) ** 2) / dof)
#     return (np.mean(x) - np.mean(y)) / pooled_std
# # For 1-month
# #R-square
# all_r_1m = [
#     0.4236623, 0.6774305, 0.3579128, 0.3684656, 0.2301943, -0.0537363, 0.1741571, 0.1431324, 0.0419010,
#     0.4081940, 0.5893732, 0.3624806, 0.2409700, 0.2243122, 0.0603109, 0.2235147, 0.1494248, 0.0745416,
#     0.1266282, 0.1157722, 0.07100486, 0.0077407, 0.0490374, -0.0044220, 0.0711587, 0.0474575, 0.0197588,
#     0.1318222, -0.1223182, -0.2525878, 0.0192630, -0.2911439, -0.4215507, -0.3030213, -0.2852036, -0.3356899,
#     0.3894590, 0.3149233, 0.09272945, 0.1824605, -0.01599179, 0.0230394, 0.002143909, -0.3016403, -0.003952498
# ]

# lead_r_1m = [
#     0.2922584, 0.5121627, 0.2913331, 0.1512582, 0.5258551, 0.5102069, 0.1885103, 0.2178332, 0.07198409,
#     0.1612816, 0.4311065, 0.2450115, 0.0735462, 0.1549769, 0.06847654, 0.3073466, 0.1619076, 0.1105185,
#     0.03350643, 0.1143806, 0.0725066, 0.01083931, 0.05991363, 0.04220908, 0.0697272, 0.0407493, 0.01667024,
#     0.02369325, -0.04562514, -0.1358338, 0.007117437, -0.1545597, -0.2125321, -0.1515873, -0.1548015, -0.1738569,
#     0.3425491, 0.05278453, -0.04609544, 0.1096951, 0.06484944, 0.02255941, 0.07336587, 0.02145608, -0.3317735
# ]
# u_stat, p_value = mannwhitneyu(lead_r_1m, all_r_1m, alternative='greater')

# print(f"Mann-Whitney U statistic: {u_stat}")
# print(f"P-value: {p_value}")

# if p_value < 0.05:
#     print("The R^2 values for rig leaders are significantly higher.")
# else:
#     print("The R^2 values for rig leaders are not significantly higher.")
# effect_size = cohen_d(lead_r_1m, all_r_1m)
# print(f"Effect size (Cohen's d): {effect_size}")

# # RMSE
# all_rmse_1m = [
#     0.0890441, 0.0532395, 0.0624456, 0.0814708, 0.0696178, 0.0686630, 0.0690405, 0.0705035, 0.0711364,
#     0.0902311, 0.0600684, 0.0622231, 0.0893168, 0.0698833, 0.0648409, 0.0669456, 0.0702442, 0.0699142,
#     0.1096141, 0.0881463, 0.07511243, 0.1021212, 0.0773769, 0.0670371, 0.0732194, 0.0743355, 0.0719537,
#     0.1092876, 0.0993071, 0.0872186, 0.1015266, 0.0901607, 0.0797514, 0.0867224, 0.0863456, 0.0839923,
#     0.1325912, 1.505024, 0.6610765, 0.06594023, 1.421267, 0.4186107, 0.03980881, 0.5173246, 1.322473]
# lead_rmse_1m = [
#     0.09867429, 0.06547262, 0.06560337, 0.09444767, 0.05463681, 0.04681266, 0.06843793, 0.06736025, 0.0700107,
#     0.1074174, 0.07070297, 0.0677135, 0.09867687, 0.07293972, 0.06455857, 0.06322857, 0.06972684, 0.06854175,
#     0.1153098, 0.08821568, 0.0750517, 0.1019617, 0.07693317, 0.06546246, 0.07327579, 0.07459678, 0.07206697,
#     0.1158937, 0.095854, 0.08305437, 0.1021533, 0.08525856, 0.07365523, 0.08152744, 0.08184793, 0.07873979,
#     0.1477101, 1.740797, 0.6897746, 0.06918467, 1.395934, 0.4163711, 0.03905946, 1.306228, 0.5160824
# ]
# u_stat, p_value = mannwhitneyu(lead_rmse_1m, all_rmse_1m, alternative='less')


# print(f"Mann-Whitney U statistic: {u_stat}")
# print(f"P-value: {p_value}")

# if p_value < 0.05:
#     print("The RMSE values for rig leaders are significantly lower than those for all employees.")
# else:
#     print("The RMSE values for rig leaders are not significantly lower than those for all employees.")

# effect_size = cohen_d(lead_rmse_1m, all_rmse_1m)
# print(f"Effect size (Cohen's d): {effect_size}")

# # For 4-month
# #R-square
# all_r_4m = [
#     0.6159904, 0.7354978, 0.6977803, 0.3567488, 0.5796847, 0.5963118, 0.7156192, 0.7741054, 0.4471862,
#     -0.1440404, -0.3647558, -0.2205072, -1.680155, -0.5169688, -0.2655748, -0.241222, -0.2113717, -0.2976118,
#     0.2081258, 0.07149244, 0.1737334, 0.04261688, 0.09008168, 0.2120719, 0.07949448, 0.03662765, 0.06318881,
#     0.4077942, 0.4758709, 0.5776002, -2.148323, -0.3397216, -0.1784295, 0.5478525, 0.7420639, 0.4917197,
#     0.7404861, 0.6113813, 0.6940697, 0.5193613, 0.5846216, 0.5420441, 0.72043, 0.7243671, 0.643262
# ]

# lead_r_4m = [
#     0.5080739, 0.6186049, 0.747243, 0.07000565, 0.3113489, 0.5405752, 0.6585385, 0.7485088, 0.5046229,
#     0.2494405, 0.3669455, 0.5962285, -0.3740529, 0.330809, 0.3118267, 0.6967905, 0.6958676, 0.4746759,
#     0.01130355, 0.05506855, 0.0818131, -0.1104365, 0.05481635, 0.1000717, 0.08636534, 0.05819379, 0.05368314,
#     -0.3894716, -0.3521746, -0.2002704, -2.016651, -0.463359, -0.2290543, -0.2013738, -0.182299, -0.2205289,
#     0.3575428, 0.5552788, 0.613614, 0.2767147, 0.4498078, 0.4982471, 0.6093062, 0.4951589, 0.478667
# ]
# u_stat, p_value = mannwhitneyu(lead_r_4m, all_r_4m, alternative='greater')

# print(f"Mann-Whitney U statistic: {u_stat}")
# print(f"P-value: {p_value}")

# if p_value < 0.05:
#     print("The R^2 values for rig leaders are significantly higher.")
# else:
#     print("The R^2 values for rig leaders are not significantly higher.")
# effect_size = cohen_d(lead_r_4m, all_r_4m)
# print(f"Effect size (Cohen's d): {effect_size}")

# # RMSE
# all_rmse_4m = [
#     0.1213799, 0.8922599, 0.296901, 0.09140288, 0.7796161, 0.2834495, 0.01349584, 0.3566052, 0.1296394,
#     0.08306355, 0.07645063, 0.07468671, 0.05441597, 0.06839155, 0.06836778, 0.08818873, 0.09515003, 0.09099324,
#     0.06910634, 0.06305889, 0.0614516, 0.0325229, 0.05296821, 0.05394496, 0.07594541, 0.08485302, 0.07731482,
#     0.05976214, 0.04737756, 0.04393746, 0.05897746, 0.06427194, 0.06597196, 0.05322656, 0.04390624, 0.05694929,
#     0.03956126, 0.0407958, 0.03739249, 0.02304389, 0.03578789, 0.04112628, 0.04185368, 0.04538745, 0.04771022
# ]

# lead_rmse_4m = [
#     0.05446779, 0.04041486, 0.03398793, 0.03205432, 0.04608013, 0.04119219, 0.04625505, 0.04335425, 0.05622179,
#     0.06727944, 0.05206839, 0.0429577, 0.03896262, 0.04542439, 0.05041462, 0.04358728, 0.04767619, 0.05789624,
#     0.07721849, 0.06361415, 0.06477966, 0.03502622, 0.05398489, 0.05765163, 0.07566144, 0.08389789, 0.07770608,
#     0.09154078, 0.07609742, 0.07406494, 0.05773098, 0.0671722, 0.06737412, 0.08676157, 0.09400131, 0.0882492,
#     0.1560213, 1.329664, 0.4013298, 0.09820743, 1.053923, 0.3435024, 0.01671044, 0.5909758, 0.1472587
# ]
# u_stat, p_value = mannwhitneyu(lead_rmse_4m, all_rmse_4m, alternative='less')


# print(f"Mann-Whitney U statistic: {u_stat}")
# print(f"P-value: {p_value}")

# if p_value < 0.05:
#     print("The RMSE values for rig leaders are significantly lower than those for all employees.")
# else:
#     print("The RMSE values for rig leaders are not significantly lower than those for all employees.")

# effect_size = cohen_d(lead_rmse_4m, all_rmse_4m)
# print(f"Effect size (Cohen's d): {effect_size}")