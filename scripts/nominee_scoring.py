"""
Nominee Scoring Project
-----------------------
This project uses GPT-powered analysis to score nominees across defined attributes
and categories based on long-form reviews. The script reads input from Excel,
generates unbiased comparative scores and justifications, and outputs results
to a structured Excel file.

Sanitized version for GitHub — no real PDO data is included.
"""

import os
import json
import pandas as pd
from dotenv import load_dotenv
import openai

# === 1. Load API key (ensure you have a .env file with OPENAI_API_KEY) ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise RuntimeError("⚠️ OPENAI_API_KEY not set in .env file")

# === 2. Define evaluation criteria ===
criteria_data = {
    "Business Performance": {
        "Delegates": 2.5,
        "Inspires and Motivates": 2.5,
        "Contributes to Lean": 2.5,
        "Personal Impact": 2.5,
        "Weight": 0.333
    },
    "People Development": {
        "Regularly Engages": 2,
        "Coaches & Mentors": 2,
        "Gives Constructive Feedback": 2,
        "Provides Opportunities in Closing Competency gaps": 2,
        "Encourages Staff Mobility": 2,
        "Weight": 0.333
    },
    "Innovation in People Development": {
        "Goes ‘out of norm’ in developing individuals": 5,
        "Made an External Impact": 5,
        "Weight": 0.333
    }
}

# Lookup maps
attribute_category = {}
attribute_max_score = {}
category_weight = {}

for category, attrs in criteria_data.items():
    category_weight[category] = attrs["Weight"]
    for attr, val in attrs.items():
        if attr != "Weight":
            attribute_category[attr] = category
            attribute_max_score[attr] = val

# === 3. Load dummy input file ===
INPUT_PATH = "./data/reviews_long_dummy.xlsx"
OUTPUT_PATH = "./outputs/processed_output_dummy.xlsx"

df = pd.read_excel(INPUT_PATH)
df["Category"]  = df["Attribute"].map(attribute_category)
df["Max Score"] = df["Attribute"].map(attribute_max_score)
df = df.dropna(subset=["Category", "Max Score"]).reset_index(drop=True)

# === 4. Process each attribute with GPT ===
def extract_json_array(text: str, attr_name: str):
    try:
        start, end = text.index('['), text.rindex(']') + 1
        return json.loads(text[start:end])
    except Exception:
        print(f"⚠️ Failed to parse GPT output for {attr_name}")
        return []

comparative_records = []

for attr, group in df.groupby("Attribute"):
    max_score = attribute_max_score[attr]
    category  = attribute_category[attr]

    snippet = "\n\n".join(
        f"Nominee: {row.Nominee}\nReview: {row.Summary}"
        for _, row in group.iterrows()
    )

    prompt = f"""
You are an experienced HR evaluator. Compare nominees for the attribute "{attr}".
- Assign scores between 1 and {max_score}.
- Provide comparative justifications using phrases like "Compared to..." or "Less impactful than...".
- Respond in JSON format:
[
  {{ "Nominee": "Name", "Score": 2.0, "Justification": "..." }}
]
Reviews:
{snippet}
"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1500
    )
    text = response.choices[0].message.content.strip()
    scored_list = extract_json_array(text, attr_name=attr)

    for item in scored_list:
        comparative_records.append({
            "Nominee": item.get("Nominee", "").strip(),
            "Attribute": attr,
            "Category": category,
            "Score": float(item.get("Score", 0)),
            "Max Score": max_score,
            "Justification": item.get("Justification", "").strip(),
            "Weighted Score": round(float(item.get("Score", 0)) * category_weight[category], 2)
        })

# === 5. Aggregate results ===
comp_df = pd.DataFrame(comparative_records)

cat_df = (
    comp_df.groupby(["Nominee", "Category"], as_index=False)["Score"]
    .sum().rename(columns={"Score":"Raw Score"})
)
cat_df["Weight"] = cat_df["Category"].map(category_weight)
cat_df["Weighted Score"] = (cat_df["Raw Score"] * cat_df["Weight"]).round(2)

total_df = (
    cat_df.groupby("Nominee", as_index=False)["Weighted Score"]
    .sum().rename(columns={"Weighted Score":"Total Weighted Score"})
)

# === 6. Export to Excel ===
with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
    comp_df.to_excel(writer, sheet_name="Attribute Scores", index=False)
    cat_df.to_excel(writer, sheet_name="Category Scores", index=False)
    total_df.to_excel(writer, sheet_name="Summary", index=False)

print(f"✅ Nominee scoring complete. Results saved to {OUTPUT_PATH}")
