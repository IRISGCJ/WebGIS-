import streamlit as st
import numpy as np
import pandas as pd
import folium
from folium.plugins import MousePosition
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

# 获取选定球队的详细信息
team_info = df[df['Team'] == team_choice].iloc[0]
coords = team_info['Coordinates']
lat, lon = dms_string_to_decimal(coords)

# 在主页面显示选定球队的详细信息
st.title(f'{team_choice} Details')
team_info_dict = team_info.to_dict()
for key, value in team_info_dict.items():
    st.write(f"{value}")
    
# 创建地图对象并添加选定球队的位置
m = folium.Map(location=[lat, lon], zoom_start=15)
folium.Marker(
    location=[lat, lon],
    popup=f"{team_choice}"
).add_to(m)

# 创建显示坐标控件并添加到地图控件中
MousePosition().add_to(m)

# 使用 streamlit_folium 显示地图
st_folium(m, width=700, height=500)
