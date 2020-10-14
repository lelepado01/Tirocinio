
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

import sys
sys.path.append('src')

import geo_utils

#def plot_geolocation_by_cluster(df, 
#                                cluster=None, 
#                                title=None, 
#                                centers=None,
#                                filename=None):
#    '''
#    Function to plot latitude and longitude coordinates
#    #####################
#    Args:
#        df: pandas dataframe 
#            Contains id, latitude, longitude, and color (optional).
#        cluster: (optional) column (string) in df 
#            Separate coordinates into different clusters
#        title: (optional) string
#        centers: (optional) array of coordinates for centers of each cluster
#        filename: (optional) string  
#    #####################
#    Returns:
#        Plot with lat/long coordinates 
#    '''
#    
#    # Transform df into geodataframe
#    geo_df = gpd.GeoDataFrame(df.drop(['longitudin', 'latitudine'], axis=1),
#                           crs={'init': 'epsg:4326'},
#                           geometry=[Point(x, y) for x, y in zip(df.longitudin, df.latitudine)])
#      
#    # Set figure size
#    fig, ax = plt.subplots(figsize=(10,10))
#    ax.set_aspect('equal')
#    
#    # Import NYC Neighborhood Shape Files
#    #nyc_full = gpd.read_file('./shapefiles/neighborhoods_nyc.shp')
#    #nyc_full.plot(ax=ax, alpha=0.4, edgecolor='darkgrey', color='lightgrey', label=nyc_full['boro_name'], zorder=1)
#    
#    # Plot coordinates from geo_df on top of NYC map
#    if cluster is not None:
#        geo_df.plot(ax=ax, column=cluster, alpha=0.5, 
#                    cmap='viridis', linewidth=0.8, zorder=2)
#        
#        if centers is not None:
#            centers_gseries = GeoSeries(map(Point, zip(centers[:,1], centers[:,0])))
#            centers_gseries.plot(ax=ax, alpha=1, marker='X', color='red', markersize=100, zorder=3)
#        
#        plt.title(title)
#        plt.xlabel('longitude')
#        plt.ylabel('latitude')
#        plt.show()
#        
#        if filename is not None:
#            fig.savefig(f'{filename}', bbox_inches='tight', dpi=300)
#    else:
#        geo_df.plot(ax=ax, alpha=0.5, cmap='viridis', linewidth=0.8, legend=True, zorder=2)
#        
#        plt.title(title)
#        plt.xlabel('longitude')
#        plt.ylabel('latitude')
#        plt.show()
#        
#    fig.clf()
#    
#df = gpd.read_file("dataset/incidenti/inc_strad_milano_2016.geojson")
#print(df)
#plot_geolocation_by_cluster(df)

# L'unica funzione che ho trovato per la creazione di un 'bubblechart' è questa,
# che non sembra funzionare per problemi (probabilmente) di versione di python 
# Decido di creare una mia versione

# Prima di tutto ho bisogno di una funzione che restituisca la distanza tra due punti,
# il centro e un dato.
import math

# Non voglio passare tuple alla funzione, preferisco avere un oggetto Point

def distance_between(p1 : geo_utils.Point, p2 : geo_utils.Point) -> float: 
    return math.sqrt(pow(p1.pos_x - p2.pos_x, 2) + pow(p1.pos_y - p2.pos_y, 2))

def get_points_close_to(centers : list, points : list, max_dist : float): 
    res = []
    for center in centers: 
        num = 0
        for point in points: 
            if distance_between(center, point) < max_dist: 
                num += 1

        res.append(num)
    
    return res

data = gpd.read_file("dataset/incidenti/inc_strad_milano_2016.geojson").to_crs(epsg=3857)
BASE = pow(10, 6)
points = geo_utils.convert_to_Point(data, BASE)

# Uso per provare qualche centro
centers = [
    geo_utils.Point(5.692, 1.020).mult(BASE), 
    geo_utils.Point(5.695, 1.025).mult(BASE), 
    geo_utils.Point(5.700, 1.035).mult(BASE), 
    geo_utils.Point(5.700, 1.020).mult(BASE)
]

#for center in centers: 
#    points[4].print()
#    print(distance_between(center, points[4]))

# Voglio creare un dataframe che contenga la posizione dei centri, e il numero di punti vicini
# a ognuno

DISTANCE_RANGE = 5776156660000.0

# lista con numero di punti vicini
points_close = get_points_close_to(centers, points, DISTANCE_RANGE)

distance = gpd.GeoDataFrame(
    points_close, 
    geometry = gpd.points_from_xy(
        geo_utils.get_coords_column(centers, 1), 
        geo_utils.get_coords_column(centers, 0), 
        crs=3857), 
    columns=['points_close']
    )

print(distance)

datal = data.plot(alpha=0.01, figsize=(11,9))
ax = distance.plot(ax=datal, markersize="points_close", alpha=0.8)
cx.add_basemap(ax=ax)
plt.show()

# Non sono sicuro che la misura della distanza funzioni,
# Ho sbagliato qualcosa nella misurazione delle coordinate dei centri rispetto a quelle 
# dei punti 