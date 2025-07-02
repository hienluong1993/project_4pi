import pandas as pd

# Load and clean columns
df = pd.read_csv("dataprocessing_cv.csv")
df.columns = df.columns.str.strip()

records = []

# Improved grading function to avoid substring collision (e.g., '중상위권' vs '상위권')
def grade_by_keywords(value, mapping):
    value = str(value)
    # Sort mappings by keyword length descending to prioritize longer, more specific keywords
    mapping_sorted = sorted(mapping, key=lambda x: len(x[0]), reverse=True)
    for keyword, grade in mapping_sorted:
        if keyword in value:
            return grade
    return 'E'

grading_rules = [
    ('학력', '학위 수준 및 전공', '최종 학위 수준', [('박사', 'A'), ('석사', 'B'), ('학사', 'C'), ('전문대', 'D'), ('고졸', 'E'), ('고졸 이하', 'E')]),
    ('학력', '출신 학교 수준', '출신 학교 수준', [('최상위권', 'A'), ('중상위권', 'C'), ('상위권', 'B'), ('하위권', 'D'), ('무인증', 'E'), ('무인증 교육기관', 'E')]),
    ('경력', '총 경력 연수', '성과 및 기여도', [('10년', 'A'), ('6-9년', 'B'), ('6~9년', 'B'), ('3-5년', 'C'), ('1-2년', 'D'), ('1~2년', 'D'), ('1년 미만', 'E')]),
    ('경력', '직무 연관성', '직무 연관성', [('완전 일치', 'A'), ('유사 직무 다수', 'B'), ('일부 유사', 'C'), ('직무 전환', 'D'), ('무관한', 'E'), ('무관한 분야', 'E')]),
    ('경력', '성과 및 기여도', '성과 및 기여도.1', [('수상', 'A'), ('수치화', 'A'), ('리드', 'B'), ('우수 성과', 'B'), ('성실 근무', 'C'), ('무평가', 'C'), ('기재 부족', 'D'), ('관련 정보 없음', 'E')])
]

# GPA parsing with E criteria explicitly
for _, row in df.iterrows():
    trainee = row['trainee']
    id_val = row['id']

    try:
        gpa_val = float(str(row.get('학점', '')).split('~')[0].strip())
        if gpa_val >= 4.0:
            gpa_grade = 'A'
        elif 3.5 <= gpa_val <= 3.99:
            gpa_grade = 'B'
        elif 3.0 <= gpa_val <= 3.49:
            gpa_grade = 'C'
        elif 2.5 <= gpa_val <= 2.99:
            gpa_grade = 'D'
        elif gpa_val <= 2.49:
            gpa_grade = 'E'
        else:
            gpa_grade = 'E'
    except:
        gpa_grade = 'E'
    records.append({'trainee': trainee, 'id': id_val, 'cat': '학력', 'subcat': '학점', 'grade': gpa_grade})

    for cat, subcat, col, mapping in grading_rules:
        grade = grade_by_keywords(row.get(col, ''), mapping)
        records.append({'trainee': trainee, 'id': id_val, 'cat': cat, 'subcat': subcat, 'grade': grade})

# Export results
pd.DataFrame(records).to_csv("graded_dataprocessing_cv_final.csv", index=False, encoding='utf-8-sig')
