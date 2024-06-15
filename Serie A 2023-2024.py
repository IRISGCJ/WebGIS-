import requests
from lxml import etree
import pandas as pd
from bs4 import BeautifulSoup

# 定义爬取数据的函数
def fetch_data(url, xpath):
    response = requests.get(url)
    response.raise_for_status()  # 确保请求成功
    html_content = response.content

    # 解析HTML
    tree = etree.HTML(html_content)
    data = tree.xpath(xpath)
    
    return data

# 解析表格数据并获取城市的Wikipedia链接
def parse_table_data(data):
    results = []
    for row in data:
        cols = row.xpath('td')
        if len(cols) >= 4:
            team = cols[0].xpath('string()').strip()
            location = cols[1].xpath('string()').strip()
            location_href = cols[5].xpath('.//a/@href')[0]
            location_url = f"https://en.wikipedia.org{location_href}"
            current_stadium = cols[5].xpath('string()').strip()
            results.append((team, location, location_url, current_stadium))
    return results[:20]  # 只保留前20个数据

# 获取地理坐标
def get_coordinates(city_url):
    response = requests.get(city_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
        
        # 方法一：尝试从信息框中获取经纬度
    try:
        latitude = soup.select_one('#mw-content-text > div.mw-content-ltr.mw-parser-output > table.infobox.ib-settlement.vcard > tbody > tr.mergedbottomrow .latitude').get_text()
        longitude = soup.select_one('#mw-content-text > div.mw-content-ltr.mw-parser-output > table.infobox.ib-settlement.vcard > tbody > tr.mergedbottomrow .longitude').get_text()
        coordinates = f"{latitude}, {longitude}"
        # 如果方法一失败，尝试方法二
    except AttributeError:
        latitude = soup.select_one('#coordinates .latitude').get_text()
        longitude = soup.select_one('#coordinates .longitude').get_text()
        coordinates = f"{latitude}, {longitude}"
    
    return coordinates

# 爬取和显示数据
url = 'https://en.wikipedia.org/wiki/Serie_A'
xpath = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[2]/tbody/tr[position()>1]'

raw_data = fetch_data(url, xpath)
parsed_data = parse_table_data(raw_data)
    
# 获取地理坐标
teams_with_coords = []
for team, location, location_url, current_stadium in parsed_data:
    coordinates = get_coordinates(location_url)
    teams_with_coords.append((team, location, current_stadium,coordinates))
    
# 转换为DataFrame
df = pd.DataFrame(teams_with_coords, columns=['Team', 'Location', 'Current Stadium','Coordinates'])
df1=df.set_index('Team')
df1.to_csv('Serie A 2023-2024.csv')


