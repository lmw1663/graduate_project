import pandas as pd
import matplotlib.pyplot as plt


# 데이터 읽기
df = pd.read_csv('pp_on_sale_cars.csv', encoding='utf-8')
# # 그래프 그리기 위한 열 목록
columns_to_plot = ['연식', '주행거리', '배기량', '가격']
# 숫자형으로 변환이 불가능한 값 확인

# # 히스토그램과 박스플롯 시각화
for col in columns_to_plot:
    plt.figure(figsize=(14, 5))

    # 히스토그램
    plt.subplot(1, 2, 1)
    plt.hist(df[col].dropna(), bins=30, edgecolor='black', color='skyblue')
    plt.title(f'{col} Distribution Histogram')
    plt.xlabel(col)
    plt.ylabel('Frequency')

    # 박스플롯
    plt.subplot(1, 2, 2)
    plt.boxplot(df[col].dropna(), vert=False)
    plt.title(f'{col} Distribution Boxplot')
    plt.xlabel(col)

    plt.tight_layout()
    plt.show()
