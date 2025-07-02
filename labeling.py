import pandas as pd

# Load and clean columns
df = pd.read_csv("dataprocessing_cv.csv")
df.columns = df.columns.str.strip()

# Create reusable grading mapping functions for clarity and speed
def map_grade(value, mapping_list, default='E'):
    for keyword, grade in mapping_list:
        if keyword in str(value):
            return grade
    return default

def parse_gpa(value):
    try:
        val = float(value.split('~')[0])
        return 'A' if val >= 4.0 else 'B' if val >= 3.5 else 'C' if val >= 3.0 else 'D' if val >= 2.5 else 'E'
    except:
        return 'E'

# Define grading criteria in compact structures for scalability
grading_criteria = [
    ('학력', '학위 수준 및 전공', '최종 학위 수준', [('박사', 'A'), ('석사', 'B'), ('학사', 'C'), ('전문대', 'D')]),
    ('학력', '출신 학교 수준', '출신 학교 수준', [('최상위권', 'A'), ('상위권', 'B'), ('중상위권', 'C'), ('하위권', 'D')]),
    ('경력', '총 경력 연수', '성과 및 기여도', [('10년', 'A'), ('6', 'B'), ('3', 'C'), ('1', 'D')]),
    ('경력', '직무 연관성', '직무 연관성', [('완전 일치', 'A'), ('유사', 'B'), ('일부 유사', 'C'), ('직무 전환', 'D')]),
    ('경력', '성과 및 기여도', '성과 및 기여도.1', [('수치화', 'A'), ('리드', 'B'), ('성실 근무', 'C'), ('기재 부족', 'D')]),
    ('교육이력', '전문교육 수료 여부', '전문교육 수료 여부', [('최신', 'A'), ('3년 내 2개', 'B'), ('3년 내 1개', 'C'), ('오래된', 'D')]),
    ('교육이력', '기업 내 교육 참여', '기업 내 교육 참여', [('핵심', 'A'), ('정기', 'B'), ('기본', 'C'), ('단기', 'D')]),
    ('교육이력', '자기개발 노력', '자기개발 노력', [('지속적', 'A'), ('관련', 'B'), ('학습', 'C'), ('계획', 'D')]),
    ('자격증', '직무 관련 자격증 적합성', '직무 관련 자격증 (적합도)', [('국가공인', 'A'), ('민간자격증', 'C'), ('무자격증', 'D')]),
    ('자격증', '자격증 수준', '자격증 수준', [('난이도 높', 'A'), ('난이도 중', 'B'), ('기초 수준', 'C'), ('실무 관련성 낮음', 'D')]),
    ('자격증', '자격증 최신성', '자격증 최신성', [('3년 이내', 'A'), ('3~5년', 'B'), ('5년 이상', 'C'), ('오래된', 'D')])
]

records = []
for _, row in df.iterrows():
    trainee = row['trainee']
    id_val = row['id']

    # GPA parsing separately for accurate numeric grading
    gpa_grade = parse_gpa(row.get('학점 성과 및 기여도', ''))
    records.append({'trainee': trainee, 'id': id_val, 'cat': '학력', 'subcat': '학점', 'grade': gpa_grade})

    for cat, subcat, column, mapping in grading_criteria:
        if subcat == '학점':
            continue  # skip because handled by GPA parsing
        grade = map_grade(row.get(column, ''), mapping)
        records.append({'trainee': trainee, 'id': id_val, 'cat': cat, 'subcat': subcat, 'grade': grade})

# Export
result_df = pd.DataFrame(records)
result_df.to_csv("graded_dataprocessing_cv_optimized.csv", index=False, encoding='utf-8-sig')
print(result_df.head())
