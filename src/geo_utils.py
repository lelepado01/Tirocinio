
import geopandas as gp
import pandas as pd
import contextily as cx
import matplotlib.pyplot as plt

# La funzione è usata per eseguire selezioni su dataframe contenenti POINT()
# in base a bounds passati per argomento
# data[remove_points_out_of_range(data['field'], BOUNDS)]
# restituisce una serie pd.Series<Boolean> 
def remove_points_out_of_range(geodf : gp.GeoDataFrame, bounds) -> pd.Series: 
    res_ls = []
    for pointstr in geodf: 
        res_ls.append(
            point_is_in_range(
                parse_geojson_point(pointstr), 
                bounds
                ))
    return pd.Series(res_ls)

# Controlla se un punto è all'interno dei bounds
def point_is_in_range(point, bounds) -> bool:
    point_x, point_y = point
    return not (point_y > bounds[0] or point_y < bounds[1] or point_x < bounds[2] or point_x > bounds[3])

# Controlla se ogni punto della linea è nei bounds
def line_is_in_range(lines, bounds) -> bool:
    for point in parse_geojson_linestring(lines): 
        if not point_is_in_range(point, bounds): 
            return False

    return True

# La funzione è da usare per eseguire selezioni su dataframe contenenti LINESTRING()
# in base ai BOUNDS
# data[remove_lines_out_of_range(data['field'], BOUNDS)]
# restituisce una serie -> pd.Series<Boolean> 
def remove_lines_out_of_range(geodf : gp.GeoDataFrame, bounds) -> pd.Series: 
    res_ls = []
    for line in geodf: 
        res_ls.append(line_is_in_range(line, bounds))

    return pd.Series(res_ls)

# Converte una stringa in formato LINESTRING(x1 y1, x2 y2...)
# in una lista di tuple [(x1, y1), (x2, y2), ...] 
def parse_geojson_linestring(linestr) -> list: # -> return LIST<(double, double)>
    # prendo tutti i valori tranne il primo, che è la stringa LINESTRING(
    # e la parentesi finale 
    value_list = str(linestr)[12:][:-1].split(", ")
    
    tuple_list = []
    for val in value_list: 
        # aggiungo i punti come tuple (tutti quelli della linea)
        x, y = val.split(" ")
        tuple_list.append((float(x), float(y)))
    
    return tuple_list

# Converte una stringa in formato POINT(x y) in una tupla (x, y)
def parse_geojson_point(point) -> tuple: # -> return (float, float)
    # la struttura è POINT(x, y), devo eliminare la stringa POINT( e la parentesi finale
    value_list = str(point)[7:][:-1].split(" ")
    return (float(value_list[0]), float(value_list[1]))

def parse_geojson_point_list(point_list : list) -> list: 
    res = []
    for point in point_list: 
        res.append(parse_geojson_point(point))

    return res


def convert_geometry(geometry) -> list: 
    res = []
    for row in geometry: 
        data = str(row)[7:][:-1].split(" ")
        res.append((float(data[0]), float(data[1])))

    return res


# Converto a lista di punti tutte le righe del dataframe
def convert_to_Point(df : gp.GeoDataFrame, base : int) -> list:
    res = []
    for long, lat in convert_geometry(df['geometry']): 
        res.append(Point(long, lat).mult(base))

    return res

# Small class used for the following functions
class Point: 
    def __init__(self, x, y): 
        self.pos_x : float = x
        self.pos_y : float = y

    def mult(self, mult: int): 
        self.pos_x *= mult
        self.pos_y *= mult
        return self

    def get(self, coord : int): 
        if coord == 0: 
            return self.pos_x
        elif coord == 1: 
            return self.pos_y 
        return None   

    def print(self): 
        print("POINT(" + str(self.pos_x) + ", " + str(self.pos_y) + ")")

# The function returns, from the given list of points, eighter the first (x) column
# or the second (y) 
def get_coords_column(point_list : list, col : int) -> list:
    res = []
    for point in point_list: 
        res.append(point.get(col))
    return res 
    
# The function prints a map using the given bounds
def print_zoomed_graph(data : gp.GeoDataFrame, bounds : list, label=""): 
    ax = data.plot(figsize=(11,9), alpha=0.5)
    ax.set_title(label)
    ax.set_xlim([bounds[0], bounds[1]])
    ax.set_ylim([bounds[2], bounds[3]])
    cx.add_basemap(ax, crs=data.crs.to_string(), zoom=14)
    plt.show()
