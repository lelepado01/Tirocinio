
import pandas as pd
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv("dataset/area_c/orari_2016.csv", sep=';').dropna()
orari_serali = data[(data['hour'] != 25) & (data['hour'] >= 23) | (data['hour'] <=6)] 

def is_weekend(year, month, day) -> pd.Series: 
    s = pd.Series()

    for y, m, d in zip(year, month, day): 
        s = s.append(pd.Series(datetime.datetime(y, m, d).weekday() > 4), ignore_index=True)

    return s

weekend_days = orari_serali
week_days = orari_serali
days = is_weekend(orari_serali['year'], orari_serali['month'], orari_serali['day'])

weekend_days.index = range(0, len(weekend_days))
week_days.index = range(0, len(week_days))

i = 0
for d in days: 
    if not d: 
        weekend_days = weekend_days.drop(index=i)
    else: 
        week_days = week_days.drop(index=i)
    i+= 1

traffico_weekend = {}
for f in weekend_days['hour'].unique():
    traffico_weekend[f] = weekend_days[weekend_days['hour'] == f]['totale'].sum()

traffico_weeke = {}
for f in weekend_days['hour'].unique():
    traffico_weeke[f] = week_days[week_days['hour'] == f]['totale'].sum()

traffico_weekend = pd.DataFrame(traffico_weekend, index=['Traffico nel weekend']).transpose()
traffico_week = pd.DataFrame(traffico_weeke, index=['Traffico in settimana']).transpose()

traffico_weekend /= 2 * 52
traffico_week /= 5 * 52

traffico_weekend = traffico_weekend.reindex([23,0,1,2,3,4,5,6])
traffico_week = traffico_week.reindex([23,0,1,2,3,4,5,6])

traffico_weekend['Traffico in settimana'] = traffico_week['Traffico in settimana']
traffico_weekend.plot.bar(width=0.9, color=['#6262d1', '#d1d162'])
plt.ylabel("Accessi in area C per giorno")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
