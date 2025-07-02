import pandas as pd
import json

# 1️⃣ Load CSV file
file_path = "extracted_dataprocessing_cv_combined.csv"  # Change to your local file path
df = pd.read_csv(file_path)

# 2️⃣ Convert to JSON in the requested structure
json_output = []

for _, row in df.iterrows():
    json_entry = {
        "trainee": str(row.get("trainee", "")),
        "id": str(row.get("id", "")),
        "학력": row.get("학력", "").strip() if pd.notna(row.get("학력", "")) else "기타의 내용",
        "경력": row.get("경력", "").strip() if pd.notna(row.get("경력", "")) else "기타의 내용",
        "교육이력": row.get("교육이력", "").strip() if pd.notna(row.get("교육이력", "")) else "기타의 내용",
        "자격증": row.get("자격증", "").strip() if pd.notna(row.get("자격증", "")) else "기타의 내용",
        "기타": "기타의 내용"
    }
    json_output.append(json_entry)

# 3️⃣ Save to JSON file for delivery to HR pipeline or MongoDB insertion
output_path = "extracted_dataprocessing_cv_combined_converted.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, ensure_ascii=False, indent=2)

print(f"✅ JSON conversion completed. Saved to {output_path}")
