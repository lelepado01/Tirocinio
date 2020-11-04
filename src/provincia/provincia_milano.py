
import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt

data = gp.read_file("dataset/regioni/provincia.geojson").to_crs(epsg=3857)

# print(data[data['prov_acr'] == 'MI'])
lombardia = data[data['reg_istat_code_num'] == 3]
# lombardia.plot()
# plt.show()

# incidenti = pd.read_csv("dataset/incidenti/aci/autostrade/comuni_2011.csv")
incidenti = pd.read_csv("dataset/incidenti/aci/strade_provinciali/aci_2011.csv")
incidenti_lombardia = incidenti[incidenti['REGIONE'] == 'Lombardia']

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


incidenti_lombardia = gp.GeoDataFrame(get_sum_of_fields(incidenti_lombardia, 'provincia', 'Inc'))

incidenti_lombardia = lombardia.merge(incidenti_lombardia, left_on='prov_name', right_on='provincia')

from matplotlib.lines import Line2D

incidenti_lombardia.plot(column='Inc', cmap='OrRd')
plt.legend([
    Line2D([],[],color='#84190f',linewidth=5), 
    Line2D([],[],color='#ef5547',linewidth=5), 
    Line2D([],[],color='#efd4ae',linewidth=5)
], [max(incidenti_lombardia['Inc']), int(incidenti_lombardia['Inc'].mean()), min(incidenti_lombardia['Inc'])])
plt.axis('off')
plt.show()