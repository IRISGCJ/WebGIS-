### 项目简介

该项目使用 Python 编写的 Streamlit 应用程序，结合爬虫技术，展示了2023-2024年英超联赛（Premier League）和意甲联赛（Serie A）球队的位置和相关信息。用户可以通过交互界面选择不同的球队并查看它们的详细信息、地图位置以及两地之间的路线规划。

### 文件结构

1. **main.py**
   - 主程序，包含 Streamlit 应用的逻辑，负责数据加载、地图显示以及路线规划。
   
2. **SeriesA.py**
   - 爬虫程序，用于从 Wikipedia 爬取意甲联赛球队信息和地理坐标，并保存为 CSV 文件。

3. **PremierLeague.py**
   - 爬虫程序，用于从 Wikipedia 爬取英超联赛球队信息和地理坐标，并保存为 CSV 文件。

### 安装与运行

1. **克隆代码库**
   ```sh
   git clone https://github.com/your-repository/project-name.git
   cd project-name
   ```

2. **安装依赖**
   ```sh
   pip install -r requirements.txt
   ```

3. **运行爬虫程序**
   ```sh
   python SeriesA.py
   python PremierLeague.py
   ```

4. **运行主程序**
   ```sh
   streamlit run main.py
   ```

### 文件说明

#### main.py
- 使用 Streamlit 创建了一个交互式网页应用。
- 加载并显示用户选择的联赛和球队的信息。
- 通过 Folium 显示球队的位置地图。
- 使用 OpenRouteService API 进行路线规划并在地图上展示。

#### SeriesA.py
- 从 Wikipedia 页面爬取意甲联赛球队信息。
- 解析并提取球队名称、位置、当前体育场和地理坐标。
- 将信息保存到 `Serie A 2023-2024.csv` 文件中。

#### PremierLeague.py
- 从 Wikipedia 页面爬取英超联赛球队信息。
- 解析并提取球队名称、位置、当前体育场和地理坐标。
- 将信息保存到 `Premier League 2023-2024.csv` 文件中。

### 使用方法

1. **选择联赛**
   - 在侧边栏中选择“Premier League”或“Serie A”。

2. **选择球队**
   - 在侧边栏中选择感兴趣的球队。

3. **查看球队信息**
   - 页面主区域会显示球队的详细信息、位置地图以及地址信息。

4. **路线规划**
   - 在侧边栏选择起点和终点球队，并选择出行方式（驾驶、骑行或步行）。
   - 页面会显示从起点到终点的路线图。

### 依赖项

- streamlit
- pandas
- folium
- streamlit_folium
- openrouteservice
- requests
- lxml
- BeautifulSoup4

### 注意事项

- 请确保在运行主程序前已经获取到 OpenRouteService API 密钥并将其填入 `main.py` 文件中。
- 爬虫程序依赖于目标网页的结构，若目标网页结构发生变化，可能需要更新相应的 XPath 表达式。

### 许可证

该项目采用 MIT 许可证，详情请参阅 LICENSE 文件。

---

通过上述步骤，您将能够成功运行并使用该应用程序来查看和分析英超联赛和意甲联赛球队的信息和路线规划。
