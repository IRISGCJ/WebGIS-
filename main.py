import streamlit as st
import numpy as np
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MousePosition
from streamlit_folium import st_folium

# 定义转换函数
def dms_string_to_decimal(coord_str):
    def dms_to_decimal(d, m=0, s=0):
        return d + (m / 60.0) + (s / 3600.0)
    
    parts = coord_str.strip().split(', ')
    lat_dms = parts[0].replace('°', ' ').replace('′', ' ').replace('″', '').replace('N', '').replace('S', '').strip().split()
    lon_dms = parts[1].replace('°', ' ').replace('′', ' ').replace('″', '').replace('E', '').replace('W', '').strip().split()
    
    lat_deg = int(lat_dms[0])
    lat_min = int(lat_dms[1]) if len(lat_dms) > 1 else 0
    lat_sec = float(lat_dms[2]) if len(lat_dms) > 2 else 0
    lat_dir = parts[0][-1]

    lon_deg = int(lon_dms[0])
    lon_min = int(lon_dms[1]) if len(lon_dms) > 1 else 0
    lon_sec = float(lon_dms[2]) if len(lon_dms) > 2 else 0
    lon_dir = parts[1][-1]
    
    lat = np.float64(dms_to_decimal(lat_deg, lat_min, lat_sec))
    lon = dms_to_decimal(lon_deg, lon_min, lon_sec)
    
    if lat_dir == 'S':
        lat = -lat
    if lon_dir == 'W':
        lon = -lon
    
    return lat, lon

st.title('Football Leagues 2023-2024')

# 让用户选择联赛
league_options = ['Premier League', 'Serie A']
league_choice = st.selectbox('Select a League:', league_options)

# 根据用户选择设置文件路径
file_paths = {
    'Premier League': 'Premier League 2023-2024.csv',
    'Serie A': 'Serie A 2023-2024.csv'
}

# 读取用户选择的文件
file_path = file_paths[league_choice]
df = pd.read_csv(file_path)

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

# 设置地图边界框
m.fit_bounds(bounds)

feature_group.add_to(m)

# 创建显示坐标控件并添加到地图控件中
MousePosition().add_to(m)

st_folium(m, width=700, height=500)
