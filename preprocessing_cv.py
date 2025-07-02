import pandas as pd

# Load CSV file
df = pd.read_csv("dataprocessing_cv.csv")

# Clean column names to remove potential invisible characters or spaces
df.columns = df.columns.str.strip()

# Print columns to debug if KeyError occurs
print(df.columns.tolist())

# Combine columns safely with fallback if column names have changed
df['학력'] = df.get('최종 학위 수준', '') + ' , ' + df.get('출신 학교 수준', '') + ' , ' + df.get('학점', '')
df['경력'] = df.get('총 경력 연수', '') + ' , ' + df.get('직무 연관성', '') + ' , ' + df.get('성과 및 기여도', '')
df['교육이력'] = df.get('전문교육 수료 여부', '') + ' , ' + df.get('기업 내 교육 참여', '') + ' , ' + df.get('자기개발 노력', '')
df['자격증'] = df.get('직무 관련 자격증 (적합도)', '') + ' , ' + df.get('자격증 수준', '') + ' , ' + df.get('자격증 최신성', '')

# Select final columns
extracted_df = df[['trainee', 'id', '학력', '경력', '교육이력', '자격증']]

# Save to CSV
extracted_df.to_csv("extracted_dataprocessing_cv_combined.csv", index=False, encoding='utf-8-sig')

# Preview extracted dataframe
print(extracted_df.head())