import os
import sys
import numpy as np
from xgboost import XGBRegressor

# 判斷當前執行環境
if getattr(sys, 'frozen', False):  # 是否在打包後環境
    base_path = sys._MEIPASS
else:  # 開發環境
    base_path = os.path.dirname(os.path.abspath(__file__))
    
# 模型文件的完整路徑
model_height_path = os.path.join(base_path, "model_height.json")
model_period_path = os.path.join(base_path, "model_period.json")
model_power_path = os.path.join(base_path, "model_power.json")

# 加載模型
model_height = XGBRegressor()
model_height.load_model(model_height_path)

model_period = XGBRegressor()
model_period.load_model(model_period_path)

model_power = XGBRegressor()
model_power.load_model(model_power_path)

def preprocess_input(input_data):
    """
    將原始輸入數據轉換為模型需要的特徵格式
    """
    # One-hot encoding 映射
    direction_mapping = {
        'Cross-shore': [0, 0],
        'Offshore': [1, 0],
        'Onshore': [0, 1]
    }
    # One-hot encoding
    direction_type = input_data['directionType']
    direction_one_hot = direction_mapping.get(direction_type, [0, 0])  # 默認為 [0, 0]

    # 將 one-hot 編碼加入輸入數據
    input_data['directionType_Offshore'] = direction_one_hot[0]
    input_data['directionType_Onshore'] = direction_one_hot[1]

    # 刪除原始的 directionType
    del input_data['directionType']

    return input_data

def get_user_input():
    """
    從用戶那裡獲取輸入數據
    """
    print("請依次輸入以下數據：")
    try:
        input_data = {
            'gust': float(input("陣風速度 (m/s): ")),
            'surf_min': float(input("最小浪高 (m): ")),
            'surf_max': float(input("最大浪高 (m): ")),
            'speed': float(input("風速 (m/s): ")),
            'direction': float(input("風向 (度): ")),
            'pressure': float(input("氣壓 (hPa): ")),
            'temperature': float(input("溫度 (°C): ")),
            'power': float(input("波浪能量 (W): ")),
            'directionType': input("風向類別 (Cross-shore/Offshore/Onshore): ")
        }
        return input_data
    except ValueError:
        print("請輸入有效的數值！")
        return None
    
def predict_surf_conditions(input_data):
    """
    根據用戶輸入數據進行預測
    """
    if input_data is None:
        print("數據輸入有誤，無法進行預測！")
        return

    # 預處理輸入數據
    input_data = preprocess_input(input_data)

    # 特徵提取
    height_features = np.array([[
        input_data['speed'], input_data['direction'], input_data['pressure'],
        input_data['temperature'], input_data['power'],
        input_data['directionType_Offshore'], input_data['directionType_Onshore']
    ]])

    period_features = np.array([[
        input_data['gust'], input_data['surf_min'], input_data['surf_max'],
        input_data['speed'], input_data['direction'], input_data['pressure'],
        input_data['temperature'], input_data['power'],
        input_data['directionType_Offshore'], input_data['directionType_Onshore']
    ]])

    power_features = np.array([[
        input_data['surf_min'], input_data['surf_max'], input_data['speed'],
        input_data['direction'], input_data['pressure'], input_data['temperature'],
        input_data['power'], input_data['directionType_Offshore'], input_data['directionType_Onshore']
    ]])

    # 預測結果
    swell_height = model_height.predict(height_features)[0]
    swell_period = model_period.predict(period_features)[0]
    swell_power = model_power.predict(power_features)[0]

    # 判斷是否適合衝浪
    offshore = input_data['directionType_Offshore']  # 判斷是否為 Offshore 狀態
    suitable_for_surfing = (
        8 <= swell_period <= 16 or  # 週期 8-16 秒
        (6 <= swell_period < 8 and offshore == 1)  # 週期 6-8 秒 且 Offshore
    )

    # 添加提醒信息
    warnings = []
    if input_data['speed'] > 19:
        warnings.append("風大提醒：風速超過 19 m/s")
    if input_data['temperature'] < 20:
        warnings.append("低溫提醒：溫度低於 20°C")

    return {
        'swell_height': swell_height,
        'swell_period': swell_period,
        'swell_power': swell_power,
        'suitable_for_surfing': suitable_for_surfing,
        'warnings': warnings
    }

# 主程式
if __name__ == "__main__":
    input_data = get_user_input()
    if input_data:
        result = predict_surf_conditions(input_data)

        # 顯示結果
        print('----------------------------------------------')
        print('預測結果')
        print(f"Swell Height: {result['swell_height']:.2f} m")
        print(f"Swell Period: {result['swell_period']:.2f} s")
        print(f"Swell Power: {result['swell_power']:.2f}")
        print('----------------------------------------------')
        if result['suitable_for_surfing']:
            print("適合衝浪！")
        else:
            print("不適合衝浪！")
        print('----------------------------------------------')
        if result['warnings']:
            print("提醒事項：")
            for warning in result['warnings']:
                print(f" - {warning}")