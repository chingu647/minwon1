import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np 

import matplotlib as mpl 
import matplotlib.pyplot as plt 
import matplotlib.font_manager as fm 
import seaborn as sns

import geopandas as gpd 
import folium 
from streamlit_folium import folium_static 

import nltk 
from konlpy.tag import Kkma, Hannanum, Twitter, Okt
from wordcloud import WordCloud, STOPWORDS 


def run_tab(): 
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ css 설정
    st.markdown(""" 
                <style> 
                    table{background-color:#f0f0f0;} 
                    # div{border:1px solid #00ff00;}
                    img {max-width: 600px; max-height: 600px;}    # 이미지 파일 최대크기 제한
                </style> """, 
                unsafe_allow_html=True
                ) 

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ST CACHE 사용
    # @st.cache
    def load_df(organ, kind1):
        df = pd.read_csv("data/민원처리현황.csv")
        df = df.query( f"organ=='{organ}'" )
        kind1_df = df.groupby(by=f'{kind1}').count() #.sort_values(by=f'{kind1}', ascending=False)
        kind1_df = kind1_df.iloc[:5,:1]
        kind1_df.columns = ['건수']
        kind1_df['비율(%)'] = ( kind1_df['건수']/(kind1_df['건수'].sum())*100).astype(int)
        kind1_df = kind1_df.sort_values(by='건수', ascending=False) 

        return kind1_df  
    
    # @st.cache
    def load_wc(text_raw):
        t = Okt()
        text_nouns = t.nouns(text_raw) 
        stopwords =['시어']
        text_nouns = [n for n in text_nouns if n not in stopwords]
        text_str = ' '.join(text_nouns)
        wc = WordCloud(background_color='#ECF8E0', font_path=r"data/NanumGothic.ttf", max_words=50).generate(text_str) 
        
        return wc 


    ###################################################################### layout 
    t1h0, t1h1, t1h2 = st.columns( [0.001, 0.998, 0.001] )
    
    t1b0, t1b1, t1b2, t1b3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1b4, t1b5, t1b6, t1b7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1b8, t1b9, t1b10,t1b11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t1t0, t1t1, t1t2 = st.columns( [0.001, 0.998, 0.001] ) 

    ###################################################################### head 1  
    t1h1.markdown("###### 공지사항") 

    t1h1.markdown(r"""
	1. 광주지사 민원은 증가추세에 있다고 할 수 있습니다.
    """)

    ###################################################################### body 1  
    t1b1.markdown("###### 2024년 이슈 (민원 유형별)") 

    t1b1_kind1_df = load_df('광주지사', '서비스유형(대)') 

    t1b1.table(t1b1_kind1_df.style.background_gradient(cmap='Blues')) 

    ###################################################################### body 2 
    t1b2.markdown("###### 주요 키워드 클라우드") 

    text_raw = '한국어 분석을 시작합니다... 재미있어요!!!~~~한국어 분석 고속도로 포장 포장 광주 광주지사 시어요!!!~~~한국어 합니다... 재미있어요!!!~~~'
    t1b2_wc = load_wc(text_raw)
  

    t1b2_fig, t1b2_ax = plt.subplots(figsize=(10,4)) 
    t1b2_ax.axis('off')
    t1b2_ax.imshow(t1b2_wc)
    t1b2.pyplot(t1b2_fig) 

    ###################################################################### body 5 
    t1b5.markdown("###### 노선별 민원 발생현황") 

    # -------------------------------------------------------- pie 그래프 
    # data  
    t1b5_kind1_df = load_df('광주지사', '서비스유형(대)') 

    t1b5_x = t1b5_kind1_df.index.values
    t1b5_y = t1b5_kind1_df['건수'] 

    # preprocessing
    t1b5_fig, t1b5_ax = plt.subplots(figsize=(10,4)) 
    t1b5_ax.tick_params(
        # axis=x or axis=y,
        # labelsize=20,
        direction='inout',
        color = 'red',
        colors = 'blue',
        # rotation=20, 
        bottom = True, labelbottom=True,        # tick 수정
        top = False, labeltop=False,
        left = True, labelleft=True,
        right= False, labelright=False
        )
    t1b5_ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    explode = [0.05 for i in t1b5_x]
    wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 3}
    t1b5_ax.pie(t1b5_y, labels=t1b5_x, 
            startangle=260,
            counterclock=False, 
            autopct="%.1f%%", 
            # explode=explode,
            # shadow=True,
            wedgeprops=wedgeprops, 
            textprops={'size':9}) 

    t1b5.pyplot(t1b5_fig) 

    ###################################################################### body 6 
    t1b6.markdown("###### 노선별 민원 발생현황") 

    # -------------------------------------------------------- 세로 bar 그래프 
    # data  
    t1b6_kind1_df = load_df('광주지사', '서비스유형(대)') 

    t1b6_x = t1b6_kind1_df.index.values
    t1b6_y = t1b6_kind1_df['건수'] 

    # preprocessing 
    t1b6_fig, t1b6_ax = plt.subplots(figsize=(10,4)) 
    t1b6_ax.tick_params(
        # axis=x or axis=y,
        labelsize=20,
        direction='inout',
        color = 'red',
        colors = 'blue',
        # rotation=20, 
        bottom = True, labelbottom=True,        # tick 수정
        top = False, labeltop=False,
        left = False, labelleft=False,
        right= False, labelright=False
        )
    t1b6_ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    t1b6_ax.bar(t1b6_x, t1b6_y, color='#E0ECF8')            # bar plot 표시
    for i in range(len(t1b6_x)):                        # bar text 표시
        height = t1b6_y[i]+0.5 
        height_str = str(t1b6_y[i])+'건'
        t1b6_ax.text(t1b6_x[i], height, height_str, 
                 ha='center', va='bottom', 
                 color='green',
                 fontsize=20)                           # bar text 폰크 

    t1b6.pyplot(t1b6_fig) 

    ###################################################################### body 9
    t1b9.markdown("###### 노선별 민원 발생현황") 
    
    # -------------------------------------------------------- 가로 sns bar 그래프 
    # data  
    t1b9_kind1_df = load_df('광주지사', '서비스유형(대)') 
    t1b9_x = t1b9_kind1_df.index.values
    t1b9_y = t1b9_kind1_df['건수'] 

    # preprocessing ---------------------------
    t1b9_fig,  t1b9_ax = plt.subplots(figsize=(10,4)) 
    t1b9_ax.tick_params(
        # axis=x or axis=y,
        labelsize=20,
        direction='inout',
        color = 'red',
        colors = 'blue',
        # rotation=20, 
        bottom = True, labelbottom=True,        # tick 수정
        top = False, labeltop=False,
        left = False, labelleft=False,
        right= False, labelright=False
        )
    t1b9_ax.set_facecolor('white')                  # figure 배경색 

    # paint 
    sns.barplot(x=t1b9_y, y=t1b9_x, 
                hue=t1b9_x, 
                dodge=False,
                ax=t1b9_ax) 
    for i in range(len(t1b9_x)):               # bar text 표시
        width = t1b9_y[i]+1.5 
        width_str = str(t1b9_y[i])+'건'
        t1b9_ax.text(width, i, width_str, 
                #  ha='center', va='bottom', 
                 color='green',
                 fontsize=20)                   # bar text 폰크

    t1b9.pyplot(t1b9_fig) 
    # ===================================================== 그래프 end

    t1_body5_df = pd.read_csv("data/민원처리현황.csv")
    t1_body5_df = t1_body5_df.query("organ=='광주지사'" )
    t1_body5_df_gby_kind = t1_body5_df.groupby(by='서비스유형(대)').count().sort_values(by='서비스유형(대)', ascending=False)
    t1_body5_df_gby_kind = t1_body5_df_gby_kind.iloc[:5,:1]
    t1_body5_df_gby_kind.columns = ['건수']
    t1_body5_df_gby_kind = t1_body5_df_gby_kind.sort_values(by='건수', ascending=False)  
    t1_body5.table(t1_body5_df_gby_kind.style.background_gradient(cmap='Blues')) 


    # ---------------------------------------------------- 
    # map 
    # base_position = [35.18668601, 126.87954220] 
    # map_data = pd.DataFrame(np.random.randn(5,1)/[20,20] + base_position,
    #     columns=['lat','lon'] 
    #     ) 
    # #print(map_data) 
    # t1_tail1.code('con11.map(map_data)')
    # t1_tail1.map(map_data) 

    # map data
    t1_gpf_point = gpd.read_file("data/ex_point_KWANGJU.geojson")
    t1_gpf_point = t1_gpf_point[ ['노선번호','X좌표값', 'Y좌표값'] ]
    t1_gpf_point.columns = ['노선번호','latitude','longitude'] 

    t1_gpf_point = t1_gpf_point.iloc[:5, :]
    base_position = [35.18668601, 126.87954220] 

    # map layout ---------------------------------------------------------
    t1_map = folium.Map( location=base_position, zoom_start=9 ) #, tiles='Stamentoner') 

    t1_gpf_line = gpd.read_file("data/ex_line_KWANGJU.shp") 
    folium.GeoJson(t1_gpf_line,
                   style_function=lambda feature: {
                       'fillColor': 'blue' , #feature['properties']['color'],
                       'color': '#F5F6CE',
                       'weight': 3,
                       'dashArray': '5, 5',
                       'fillOpacity': 0.3, 
                       }
                    ).add_to(t1_map)


    for index, row in t1_gpf_point.iterrows():
        folium.CircleMarker( location=[ row['latitude'], row['longitude'] ],  # 원 중심
                            radius=1,            # 원 반지름
                            color='blue',        # 원 테두리 색상
                            fill=True,           # 원 채움
                            fill_opacity=1.0     # 원 채움 투명도
                            ).add_to(t1_map) 
        
        folium.Marker( location=[ row['latitude'], row['longitude'] ],  # 값 중심 
                      popup=row['노선번호'],
                      tooltip=row['latitude'],
                      icon=folium.Icon(color='red', icon='star'), 
                    #   icon=folium.DivIcon(                              # 값 표시방식
                    #       html=f"<div>{row['노선번호']} {row['latitude']} {row['longitude']}</div>"),
                      ).add_to(t1_map) 

    folium_map = t1_map._repr_html_() 
    st.components.v1.html(folium_map, height=900) #, width=800, height=600)
    # folium_static(t1_map) #, width=600, height=400)
    # t1_tail1.map(data=t1_gpf, latitude='latitude', longitude='longitude')  

