import pandas as pd

# 1. csv 불러오기
def load_data(filepath: str = "ChatbotData.csv"):
    # 학습용 CSV(Q/A) -> 리스트 변환
    data = pd.read_csv(filepath)
    return data["Q"].tolist(), data["A"].tolist()

# 2. 레벤슈타인 거리
def levenshtein(a: str, b: str) -> int:
    # 각 문자열 길이저장
    m, n = len(a), len(b)
    # 첫 번째 행 초기화
    dp = list(range(n + 1))
    
    # 동적 계획법 적용
    for i, ca in enumerate(a, 1):
        prev, dp[0] = i - 1, i
        
        for j, cb in enumerate(b, 1):
            prev, dp[j] = dp[j], min(
                dp[j] + 1,              # 삭제
                dp[j-1] + 1,            # 삽입
                prev + (ca != cb)       # 치환(1 or 0)
            )
    return dp[-1]

# 3. 챗봇 클래스
class Chatbot:
    def __init__(self, filepath: str = "ChatbotData.csv"):
        self.questions, self.answers = load_data(filepath)
    
    def find_best_answer(self, user_input: str) -> str:
        # 입력-질문 간 레벤슈타인 거리계산
        distances = [levenshtein(user_input, q) for q in self.questions]
        
        # 최소거리값 추출
        min_dist = min(distances)
        
        # 최소 거리와 같은 값을 가진 모든 인덱스 저장
        ties = [i for i, d in enumerate(distances) if d == min_dist]
        
        # 같은 거리일 경우 질문 길이가 가장 짧은 인덱스를 선택
        best_idx = min(ties, key=lambda i: len(self.questions[i]))
        
        return self.answers[best_idx]
    
# 4. cli 인터페이스
if __name__ == "__main__":
    bot = Chatbot()
    
    print("Levenshtein Chatbot (exit/quit 입력 시 종료)")
    
    while True:
        user = input("YOU > ").strip()
        
        if user.lower() in {"exit", "quit"}:
            break
        
        print("BOT > ", bot.find_best_answer(user))