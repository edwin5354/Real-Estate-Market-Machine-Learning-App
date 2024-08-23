import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('./cleaned.csv')

# Correlation Matrix
corr_df = df[['num_room', 'age', 'sa', 'gfa', 'convenience', 'price']]
corr_matrix = corr_df.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', mask=mask, linewidths=.8, cmap='coolwarm')
plt.title('Correlation Matrix of Real Estate Offers')
plt.show()

# Boxplot --> Price Distribution
sns.boxplot(data= df, x = df['price'], y = df['region'], showfliers=False, fill=False)
plt.title('Real Estate Price')
plt.xlabel('Price in millions ($)')
plt.ylabel('Region')

# Number of real estates for each region
region_count = df.groupby('region').size().reset_index(name='count')
sns.barplot(x = 'region',y = 'count', data = region_count, edgecolor='black')
plt.title('Number of real estates')
plt.ylabel('Frequency')
plt.xlabel('Region')

# Seaborn pairplot
new_df = df[['sa', 'gfa', 'num_room', 'region']]
sns.pairplot(new_df, hue ='region')
