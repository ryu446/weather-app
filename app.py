import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ページの設定
st.set_page_config(
    page_title="天気予報アプリ",
    page_icon="☀️",
    layout="centered"
)

st.title("☀️ リアルタイム天気予報アプリ")
st.write("世界の都市の現在の天気と、今後の天気予報を確認できます。")

# APIキー設定
API_KEY = "e1067659ccf098b2a213ac6bcd206b55"

# 都市名の入力フォーム
city = st.text_input("都市名を英語で入力してください (例: Tokyo, Osaka, London)", "Tokyo")

if st.button("天気予報を取得", type="primary"):
    if not city:
        st.warning("都市名を入力してください。")
    else:
        with st.spinner("天気情報を取得中..."):
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ja"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # 現在の天気情報
                current = data['list'][0]
                current_temp = current['main']['temp']
                current_desc = current['weather'][0]['description']
                current_icon = current['weather'][0]['icon']
                city_name = data['city']['name']
                country = data['city']['country']
                
                st.subheader(f"📍 {city_name}, {country} の現在の天気")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(f"http://openweathermap.org/img/wn/{current_icon}@2x.png", width=100)
                with col2:
                    st.metric(label="気温", value=f"{current_temp:.1f} °C")
                    st.write(f"**天気状況:** {current_desc}")
                
                st.divider()
                st.subheader("📈 気温の変化（3時間ごと）")
                
                # 予報データの作成
                forecast_list = []
                for item in data['list']:
                    dt = datetime.fromtimestamp(item['dt'])
                    temp = item['main']['temp']
                    humidity = item['main']['humidity']
                    weather_desc = item['weather'][0]['description']
                    
                    forecast_list.append({
                        '日時': dt.strftime('%m/%d %H:%M'),
                        '天気': weather_desc,
                        '気温 (°C)': round(temp, 1),
                        '湿度 (%)': humidity
                    })
                
                df = pd.DataFrame(forecast_list)
                
                # 折れ線グラフの表示
                st.line_chart(df.set_index('日時')['気温 (°C)'])
                
                # テーブル表示
                st.subheader("📋 詳細データ")
                st.dataframe(df, use_container_width=True)
                
            else:
                st.error(f"「{city}」のデータが見つかりませんでした。都市名（英語表記）を確認してください。")
