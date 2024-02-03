import streamlit as st 
import pandas
import numpy
import plotly.graph_objects as go
import time
from enum import Enum  ##枚举类型
from config_adapt import Config_Adapt
import markdown
 
class CatType(Enum):    ##各单元格的类型
   XIAOKE=0
   PIKAQIU=1
   SHNEGYE=2
   NATIE=3
   NAICHA=4
   XUEDING=5

class CatWebsite(object):
    def __init__(self):
        self.init_config()

        # 设置网页显示信息
        st.set_page_config(
            page_title='熊宝的小可',
            page_icon=' ',
            layout='wide'
        )

        # 设置首页信息
        st.title('记录Leo的小猫们:sunglasses:')
        tab_log, tab_ke, tab_pi, tab_ye, tab_tie, tab_tea, tab_xue = st.tabs(['日志', '小可', '皮卡丘', '生椰', '拿铁', '奶茶', '雪顶'])

        # 设置侧边栏
        with st.sidebar:
            st.title('欢迎来我的小猫舍')
            st.markdown('---')
            st.markdown('这是它们的名字：\n- 小可\n- 皮卡丘\n- 生椰\n- 拿铁\n- 奶茶\n- 雪顶')
            
        with tab_log:
            st.header('欢迎来到我的小猫世界')
            # 打开Markdown文件
            with open(file= 'mdfiles/猫猫.md', mode='r', encoding= "utf-8") as file:
                # 将内容转换为HTML格式
                content = file.read()
                st.markdown(content)
            option = st.sidebar.selectbox(
                '给你喜欢的猫咪投票！！！',
                ['小可', '皮卡丘', '生椰', '拿铁', '奶茶', '雪顶'])

            st.divider()
            '你将投票给: ', option
            if st.sidebar.button("投票", key=None):
                st.write('投票成功！')
                self.save_config(option)

        with tab_ke:
            '''
            python
            from PIL import Image
            image = Image.open('image.png')
            '''
            map_data = pandas.DataFrame(
            numpy.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon'])

            st.map(map_data)

        with tab_pi:
            '''
            ```python
            import imageio
            image = imageio.imread('image.png')
            ```
            '''
            if st.checkbox('Show dataframe'):
                chart_data = pandas.DataFrame(
                numpy.random.randn(20, 3),
                columns=['a', 'b', 'c'])

                st.line_chart(chart_data)

            latest_iteration = st.empty()

            bar = st.progress(0)

            for i in range(100):
            # Update the progress bar with each iteration.
                latest_iteration.text(f'Iteration {i+1}')
                bar.progress(i + 1)
                time.sleep(0.1)

        '...and now we\'re done!'

        ## 默认渲染到主界面
        ## st.title('这是主界面')
        ## st.info('这是主界面内容')
        # st.write(pandas.DataFrame({
        #     'first column': [1, 2, 3, 4],
        #     'second column': [10, 20, 30, 40]
        #     }))

    # 初始化配置文件
    def init_config(self):
        self.config_obj = Config_Adapt("web_config.ini")
        self.votes_list=[0,0,0,0,0,0]

        self.votes_list[CatType.XIAOKE.value] = int(self.config_obj.get_config("votes", "xiaoke")["data"])
        self.votes_list[CatType.PIKAQIU.value] = int(self.config_obj.get_config("votes","pikaqiu")["data"])
        self.votes_list[CatType.SHNEGYE.value] = int(self.config_obj.get_config("votes","shengye")["data"])
        self.votes_list[CatType.NATIE.value] = int(self.config_obj.get_config("votes", "natie")["data"])
        self.votes_list[CatType.NAICHA.value] = int(self.config_obj.get_config("votes", "naicha")["data"])
        self.votes_list[CatType.XUEDING.value] = int(self.config_obj.get_config("votes","xueding")["data"])

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
        self.show_graph()

    # 显示统计数据图
    def show_graph(self):
        chart = go.Figure()
        chart.add_trace(go.Bar(x=['小可', '皮卡丘', '生椰', '拿铁', '奶茶', '雪顶'], y=self.votes_list))
        chart.update_layout(
            title="猫咪的票数统计图",
            xaxis=dict(title="猫咪的种类"),
            yaxis=dict(title="票数")
        )
        chart.update_layout(width=800, height=400)
        st.plotly_chart(chart)
        
if __name__ == '__main__':
    CatWebsite()

