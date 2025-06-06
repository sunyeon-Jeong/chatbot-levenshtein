def load_data(filepath: str = "ChatbotData.csv"):
    # 학습용 CSV(Q/A) -> 리스트 변환
    data = pd.read_csv(filepath)
    return data["Q"].tolist(), data["A"].tolist()