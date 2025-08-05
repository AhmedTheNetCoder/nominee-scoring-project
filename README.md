# Nominee Scoring Project

This project demonstrates an AI-powered framework for evaluating nominees fairly and transparently across multiple attributes and categories.  
It was developed during my Eidaad training program at PDO, using GPT-4o to perform comparative analysis of long-form nominee reviews.  
**Note:** All data included in this repository is dummy data for demonstration purposes only.

---

## 📌 Overview
The Nominee Scoring Project automates the evaluation of award nominees based on structured reviews.  
Using GPT-4o, the system compares nominees for each attribute, assigns unbiased scores, and provides comparative justifications.  
The results are aggregated into a multi-sheet Excel report for HR leadership decision-making.

---

## 🚀 Features
- Evaluates nominees across categories:
  - **Business Performance**
  - **People Development**
  - **Innovation in People Development**
- Uses GPT-powered comparative scoring to minimize human bias.
- Provides detailed justifications for each score.
- Aggregates results by category and calculates total weighted scores.
- Outputs results into an Excel file with three sheets:
  - **Attribute Scores**
  - **Category Scores**
  - **Summary**

---

## 🔄 Pipeline
1. **Input Data**  
   - Reviews provided in Excel format (`reviews_long_dummy.xlsx`)  
   - Columns: `Nominee`, `Attribute`, `Summary`

2. **Criteria Setup**  
   - Maximum scores and weights defined for each category and attribute.

3. **Comparative Scoring**  
   - GPT-4o model reads nominee reviews per attribute.
   - Assigns scores (e.g., 1.5, 2.0, etc.) with specific justifications.

4. **Aggregation**  
   - Scores grouped by category and weighted according to importance.
   - Final total weighted scores calculated for each nominee.

5. **Report Generation**  
   - Results exported into `processed_output_dummy.xlsx` with 3 sheets:
     - Attribute Scores
     - Category Scores
     - Summary

---

## 📊 Example Output

### Attribute Scores (Sample)

| Nominee     | Attribute                          | Score | Justification                                    |
|-------------|------------------------------------|-------|------------------------------------------------|
| Ali Ahmed   | Delegates                          | 2.3   | Delegated tasks effectively, more impactful... |
| Sara Khalid | Coaches & Mentors                  | 1.9   | Mentored juniors regularly, though less broad |
| John Smith  | Made an External Impact            | 4.7   | Introduced impactful initiative compared...    |

📂 The full output can be found in `outputs/processed_output_dummy.xlsx`.

---

## 🛠 Requirements

### Python Libraries
Install required dependencies:
```bash
pip install pandas openpyxl python-dotenv openai
