import folium
import pandas as pd
import pyproj

#create dataset
data = {'y': [67480.7, 67500.7, 67520.5],
        'x': [220850.6, 220868.4, 220888.7]}

df = pd.DataFrame(data)


# proj4 string
p = pyproj.Proj("+proj=lcc +lat_1=51.16666723333333 +lat_2=49.8333339 +lat_0=90 +lon_0=4.367486666666666 +x_0=150000.013 +y_0=5400088.438 +ellps=intl +towgs84=-99.059,53.322,-112.486,0.419,-0.830,1.885,-1")


def convert_to_LatLon(df, p):
    lon, lat = p(df['x'], df['y'], inverse=True)
    df['lat'] = lat
    df['lon'] = lon
    return df

df = df.apply(convert_to_LatLon, p=p, axis=1)
df.head()

# change location and zoom accordingly
m =folium.Map(location=[49.914623, 5.355284], zoom_start=16, max_zoom=25)
for index, row in df.iterrows():
    lat, lon = row[['lat', 'lon']]
    folium.CircleMarker(
        radius=5,
        location=[lat, lon],
        popup=index,
        color='crimson',
        fill=False,
    ).add_to(m)
m