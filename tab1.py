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
        
    ###################################################################### layout 
    t1_head0, t1_head1, t1_head2 = st.columns( [0.001, 0.998, 0.001] )
    
    t1_body0, t1_body1, t1_body2, t1_body3 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1_body4, t1_body5, t1_body6, t1_body7 = st.columns( [0.001, 0.499, 0.499, 0.001] )
    t1_body8, t1_body9, t1_body10,t1_body11= st.columns( [0.001, 0.499, 0.499, 0.001] )

    t1_tail0, t1_tail1, t1_tail2 = st.columns( [0.001, 0.998, 0.001] ) 

    ###################################################################### head 1  

    t1_head1.markdown("###### 공지사항") 
    t1_head1.markdown(r"""
	1. 광주지사 민원은 증가추세에 있다고 할 수 있습니다.
    """)

    ###################################################################### body 1  
    t1_body1.markdown("###### 2024년 이슈 (민원 유형별)") 
    t1_body1_df = pd.read_csv("data/민원처리현황.csv")
    t1_body1_df = t1_body1_df.query("organ=='광주지사'" )
    t1_body1_df_gby_kind = t1_body1_df.groupby(by='서비스유형(대)').count().sort_values(by='서비스유형(대)', ascending=False)
    t1_body1_df_gby_kind = t1_body1_df_gby_kind.iloc[:5,:1]
    t1_body1_df_gby_kind.columns = ['건수']
    t1_body1_df_gby_kind['비율(%)'] = ( t1_body1_df_gby_kind['건수']/(t1_body1_df_gby_kind['건수'].sum())*100).astype(int)
    t1_body1_df_gby_kind = t1_body1_df_gby_kind.sort_values(by='건수', ascending=False)  
    t1_body1.table(t1_body1_df_gby_kind.style.background_gradient(cmap='Blues')) 

    ###################################################################### body 2 
    t1_body2.markdown("###### 주요 키워드 클라우드") 
    t = Okt() 

    text_raw = '한국어 분석을 시작합니다... 재미있어요!!!~~~한국어 분석 고속도로 포장 포장 광주 광주지사 시어요!!!~~~한국어 합니다... 재미있어요!!!~~~'
    text_nouns = t.nouns(text_raw) 
    stopwords =['시어']
    text_nouns = [n for n in text_nouns if n not in stopwords]
    text_str = ' '.join(text_nouns) 
    # t1_body2.write(text_raw)

    # text_data = '한국, 한국, korea, korea, usa, england, highway, service, highway'
    wc = WordCloud(background_color='#ECF8E0', font_path=r"data/NanumGothic.ttf", max_words=50).generate(text_str) 
    # wc = WordCloud(background_color='white', max_words=50).generate(text_str) 

    fig, ax = plt.subplots(figsize=(10,4)) 
    ax.axis('off')
    ax.imshow(wc)
    t1_body2.pyplot(fig) 

    ###################################################################### body 5 
    t1_body5.markdown("###### 노선별 민원 발생현황") 

    # -------------------------------------------------------- pie 그래프 
    # data ------------------------------------
    data_x1 = t1_body1_df_gby_kind.index.values
    data_y1 = t1_body1_df_gby_kind['건수'] 

    # preprocessing ---------------------------
    fig1, ax1 = plt.subplots(figsize=(10,4)) 
    ax1.tick_params(
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
    ax1.set_facecolor('white')                  # figure 배경색 

    # paint ----------------------------------
    explode = [0.05 for i in data_x1]
    wedgeprops={'width': 0.5, 'edgecolor': 'w', 'linewidth': 3}
    ax1.pie(data_y1, labels=data_x1, 
            startangle=260,
            counterclock=False, 
            autopct="%.1f%%", 
            # explode=explode,
            # shadow=True,
            wedgeprops=wedgeprops, 
            textprops={'size':9}) 

    t1_body5.pyplot(fig1) 

    # -------------------------------------------------------- 세로 bar 그래프 
    # data ------------------------------------
    data_x2 = t1_body1_df_gby_kind.index.values
    data_y2 = t1_body1_df_gby_kind['건수'] 

    # preprocessing ---------------------------
    fig2, ax2 = plt.subplots(figsize=(10,4)) 
    ax2.tick_params(
        # axis=x or axis=y,
        # labelsize=20,
        direction='inout',
        color = 'red',
        colors = 'blue',
        # rotation=20, 
        bottom = True, labelbottom=True,        # tick 수정
        top = False, labeltop=False,
        left = False, labelleft=False,
        right= False, labelright=False
        )
    ax2.set_facecolor('white')                  # figure 배경색 

    # paint ----------------------------------
    ax2.bar(data_x2, data_y2, color='#E0ECF8')            # bar plot 표시
    for i in range(len(data_x2)):                        # bar text 표시
        height2 = data_y2[i]+0.5 
        height2_val = str(data_y2[i])+'건'
        ax2.text(data_x2[i], height2, height2_val, 
                 ha='center', va='bottom', 
                 color='green',
                 fontsize=20)                           # bar text 폰크 

    t1_body6.pyplot(fig2) 

    # 가로 sns.barplot ----------------------------

    # sns.barplot(x=data_y, y=data_x, 
    #             hue=data_x, 
    #             dodge=False,
    #             ax=ax1) 
    # for i in range(len(data_x)):                        # bar text 표시
    #     width = data_y[i]+1.5 
    #     width_val = str(data_y[i])+'건'
    #     ax1.text(width, i, width_val, 
    #             #  ha='center', va='bottom', 
    #              color='green',
    #              fontsize=20)                           # bar text 폰크

    # t1_body5.pyplot(fig1) 
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

