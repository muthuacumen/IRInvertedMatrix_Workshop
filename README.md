
# 🧑‍🏫 NLP Workshop: IR Inverted Matrix

Developed by: David Espinosa, September 2025
Completed by: Muthu, March 2026

This repository contains the **Natural Language Processing Workshop** with:
- Active learning notebook (`IR_InvertedMatrix_Workshop.ipynb`)
- Automated submission script (`utils/submit_assignment.py`)
- Validation + scoring (`utils/validate_notebook.py`)
- Configurable requirements (`config/required_items.json`)
- Auto-generated gradebook (`submissions_log.csv`)

---

## 🎓 Student Instructions (Quick Start)
1. **Fork & Clone the Repo**
   ```bash
   git clone https://github.com/muthuacumen/IRInvertedMatrix_Workshop.git
   cd IRInvertedMatrix_Workshop
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Work on the Notebook**
   - Open: `IR_InvertedMatrix_Workshop.ipynb`
   - Fill all Markdown placeholders (no `TODO` left)
   - Implement required functions (e.g., `build_inverted_index`, `query_processor`)
   - Run all code cells

4. **Submit Your Work**
   Run in the last cell:
   ```python
   !python utils/submit_assignment.py --notebook IR_InvertedMatrix_Workshop.ipynb --student_id "team1"
   ```

   ✅ If valid → notebook is committed & pushed to `submissions/team1`  
   ❌ If errors → fix and resubmit  

5. **Checklist Before Submitting**
   - [ ] No TODOs remain in Markdown  
   - [ ] All required functions implemented  
   - [ ] Notebook runs top-to-bottom without errors  

---

## 🧑‍🏫 Instructor Instructions (Quick Start)
1. **Configure Requirements**
   Edit `config/required_items.json`:
   ```json
   {
     "required_functions": {
       "build_inverted_index": {
         "test_input": [["this is a doc", "this doc is about nlp"]],
         "expected_type": "dict",
         "points": 5
       },
       "query_processor": {
         "test_input": ["doc", {"doc1": [0], "doc2": [1]}],
         "expected_type": "list",
         "points": 5
       }
     },
     "required_markdown": {
       "Introduction": 2,
       "Reflection": 3
     }
   }
   ```

2. **Scaffold Students**
   - Students fork the repo & complete the notebook  
   - Dependencies: `nbformat`, `gitpython`  

3. **Collect Submissions**
   - Fetch all branches:  
     ```bash
     git fetch --all
     ```
   - Review gradebook:  
     ```bash
     cat submissions_log.csv
     ```

   Example log:
   ```csv
   timestamp,student_id,notebook,score,max_score,status
   2025-09-08T14:22:01,team1,IR_InvertedMatrix_Workshop.ipynb,8,10,✅ Passed
   2025-09-08T14:25:12,team2,IR_InvertedMatrix_Workshop.ipynb,6,10,❌ Failed
   ```

---

## ✅ Features
- Automatic validation of Markdown + code answers  
- Quick tests for required functions  
- Point-based scoring with feedback  
- Submissions logged in `submissions_log.csv`  
- Final work pushed to `submissions/<team_id>` branches  

---

📌 For a detailed step-by-step guide, see:
- [Student Instructions Notebook](Student_Instructions_Workshop.ipynb)
