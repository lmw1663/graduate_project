import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('on_sale_cars.csv')

# 1. 불필요한 열 제거
df.drop(columns=['Unnamed: 0.1','Unnamed: 0', '링크'], inplace=True)

# 2. 연식 데이터 변환 (연도에서 뒤 두 자리만 추출하여 1을 더한 후 저장, 결측값은 0으로 채움)
df['연식'] = df['연식'].str.extract(r'20(\d{2})')[0].fillna(0).astype(int) + 1

# 3.주행거리 데이터 변환
# 1. 주행거리에서 'mi'가 있는지 확인하여 별도의 열로 저장
df['is_miles'] = df['주행거리'].str.contains(' mi')

# 2. 쉼표와 공백을 제거하고, 'km'와 'mi' 단위 문자열 제거
df['주행거리'] = df['주행거리'].str.replace(',', '').str.replace(' km', '').str.replace(' mi', '')

# 3. 숫자형으로 변환
df['주행거리'] = pd.to_numeric(df['주행거리'], errors='coerce')

# 4. 'mi'인 경우 1.60934를 곱해 km로 변환
df['주행거리'] = df['주행거리'] * df['is_miles'].map({True: 1.60934, False: 1})

# 필요 시 is_miles 열 삭제
df.drop(columns=['is_miles'], inplace=True)

# 5. - 배기량: cc 및 특수 문자 제거 후 숫자로 변환
df['배기량'] = df['배기량'].str.extract(r'(\d+,\d+|\d+)').iloc[:, 0].str.replace(',', '').astype(float)

# 6. - 가격 변환: '만원' 제거하고 숫자로 변환
df = df.dropna(subset=['가격'])
# 가격과 관련된 값들이 아니면 전부 제거
df = df[~df['가격'].isin(['[보류]', '0원', '[가격상담]','[계약]'])]

df['가격'] = df['가격'].apply(lambda x: x.replace('만원', '0000').replace(',', '') if isinstance(x, str) else None)
df['가격'] = pd.to_numeric(df['가격'], errors='coerce')

# 결측값 처리
df['신차대비가격'] = df['신차대비가격'].replace(['준비중', '[보류]'], None)

# 3. 옵션 열: '무'를 0으로, '유'를 1로 변환하고 결측값을 0으로 처리한 후 int로 변환
option_columns = [col for col in df.columns if '옵션_' in col]
df[option_columns] = df[option_columns].replace({'무': 0, '유': 1}).fillna(0).astype(int)

# 보험이력등록 열: '등록'을 1로, '미등록'을 0으로 변환하고 결측값을 0으로 채운 후 int로 변환
df['보험이력등록'] = df['보험이력등록'].replace({'등록': 1, '미등록': 0}).fillna(0).astype(int)

# CSV 파일로 저장
df.to_csv('pp_on_sale_cars.csv', index=False)
