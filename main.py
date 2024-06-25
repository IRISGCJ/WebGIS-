import streamlit as st
import numpy as np
import pandas as pd
import folium
from folium.plugins import MousePosition
from streamlit_folium import st_folium
import openrouteservice

# 设置OpenRouteService API密钥
ORS_API_KEY = '5b3ce3597851110001cf6248ec4432c73f4f4735a30df115efb8e6bc'

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
    
    lat = dms_to_decimal(lat_deg, lat_min, lat_sec)
    lon = dms_to_decimal(lon_deg, lon_min, lon_sec)
    
    if lat_dir == 'S':
        lat = -lat
    if lon_dir == 'W':
        lon = -lon
    
    return lat, lon

# 获取路线规划
@st.cache_data(ttl=3600.0)
def get_directions(_client, start_coords, end_coords):
    routes = _client.directions(
        coordinates=(start_coords, end_coords),
        profile='driving-car',
        format='geojson'
        )
    return routes

# 定义侧边栏
st.sidebar.title('Football Leagues 2023-2024')
file_paths = {
    'Premier League': 'Premier League 2023-2024.csv',
    'Serie A': 'Serie A 2023-2024.csv'
}
league_options = list(file_paths.keys())
league_choice = st.sidebar.selectbox('Select a League:', league_options)

# 读取用户选择的文件
file_path = file_paths[league_choice]
df = pd.read_csv(file_path)

# 在侧边栏显示球队名称供用户选择
teams = df['Team'].tolist()
team_choice = st.sidebar.selectbox('Select a Team:', teams)
navigation_mode = st.sidebar.checkbox('Enable Navigation Mode')

while True:
    # 获取选定球队的详细信息
    team_info = df[df['Team'] == team_choice].iloc[0]
    coords = team_info['Coordinates']
    lat, lon = dms_string_to_decimal(coords)

    # 在主页面显示选定球队的详细信息
    st.title(f'{team_choice} Details')
    team_info_dict = team_info.to_dict()
    st.write(f"位置：{lon:.4f}, {lat:.4f}")
    
    # 创建地图对象并添加选定球队的位置
    m = folium.Map(location=[lat, lon], zoom_start=15)

    tile_layers = {
        "OpenStreetMap": "openstreetmap",
        "Esri全球影像": "Esri.WorldImagery",
        "CartoDB Voyager":"CartoDB Voyager"
    }

    for name, tile in tile_layers.items():
        if "OpenStreetMap" in name:
            folium.TileLayer(tile).add_to(m)
        elif "Esri全球影像" in name:
            folium.TileLayer(tile).add_to(m)
        elif "CartoDB Voyager" in name:
            folium.TileLayer(tile).add_to(m)

    folium.Marker(
        location=[lat, lon],
        popup=f"{team_choice}"
        ).add_to(m)

    folium.LayerControl().add_to(m)
    MousePosition().add_to(m)

    # 使用 streamlit_folium 显示地图
    st_folium(m)
    
    

    if navigation_mode:
        st.write('This mode use OpenRouteServices')
        st.sidebar.subheader('Choose Start and End Points')
    
        # 显示球队列表供选择起点和终点
        teams = df['Team'].tolist()
        start_team = st.sidebar.selectbox('Select Start Team:', teams)
        end_team = st.sidebar.selectbox('Select End Team:', teams)

        # 获取选定球队的坐标信息
        start_coords = df[df['Team'] == start_team]['Coordinates'].values[0]
        start_lat,start_lon=dms_string_to_decimal(start_coords)
        end_coords = df[df['Team'] == end_team]['Coordinates'].values[0]
        end_lat,end_lon=dms_string_to_decimal(end_coords)
        start=(start_lon,start_lat)
        end=(end_lon,end_lat)
        client = openrouteservice.Client(key=ORS_API_KEY)

        # 创建Folium地图
        map_center = [(start_lat + end_lat) / 2, (start_lon + end_lon) / 2]
        m1 = folium.Map(location=map_center, zoom_start=10)

        #获取路线
        route=get_directions(client,start,end)
        folium.GeoJson(route, name='路线').add_to(m1)
    
        # 添加起点和终点标记
        folium.Marker([start_lat, start_lon], tooltip='起点', icon=folium.Icon(color='green')).add_to(m1)
        folium.Marker([end_lat, end_lon], tooltip='终点', icon=folium.Icon(color='red')).add_to(m1)

        # 绘制路线
        folium.GeoJson(route, name='路线').add_to(m)
        
        # 使用 streamlit_folium 显示地图
        st_folium(m1)
    break
