# 足球联赛地图和路线规划器

## 1. 项目简介

这个项目是一个基于Streamlit构建的Web应用，允许用户探索2023-2024赛季的足球联赛（英超和意甲）。用户可以查看球队的详细信息、位置，并且可以在选定的球队之间进行路线规划。应用程序使用Folium进行交互式地图展示，并利用OpenRouteService进行路线规划。

## 2. 文件结构

```
- main.py                        # 主程序，包含Streamlit应用的核心功能
- Serie A 2023-2024.py           # 爬虫程序，用于从Wikipedia爬取意甲联赛球队信息
- Premier League 2023-2024.py    # 爬虫程序，用于从Wikipedia爬取英超联赛球队信息
- Serie A 2023-2024.csv          # 爬虫程序生成的意甲联赛数据文件
- Premier League 2023-2024.csv   # 爬虫程序生成的英超联赛数据文件
- requirements.txt               # 运行环境所需库
- README.md                      # 项目说明文档
```

## 3. 安装与运行

本项目已经封装上传streamlit-cloud，您可以访问https://cjgan-footballclubs.streamlit.app/ 进行使用。

### 运行应用程序

```bash
streamlit run main.py
```

## 4. 文件说明

### 主程序 `main.py`

主程序包含了整个Web应用的核心功能，使用Streamlit构建用户界面，并集成了地图展示和路线规划功能。以下是主要函数的介绍：

#### 1. `dms_string_to_decimal(coord_str)`

将度分秒格式的地理坐标转换为十进制格式的经纬度。

```python
def dms_string_to_decimal(coord_str):
    """
    将度分秒格式的地理坐标转换为十进制格式的经纬度。
    Args:
        coord_str (str): 度分秒格式的地理坐标字符串，例如 '40°26′46″N, 79°58′56″W'。

    Returns:
        tuple: 十进制经纬度，格式为 (latitude, longitude)。
    """
    # 实现代码...
```
#### 2. `get_directions(_client, start_coords, end_coords, travel_mode)`

使用OpenRouteService API获取两个地点之间的路线信息。

```python
@st.cache_data(ttl=3600.0)
def get_directions(_client, start_coords, end_coords, travel_mode):
    """
    使用OpenRouteService API获取两个地点之间的路线信息。
    Args:
        _client (openrouteservice.Client): OpenRouteService客户端实例。
        start_coords (tuple): 起始地点的经纬度，格式为 (longitude, latitude)。
        end_coords (tuple): 终点地点的经纬度，格式为 (longitude, latitude)。
        travel_mode (str): 出行方式，例如 'driving-car', 'cycling-regular', 'foot-walking'。

    Returns:
        dict: 路线信息的GeoJSON格式。
    """
    # 实现代码...
```

#### 3. `get_address(_client, lon, lat)`

使用OpenRouteService的逆地理编码功能获取经纬度对应的地理位置地址信息。

```python
@st.cache_data(ttl=3600.0)
def get_address(_client, lon, lat):
    """
    使用OpenRouteService的逆地理编码功能获取经纬度对应的地理位置地址信息。
    Args:
        _client (openrouteservice.Client): OpenRouteService客户端实例。
        lon (float): 经度。
        lat (float): 纬度。

    Returns:
        str: 地址信息。
    """
    # 实现代码...
```

### 爬虫程序 `SeriesA.py` 和 `PremierLeague.py`

爬虫程序用于从Wikipedia页面爬取足球联赛（意甲和英超）的数据，并生成相应的CSV文件，包括球队的名称、位置、当前主场和地理坐标信息。

```python
def fetch_data(url, xpath):
    """
    从指定的URL使用XPath获取HTML数据。
    Args:
        url (str): 要爬取的页面的URL。
        xpath (str): XPath表达式，用于定位需要提取的数据。

    Returns:
        list: 包含HTML数据的列表。
    """
    # 实现代码...
```

```python
def parse_table_data(data):
    """
    解析HTML表格数据，提取足球球队的名称、位置、Wikipedia链接和当前主场信息。
    Args:
        data (list): 包含HTML数据的列表。

    Returns:
        list: 元组列表，每个元组包含球队名称、位置、Wikipedia链接和当前主场信息。
    """
    # 实现代码...
```

```python
def get_coordinates(city_url):
    """
    根据Wikipedia页面中的信息获取城市或位置的地理坐标（经纬度）信息。
    Args:
        city_url (str): 城市或位置的Wikipedia页面URL。

    Returns:
        str: 地理坐标，格式为 'latitude, longitude'。
    """
    # 实现代码...
```

## 5. 使用方法

1. 运行主程序 `mian.py` 启动Web应用。
2. 在侧边栏选择想要查看的联赛（英超或意甲）和具体球队。
3. 查看选定球队的位置、详细信息，并在地图上展示。
4. 在侧边栏选择起点和终点球队，选择出行方式，进行路线规划展示。

## 6. 依赖项

- Streamlit：用于构建交互式Web应用。
- Pandas：用于数据处理和CSV文件操作。
- Folium：用于创建地图和地图数据可视化。
- streamlit-folium：用于在Streamlit应用中集成Folium地图。
- OpenRouteService：用于获取路线规划和逆地理编码服务。
- Requests：用于HTTP请求。
- lxml：用于处理HTML和XML数据。
- BeautifulSoup4：用于解析HTML数据。

__具体版本请参考requirements.txt文件__

## 7. 注意事项

- 在使用前请确保安装所有依赖项，并且拥有OpenRouteService的API密钥(本代码提供api，您也可以使用自己的ORS api)。
- 确保网络连接畅通，以便从Wikipedia获取数据。
- 如果爬虫程序运行失败，请检查Wikipedia页面结构变化或网络问题。

__！！！由于使用OpenRouteService，以及Wikipedia，请确保运行所有程序时，使用科学上网。__

---
甘成杰 10223901424 地理科学学院 地理科学 22基地班  
iris.ganchengjie@outlook.com

