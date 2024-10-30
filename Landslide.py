# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import time
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import warnings

warnings.filterwarnings("ignore")

# URL của dữ liệu trên ThingSpeak
THINGSPEAK_URL = 'https://api.thingspeak.com/channels/2683852/feeds.csv?api_key=BHVMN9MSF6DWVM5F&results=8000'

# Hàm tải dữ liệu từ ThingSpeak
def load_data():
    try:
        # Tải dữ liệu từ URL
        startup_df = pd.read_csv(THINGSPEAK_URL)
        return startup_df
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu từ ThingSpeak: {e}")
        return None

# Huấn luyện mô hình Linear Regression và trả về độ chính xác
def train_and_predict(startup_df):
    # Kiểm tra dữ liệu
    if startup_df is None or startup_df.empty:
        print("Không có dữ liệu để huấn luyện mô hình.")
        return None
    
    # Xử lý dữ liệu
    x = startup_df.iloc[:, 2:8]  # Lấy cột từ 3 đến 8
    y = startup_df.iloc[:, 2]  # Lấy cột 3 làm nhãn dự đoán

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    # Huấn luyện mô hình hồi quy tuyến tính
    linreg = LinearRegression()
    linreg.fit(x_train, y_train)

    # Dự đoán trên tập kiểm tra
    y_pred = linreg.predict(x_test)

    # Tính độ chính xác
    accuracy = r2_score(y_test, y_pred) * 100
    return accuracy

# Đưa ra cảnh báo dựa trên độ chính xác
def alert_system(accuracy):
    if accuracy is None:
        print("Không thể tính toán độ chính xác, bỏ qua cảnh báo.")
        return

    print(f"Model accuracy: {accuracy:.2f}%")
    
    if accuracy < 70:
        print("Landslide alert: Safe area, no chances of landslide.")
    elif 70 <= accuracy < 86:
        print("Landslide alert: Moderate chances of landslide, be alert.")
    elif 86 <= accuracy < 91:
        print("Landslide alert: Yellow zone, high chances of landslide.")
    elif 91 <= accuracy < 100:
        print("Landslide alert: Danger Zone, lookout in area as there are high chances of prediction.")
    elif accuracy == 100:
        print("Landslide alert: !!!!!!!!!!!!Landslide!!!!!!! Evacuate immediately!")

# Chạy chương trình chính
def main():
    while True:
        print("\nĐang tải dữ liệu từ ThingSpeak...")
        startup_df = load_data()

        if startup_df is not None:
            print("Dữ liệu đã được tải thành công, bắt đầu huấn luyện mô hình.")
            accuracy = train_and_predict(startup_df)

            # Đưa ra cảnh báo dựa trên độ chính xác
            alert_system(accuracy)
        else:
            print("Không có dữ liệu để xử lý.")

        # Đợi 10 phút (600 giây) trước khi tải lại dữ liệu mới
        time.sleep(600)

if __name__ == "__main__":
    main()
