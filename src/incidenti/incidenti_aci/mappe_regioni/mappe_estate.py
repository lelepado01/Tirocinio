
import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt

def get_sum_of_fields(data : pd.DataFrame, select_field : str, field_to_sum : str) -> pd.Series: 
    res = {}
    index = 0
    for reg in data[select_field].unique():
        res[index] = [reg, 0]
        index += 1

    index = 0
    for reg in data[select_field].unique():
        for row in data[data[select_field] == reg][field_to_sum]:
            res[index] = [res[index][0], res[index][1] + row]
        index += 1

    return pd.DataFrame(res, index=[select_field, field_to_sum]).transpose()

field_incidenti = 'Agosto'
path = "dataset/regioni/regioni.geojson"
regioni = gp.read_file(path)

data = pd.read_csv('dataset/incidenti/aci/autostrade/mesi_2014.csv')
#data = data[data['INC'] != '0,0'].astype({'INC': int})

# incidenti = get_sum_of_fields(data, 'REGIONE', field_incidenti)

# incidenti.index = incidenti['REGIONE']
# regioni.index = regioni['reg_name']
# # print(incidenti_2011)
# # print(regioni)

# regioni = gp.GeoDataFrame(incidenti[field_incidenti], geometry=regioni['geometry'].transpose())

# from matplotlib.lines import Line2D

# regioni.plot(column=field_incidenti, cmap='OrRd', legend=True)
# # plt.title("Incidenti per regione nel 2014")
# plt.axis('off')
# plt.legend([
#     Line2D([],[],color='#a52317',linewidth=5), 
#     Line2D([],[],color='#d6584d',linewidth=5), 
#     Line2D([],[],color='#f7aca5',linewidth=5)
# ], [max(regioni[field_incidenti]), '1000', min(regioni[field_incidenti])])
# plt.show()

agosto = get_sum_of_fields(data, 'REGIONE', 'Agosto')
gennaio = get_sum_of_fields(data, 'REGIONE', 'Gennaio')

agosto.index = agosto['REGIONE']
gennaio.index = gennaio['REGIONE']
agosto = agosto['Agosto']
gennaio = gennaio['Gennaio']

plt.bar(agosto.index, agosto, label='Agosto',  color='#d8758c')
plt.bar(gennaio.index, gennaio, label='Gennaio', alpha=0.9, color='#75d8c1')
plt.xticks(rotation=90)
plt.ylabel("Incidenti al mese (2014)")
plt.legend()
plt.tight_layout()
plt.show()