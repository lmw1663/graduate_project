import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN

# 데이터 읽기
df = pd.read_csv('pp_on_sale_cars.csv', encoding='utf-8')

# '이름' 열에서 특정 단어 제거
df['이름'] = df['이름'].str.replace('현대 ', '', regex=False)
df['이름'] = df['이름'].str.replace('기아 ', '', regex=False)
df['이름'] = df['이름'].str.replace('KG모빌리티 ', '', regex=False)
df['이름'] = df['이름'].str.replace(r'\d+\.\d+', '', regex=True)  # 예: '2.0'과 같은 배기량 제거
df['이름'] = df['이름'].str.replace(r'\b\d+WD\b', '', regex=True)  # 예: '4WD'와 같은 구동 방식 제거
df['이름'] = df['이름'].str.replace(r'[\(\)]+', '', regex=True)    # 괄호 제거

# 이름 열에 대해 TF-IDF 벡터화
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['이름'])

# 코사인 유사도 계산
cosine_sim = cosine_similarity(tfidf_matrix)

# 음수 값을 방지하기 위해 0~1 사이로 클리핑 후 거리 행렬 생성
distance_matrix = 1 - cosine_sim.clip(0, 1)

# DBSCAN 클러스터링 수행
dbscan = DBSCAN(eps=0.5, min_samples=2, metric='precomputed')
clusters = dbscan.fit_predict(distance_matrix)

# 클러스터 라벨을 데이터프레임에 추가
df['클러스터'] = clusters

# 유사도를 각 이름별로 평균하여 새로운 열 추가
df['유사도'] = cosine_sim.mean(axis=1)

# 클러스터와 유사도를 기준으로 정렬된 전체 데이터 저장
df_sorted = df.sort_values(by=['클러스터', '유사도'], ascending=[True, False])
df_sorted.to_csv('sorted_full_car_data.csv', index=False, encoding='utf-8-sig')

print("전처리 및 정렬된 전체 데이터가 'sorted_full_car_data.csv' 파일에 저장되었습니다.")
