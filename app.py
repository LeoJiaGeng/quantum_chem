import numpy as np
import requests
from collections import Counter
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import jieba
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from PIL import Image
import plotly.graph_objects as go
# 设置仿宋字体路径（替换为你本地的仿宋字体路径）
font_path = '仿宋_GB2312.ttf'

def main():
    # 使用 Streamlit 构建界面
    st.title('中文文本分词与词频统计:sunglasses:')
    # 输入要爬取的网页 URL
    url = st.text_input('请输入要爬取的网页 URL')
    # 执行爬虫逻辑并获取数据
    if url:
        data = crawl_data(url)
        data_utf8 = data.encode('utf-8')  # 如果data已经是字符串，这一步不是必需的
        # 对内容进行分词
        words =  jieba.lcut_for_search(data_utf8)
        # st.text(words)
        # 计算词语频率
        word_counts = Counter(words)
        # 找出出现次数最多的词语
        most_common_words = word_counts.most_common()
        # 构建数据框
        df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])
        #删除长度为一的值一个重复量为一的值

        df = df[~(df['Word'].str.len() == 1)]
        # 手动重新排序行号
        df = df.reset_index(drop=True)
        # 将结果展示在 Streamlit 应用中
        num = st.select_slider('请选择你要查询的数据量：', options=[5, 10 , 15, 20, 25, 30])
        st.write("出现次数最多的词语：")
        top_20_data = df.head(num)
        st.dataframe(top_20_data)

        #词云
        text = ' '.join(top_20_data['Word'])
        wordcloud = WordCloud(width=800,
                  height=400,
                  background_color='white',
                  font_path='仿宋_GB2312.ttf',  # 设置中文字体
                  colormap='viridis',  # 设置颜色映射
                  contour_width=1,
                  contour_color='steelblue',  # 设置轮廓颜色
                  max_words=100,  # 最大显示词数
                  max_font_size=80,  # 最大字体大小
                  random_state=42  # 随机状态，以确保每次生成相同的词云
                  ).generate(text)
        # 显示词云
        # 将词云图像转换为Pillow图像
        wordcloud_image = Image.fromarray(wordcloud.to_array())
        # 使用streamlit显示图像
        st.image(wordcloud_image)

        # 创建侧边栏
        st.sidebar.title('选择图像')
        # 创建复选框，包含7种图形的选项
        graph_options = ['直方图', '扇形图', '折线图', '散点图', '条形图', '面积图','瀑布图']
        selected_graphs = st.sidebar.selectbox('选择图像', graph_options)
        #

        if '条形图' in selected_graphs:
            chart = go.Figure()
            chart.add_trace(go.Bar(x=top_20_data['Word'], y=top_20_data['Frequency']))
            chart.update_layout(
                title="条形图",
                xaxis=dict(title="Word"),
                yaxis=dict(title="Frequency")
            )
            chart.update_layout(width=800, height=400)
        elif '折线图' in selected_graphs:
            chart = go.Figure()
            chart.add_trace(go.Scatter(x=top_20_data['Word'], y=top_20_data['Frequency'], mode='lines'))
            chart.update_layout(
                title="折线图",
                xaxis=dict(title="Word"),
                yaxis=dict(title="Frequency")
            )
            chart.update_layout(width=800, height=400)
        elif '散点图' in selected_graphs:
            # 创建散点图
            chart = go.Figure()

            # 添加散点
            chart.add_trace(go.Scatter(
                x=top_20_data['Word'],  # x轴数据
                y=top_20_data['Frequency'],  # y轴数据
                mode='markers',  # 散点图模式
                marker=dict(
                    size=10,  # 散点大小
                    color='blue',  # 散点颜色
                    opacity=0.7,  # 散点透明度
                    symbol='circle'  # 散点形状
                ),
                text=top_20_data['Word'],  # 鼠标悬停时显示的文本
                name='Top 20 Data'  # 图例名称
            ))
            # 更新布局
            chart.update_layout(
                title="散点图",
                xaxis=dict(title="Word"),
                yaxis=dict(title="Frequency")
            )
            chart.update_layout(width=800, height=400)
        elif '面积图' in selected_graphs:
            chart = go.Figure()
            chart.add_trace(
                go.Scatter(x=top_20_data['Word'], y=top_20_data['Frequency'], fill='tozeroy', fillcolor='yellow', line=dict(color='red', width=2)))
            chart.update_layout(
                title="面积图",
                xaxis=dict(title="Word"),
                yaxis=dict(title="Frequency")
            )
            chart.update_layout(width=800, height=400)
        elif '瀑布图' in selected_graphs:
            # 获取 top_20_data['Word'] 数据
            words = top_20_data['Word']
            # 为每个词生成随机颜色
            marker_colors = [generate_random_color() for _ in words]
            # 计算瀑布图的累计值
            cumulative_y = [sum(top_20_data['Frequency'][:i + 1]) for i in range(len(top_20_data['Frequency']))]
            # 创建瀑布图，并使用随机颜色
            chart = go.Figure(go.Bar(x=top_20_data['Word'], y=cumulative_y, marker_color=marker_colors))
            # 更新布局
            chart.update_layout(title='瀑布图', xaxis_title='Word', yaxis_title='累计频率')
            # 显示图表
            chart.update_layout(width=800, height=400)
        # 扇形图
        elif '扇形图' in selected_graphs:
            # 创建扇形图
            chart = go.Figure()
            # 添加扇形图数据
            chart.add_trace(go.Pie(
                labels=top_20_data['Word'],  # 扇形图标签
                values=top_20_data['Frequency'],  # 扇形图对应的值
                hole=0.3,  # 中间留空的大小，0表示没有留空
                pull=[0.1]*num,  # 通过调整这个参数，可以突出某个扇形
                textinfo='label+percent',  # 鼠标悬停时显示的信息，这里显示标签和百分比
            ))
            # 更新布局
            chart.update_layout(width=800, height=400)
            chart.update_layout(
                title="扇形图"
            )
        elif '直方图' in selected_graphs:
            plt.figure(figsize=(8, 4))
            chart = generate_histogram(top_20_data['Frequency'])
            # 在Streamlit侧边栏显示直方图


        st.plotly_chart(chart)
    else:
        error = '请输入正确的url'
        st.text(error)



# 生成随机颜色
def generate_random_color():
    return f'rgba({np.random.rand()}, {np.random.rand()}, {np.random.rand()}, 1)'


def crawl_data(url):
    # 发送GET请求并获取响应
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    # 利用requests对象的get方法，对指定的url发起请求,该方法会返回一个Response对象
    response = requests.get(url, headers=headers)
    # response = requests.get(url)
    # response.encoding = response.apparent_encoding
    response.encoding = 'utf-8'
    # 确定编码
    # encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    # 使用BeautifulSoup解析响应文本
    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
    # 查找ID为"UCAP-CONTENT"的DIV
    # div = soup.find('div', {'id': 'UCAP-CONTENT'})
    # 获取DIV中的文本内容
    content = soup.get_text()
    return content

def generate_histogram(data):
    plt.hist(data, bins=max(data), color='red', alpha=0.5)
    plt.title('直方图')
    plt.xlabel('频率值')
    plt.ylabel('该频率数据数')
    fig = plt.gcf()  # 获取当前图形对象
    return fig

if __name__ == "__main__":
    main()
