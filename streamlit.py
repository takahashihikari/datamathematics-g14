import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# カスタムCSSを適用
st.markdown("""
    <style>
    .stApp {
        background-color: #f3ffc6;
    }
    .stTextInput label {
        color: #333;
        font-weight: bold;
        font-size: 1.2em;
    }
    .stFileUploader label {
        color: #333;
        font-weight: bold;
        font-size: 1.2em;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        font-size: 1em;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #0056b3;
        color: white;
    }
    .stMarkdown h1, h2, h3, h4, h5, h6 {
        color: #007bff;
    }
    
    </style>
""", unsafe_allow_html=True)

st.title("アンケート結果の分析")

# ユーザーからエクセルファイルをアップロードしてもらう
uploaded_file = st.file_uploader("アンケート結果のエクセルファイルをアップロードしてください", type=["xlsx"])

if uploaded_file:
    # エクセルファイルを読み込む
    df = pd.read_excel(uploaded_file, index_col=0)  # 1列目をインデックスとして使用する
    A = df.values[0:, 0:]  # 2行目と2列目以降を取得
    
    st.subheader("アンケート結果:")
    st.dataframe(df)
    
    # ユーザーからベクトルbの入力を受け取る
    input_values = st.text_input("生徒の評価を入力してください（例: 2,5,3）")

    if input_values:
        # 入力された値を処理する
        try:
            # カンマで分割して整数に変換
            b_values = [int(x) for x in input_values.split(',')]
            if len(b_values) == A.shape[1]:
                # numpy配列に変換してreshape
                b = np.array(b_values).reshape(-1, 1)

                # np.dot(A, b)の結果を計算
                result = np.dot(A, b)

                # 結果を表示
                st.subheader("新しいアンケートの結果")
                st.write(result)

                # データの準備
                data = result.flatten()
                labels = df.index.tolist() 

                # 水平棒グラフを作成
                fig, ax = plt.subplots()
                ax.barh(range(len(data)), data, tick_label=labels, color='#007bff')

                # グラフのタイトルとラベルを設定（オプション）
                ax.set_ylabel('question')
                ax.set_title('new questionnaire results')

                # グラフをStreamlitで表示
                st.pyplot(fig)
            else:
                st.error(f"正確に {A.shape[1]} 個の整数を入力してください。")
        except ValueError:
            st.error("カンマで区切られた有効な整数を入力してください。")
else:
    st.info("エクセルファイルをアップロードしてください。")

