## 1. Overview
This document outlines the Retrieval-Augmented Generation (RAG) system implemented for the TA/Admin bot in the IITM BS Data Science program.

The bot assists Teaching Assistants (TAs) and Admins by providing accurate answers to queries related to:
- Course grading policies and assessment guidelines
- Managing student inquiries and support requests
- Academic integrity and plagiarism guidelines
- Deadlines, resubmissions, and late penalties
- Handling student complaints and escalations

The bot retrieves relevant policy documents before generating responses to ensure accuracy.

---

## 2. Architecture

### Key Components
1. **Document Loader** – Reads official TA/Admin policies from structured files.
2. **Text Splitter** – Divides documents into smaller retrievable chunks.
3. **Embedding Model** – Converts text chunks into numerical embeddings for search.
4. **Vector Store (FAISS)** – Stores embeddings for efficient retrieval.
5. **Retrieval Mechanism** – Finds the most relevant chunks based on user queries.
6. **LLM (Llama 3.3-70B-Instruct-Turbo)** – Generates responses using retrieved data.

---

## Grading Information

### Quiz Dates:
- **Quiz 1:** February 23, 2025
- **Quiz 2:** No Quiz 2
- **End Term Exam:** April 13, 2025

### Programming Exams (OPPE):
- **OPPE1:** Sunday, March 2, 2025
- **OPPE2:** Sunday, April 6, 2025

### OPPE Slot Allocation:
Depending on eligibility for OPPE1 & OPPE2, students will be allocated one of three slots. Ensure availability on the given dates.

### Eligibility for Bonus:
- The **SCT (System Compatibility Test)** is mandatory for the bonus to be added to the final score.
- Attendance in mock tests alone does **not** qualify for the bonus.

## Eligibility Criteria

### OPPE1:
- Completion of the **OPPE System Compatibility Test (SCT)** is mandatory.
- OPPE1 will **not** be scheduled for students who fail the SCT.

### OPPE2:
- **GrPA (Graded Programming Assignments):** Average of the best **5 out of the first 7** scores must be **≥ 40/100**.
- **Weekly Assessments:** Average of the best **5 out of the first 7** (objective + programming) scores must be **≥ 40/100**.

### End Term Exam:
- The **weekly assessments** (objective + programming) must have an **average score of ≥ 40/100**.

## Final Course Grade Requirements:
- Must attend the **End Term Exam**.
- Must score **≥ 40/100** in at least **one programming exam** (OPPE1 or OPPE2).

## Final Course Score Calculation:
Formula: **Capped at 100**.

Where:
- **GAA1:** Average score in the **best 10 out of 11** graded objective assignments.
- **GAA2:** Average score in the **best 10 out of 11** graded programming assignments.
- **Qz1:** Quiz 1 score (**0** if not attempted).
- **PE1:** OPPE1 score (**0** if not attempted).
- **PE2:** OPPE2 score (**0** if not attempted).
- **F:** Final exam score.

---
