
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("dataset/incidenti/aci/autostrade/comuni_2018.csv")
fields = ['INC', 'FER']

def sum_field_by_column(data, select, field_to_sum1, field_to_sum2): 
    dic = {}
    for f in data[select].unique(): 
        dic[f] = [
            data[data[select] == f][field_to_sum1].sum(), 
            data[data[select] == f][field_to_sum2].sum()
            ]

    return pd.DataFrame(dic)

provincia = sum_field_by_column(data, 'PROVINCIA', fields[0], fields[1]).transpose()

provincia = provincia.sort_values(by=0).head(20).sort_index()
plt.fill_between(provincia.index, provincia[1],label='Feriti', color='#71ceaf')
plt.fill_between(provincia.index, provincia[0], label='Incidenti', color='#7190ce')
plt.legend()
plt.xticks(range(0,20), provincia.index, rotation=90)
plt.ylabel("Numero di incidenti e feriti (2018)")
plt.tight_layout()
plt.show()