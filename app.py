import streamlit as st 
import pandas
import numpy
import plotly.graph_objects as go
import time
from enum import Enum  ##枚举类型
from config_adapt import Config_Adapt
from PIL import Image

class CatType(Enum):    ##各单元格的类型
   XIAOKE=0
   PIKAQIU=1
   SHNEGYE=2
   NATIE=3
   NAICHA=4
   XUEDING=5
   danzai=6
   YUANBAO=7
   DUDU=8

class CatWebsite(object):
    def __init__(self):
        self.init_config()

        # 设置网页显示信息
        st.set_page_config(
            page_title='熊宝的小可',
            page_icon="🧊",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.extremelycoolapp.com/help',
                'Report a bug': "https://www.extremelycoolapp.com/bug",
                'About': "# This is a header. This is an *extremely* cool app!"}
        )

        # 设置首页信息
        st.title('记录Leo的小猫们:sunglasses:')
        tab_log, tab_ke, tab_pi, tab_ye, tab_tie, tab_tea, tab_xue, tab_dan, tab_bao, tab_du = st.tabs(
            ["日志", '小可', '皮卡丘', '生椰', '拿铁', '奶茶', '雪顶', '蛋仔', '元宝', '嘟嘟'])

        # 设置侧边栏
        with st.sidebar:
            st.title('欢迎来我的小猫舍')
            # 打开Markdown文件
            self.show_md('mdfiles/自我介绍.md')

        # 设置主页面    
        with tab_log:
            st.header('欢迎来到我的小猫世界')
            col1, col2, col3 = st.columns(3)
            col1.image(Image.open('./photo/xiaoke.png'), caption='小可')
            col2.image(Image.open('./photo/pikaqiu.png'), caption='皮卡丘')
            col3.image(Image.open('./photo/xueding.png'), caption='雪顶')

            col4, col5, col6 = st.columns(3)
            col4.image(Image.open('./photo/naicha.png'), caption='奶茶')
            col5.image(Image.open('./photo/natie.png'), caption='拿铁')
            col6.image(Image.open('./photo/shengye.png'), caption='生椰')

            col7, col8, col9 = st.columns(3)
            col7.image(Image.open('./photo/danzai.png'), caption='蛋仔')
            col8.image(Image.open('./photo/yuanbao.png'), caption='元宝')
            col9.image(Image.open('./photo/dudu.png'), caption='嘟嘟')

            st.divider()
            # 打开Markdown文件
            self.show_md('mdfiles/猫猫.md')

            # 显示地图
            st.subheader("下面是我的小猫分布图")
            self.show_map()

            # 显示投票
            option = st.selectbox(
                '给你喜欢的猫咪投票！！！', self.cats_name)
            st.divider()
            '你将投票给: ', option
            if st.button("投票", key=None):
                st.balloons()
                st.success('投票成功！')
                self.save_config(option)

        with tab_ke:
            self.show_md('mdfiles/小可.md')
        with tab_pi:
            self.show_md('mdfiles/皮卡丘.md')
        with tab_ye:
            self.show_md('mdfiles/生椰.md')
        with tab_tie:
            self.show_md('mdfiles/拿铁.md')
        with tab_tea:
            self.show_md('mdfiles/奶茶.md')
        with tab_xue:
            self.show_md('mdfiles/雪顶.md')
        with tab_dan:
            self.show_md('mdfiles/蛋仔.md')
        with tab_bao:
            self.show_md('mdfiles/元宝.md')
        with tab_du:
            self.show_md('mdfiles/嘟嘟.md')
    
    def init_config(self): # 初始化配置文件
        self.config_obj = Config_Adapt("web_config.ini")
        self.cats_name = ['小可', '皮卡丘', '生椰', '拿铁', '奶茶', '雪顶', '蛋仔', '元宝', '嘟嘟']
        self.votes_list = [0]*len(self.cats_name)
        self.location_data = []

        self.votes_list[CatType.XIAOKE.value] = int(self.config_obj.get_config("votes", "xiaoke")["data"])
        self.votes_list[CatType.PIKAQIU.value] = int(self.config_obj.get_config("votes","pikaqiu")["data"])
        self.votes_list[CatType.SHNEGYE.value] = int(self.config_obj.get_config("votes","shengye")["data"])
        self.votes_list[CatType.NATIE.value] = int(self.config_obj.get_config("votes", "natie")["data"])
        self.votes_list[CatType.NAICHA.value] = int(self.config_obj.get_config("votes", "naicha")["data"])
        self.votes_list[CatType.XUEDING.value] = int(self.config_obj.get_config("votes","xueding")["data"])
        self.votes_list[CatType.danzai.value] = int(self.config_obj.get_config("votes", "danzai")["data"])
        self.votes_list[CatType.YUANBAO.value] = int(self.config_obj.get_config("votes", "yuanbao")["data"])
        self.votes_list[CatType.DUDU.value] = int(self.config_obj.get_config("votes","dudu")["data"])

    # 选取票数之后，进入增加票数
    def save_config(self, cat):
        # read data from config file
        if cat == "小可":
            self.votes_list[CatType.XIAOKE.value] += 1
            self.config_obj.set_config("votes", "xiaoke", str(self.votes_list[CatType.XIAOKE.value]))
        elif cat == "皮卡丘":
            self.votes_list[CatType.PIKAQIU.value] += 1
            self.config_obj.set_config("votes", "pikaqiu", str(self.votes_list[CatType.PIKAQIU.value]))
        elif cat == "生椰":
            self.votes_list[CatType.SHNEGYE.value] += 1   
            self.config_obj.set_config("votes", "shengye", str(self.votes_list[CatType.SHNEGYE.value]))
        elif cat == "拿铁":
            self.votes_list[CatType.NATIE.value] += 1
            self.config_obj.set_config("votes", "natie", str(self.votes_list[CatType.NATIE.value]))
        elif cat == "奶茶":
            self.votes_list[CatType.NAICHA.value] += 1
            self.config_obj.set_config("votes", "naicha", str(self.votes_list[CatType.NAICHA.value]))
        elif cat == "雪顶":
            self.votes_list[CatType.XUEDING.value] += 1
            self.config_obj.set_config("votes", "xueding", str(self.votes_list[CatType.XUEDING.value]))
        elif cat == "蛋仔":
            self.votes_list[CatType.danzai.value] += 1
            self.config_obj.set_config("votes", "danzai", str(self.votes_list[CatType.NATIE.value]))
        elif cat == "元宝":
            self.votes_list[CatType.YUANBAO.value] += 1
            self.config_obj.set_config("votes", "yuanbao", str(self.votes_list[CatType.NAICHA.value]))
        elif cat == "嘟嘟":
            self.votes_list[CatType.DUDU.value] += 1
            self.config_obj.set_config("votes", "dudu", str(self.votes_list[CatType.XUEDING.value]))
        self.show_graph()

    # 显示统计数据图
    def show_graph(self):
        chart = go.Figure()
        chart.add_trace(go.Bar(x=self.cats_name, y=self.votes_list))
        chart.update_layout(
            title="猫咪的票数统计图",
            xaxis=dict(title="猫咪的名字"),
            yaxis=dict(title="票数")
        )
        chart.update_layout(width=800, height=400)
        st.plotly_chart(chart)

    def to_int(self, value):
        ret_list = []
        for i in value:
            ret_list.append(float(i))
        return ret_list
    
    # 显示markdown文件，传入文件位置
    def show_md(self, position):
        with open(file= position, mode='r', encoding= "utf-8") as file:
            # 将内容转换为HTML格式
            content = file.read()
            # print(content)
            st.markdown(content)

    # 显示地图，传入地图文件位置
    def show_map(self, map_files="location.txt"):
        with open(map_files, encoding="utf-8") as loc_obj:
            for line in loc_obj.readlines():
                self.location_data.append(self.to_int(list(line.strip().split(" "))[1:]))

        map_data = pandas.DataFrame(self.location_data, columns=['lat', 'lon'])
        # print(map_data)
        st.map(map_data,color="#FF0000", use_container_width=True)

if __name__ == '__main__':
    CatWebsite()

