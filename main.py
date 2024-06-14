import streamlit as st
import numpy as np
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
from streamlit_folium import st_folium

st.title('Serie A 2023-2024')

# 定义转换函数
def dms_string_to_decimal(coord_str):
    def dms_to_decimal(d, m=0, s=0):
        return d + (m / 60.0) + (s / 3600.0)
    
    parts = coord_str.replace('°', ' ').replace('′', ' ').replace('″', '').replace('N', '').replace('E', '').strip().split(',')
    lat_dms = parts[0].strip().split()
    lon_dms = parts[1].strip().split()
    
    lat_deg = int(lat_dms[0])
    lat_min = int(lat_dms[1]) if len(lat_dms) > 1 else 0
    lat_sec = float(lat_dms[2]) if len(lat_dms) > 2 else 0
    
    lon_deg = int(lon_dms[0])
    lon_min = int(lon_dms[1]) if len(lon_dms) > 1 else 0
    lon_sec = float(lon_dms[2]) if len(lon_dms) > 2 else 0
    
    lat = np.float64(dms_to_decimal(lat_deg, lat_min, lat_sec))
    lon = dms_to_decimal(lon_deg, lon_min, lon_sec)
    
    return lat, lon

# 读取文件
df = pd.read_csv('Serie A 2023-2024.csv')

st.dataframe(df)

# 创建 POI 点矢量要素图层
feature_group = folium.FeatureGroup(name="Teams")

# 提取所有坐标点并计算边界
coords_list = []
for coords in df['Coordinates']:
    lat, lon = dms_string_to_decimal(coords)
    coords_list.append([lat, lon])
    folium.Marker(
        location=[lat, lon],
        popup=f"{df.loc[df['Coordinates'] == coords, 'Team'].values[0]}"
    ).add_to(feature_group)

# 计算边界框
bounds = [[min([c[0] for c in coords_list]), min([c[1] for c in coords_list])],
          [max([c[0] for c in coords_list]), max([c[1] for c in coords_list])]]

# 创建地图对象
m = folium.Map(zoom_start=11, tiles=None)

# 创建三个 Tile（地图切片）图层
tile_layers = {
    "Esri全球影像": "Esri.WorldImagery",
    "Carto地图": "CartoDB.Positron",
}

for name, tile in tile_layers.items():
    if "Carto地图" in name:
        folium.TileLayer(
            tile, 
            name=name,
            attr='Carto地图'
        ).add_to(m)
    elif "Esri全球影像" in name:
        folium.TileLayer(
            tile, 
            name=name,
            attr='Esri全球影像'
        ).add_to(m)


# 设置地图边界框
m.fit_bounds(bounds)

feature_group.add_to(m)

# 创建图层控制控件并添加到地图控件中
folium.LayerControl().add_to(m)

# 创建显示坐标控件并添加到地图控件中
MousePosition().add_to(m)

st_folium(m, width=700, height=500)

