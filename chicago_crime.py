import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import calendar
import numpy as np

crimes = pd.read_csv("Chicago_Crimes_2012_to_2017.csv");
crimes.head(2)

crimes = crimes[(crimes['Year'] == 2016) | (crimes['Year'] == 2015)]
crimes['Date'] = pd.to_datatime(crimes['Date'], format='%m/%d/%Y %I:%M:%S %p')

crimes['Month'] = (crimes['Date'].dt.month).apply(lambda x: calendar.month_abbr[x])

crimes['Month'] = pd.Categorical(crimes['Month'], categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

crimes["Weekday"] = crimes['Data'].dt.weekday_name
crimes['Weekday'] = pd.Categorical(crimes['Weekday'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
crimes.head()

sns.countplot(x='Year', data=crimes)
plt.ylabel('No of Crimes')
plt.show()

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
crimes.groupby('Month')['ID'].count().plot(marker='o')
plt.xticks(np.arange(12), months)
plt.ylabel('No of Crimes')
plt.show()