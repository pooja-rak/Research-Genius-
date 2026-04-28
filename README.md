# Research-Genius-AI

ResearchGenius AI is an intelligent research assistant designed to help students, researchers, and academicians identify unique research topics, discover research gaps, and improve the quality of their work using AI-powered analysis.

---

## Features

### 1. Topic Scanner
- Converts user input into semantic vectors using Sentence-BERT
- Compares with existing research papers
- Calculates **originality score**
- Helps avoid duplicate or overused topics

### 2. Gap Suggester
- Uses TF-IDF to identify rare but important terms
- Applies K-Means clustering to group research areas
- Suggests **research gaps** for innovation

### 3. Abstract Analyzer *(if included)*
- Evaluates clarity, keywords, and structure
- Suggests improvements for better readability

### 4. Smart Suggestions
- Recommends:
  - Better keywords
  - Research directions
  - Improvements in topic framing

---

## Tech Stack

- **Frontend:** Streamlit / HTML / CSS (based on your implementation)
- **Backend:** Python
- **Libraries:**
  - SentenceTransformers (BERT)
  - Scikit-learn (TF-IDF, KMeans)
  - Pandas, NumPy
- **API (optional):**
  - Semantic Scholar API

---

## Project Structure

```

ResearchGenius-AI/
│── app.py
│── models/
│   ├── topic_scanner.py
│   ├── gap_suggester.py
│── data/
│── utils/
│── requirements.txt
│── README.md

````

---

## Installation

```bash
git clone https://github.com/your-username/researchgenius-ai.git
cd researchgenius-ai
pip install -r requirements.txt
````

---

## Usage

```bash
streamlit run app.py
```

Then open in browser:

```
http://localhost:8501
```

---

## Example Input

**Topic:**

```
Student Performance Prediction using Machine Learning
```

**Output:**

* Originality Score: 72%
* Suggested Gaps:

  * Lack of emotional/mental health factors
  * Missing real-time data analysis
  * Limited personalization

---

## Outcomes of the Project

* Helps researchers **validate topic uniqueness**
* Reduces time spent in manual literature review
* Encourages **innovative research ideas**
* Identifies **hidden research gaps**
* Improves quality of academic writing
* Acts as a **beginner-friendly research assistant**

---

## Future Enhancements

* Integration with more research databases
* Full research paper generator
* Citation suggestions
* AI-powered plagiarism detection
* Multi-language support

---

## Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

## Author

Developed by Pooja Rajaram MCA Student | Aspiring Machine Learning Engineer

```

