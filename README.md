# llm-vs-sast

논문을 작성하기 전에 **LLM 모델과 SAST 도구의 성능**을 비교하는 Repository입니다.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python) ![CodeBERT](https://img.shields.io/badge/CodeBERT-v0.2.3-green) ![Status](https://img.shields.io/badge/status-developing-orange)


## 🛠 개발 환경
```bash
🧑🏻‍💻 Language : Python 3.11.x
🔭 Virtual Environment : venv
👾 IDE : Visual Studio Code / PyCharm / Jupyter Notebook
📦 Package Manager : pip
🌟 Essential Library : requirements.txt
```



## ️🥇 개발 환경 구축 -> (Windows)
```bash
# Python Version Check
python --version
python3 --version
# 만약 파이썬 버전이 3.11.x가 아닌 경우, 기존 파이썬을 지우지 않고 Python 3.11.x 버전을 추가로 설치합니다.
py -3.11 --version

# Git Clone
git clone https://github.com/AutoFiC/llm-vs-sast.git
cd llm-vs-sast

# Directory Create
mkdir "본인이름"
cd "본인이름"

# Virtual Environment Create
python -m venv .venv
python3 -m venv .venv
py -3.11 venv .venv

# Activate Virtual Environment
.venv\Scripts\activate

# Essential Library install
pip install -r requirements.txt
```


## 🥈 개발 환경 구축 -> (Mac/Ubuntu)
```bash
# Python Version Check
python --version
python3 --version
# 만약 파이썬 버전이 3.11.x가 아닌 경우, 기존 파이썬을 지우지 않고 Python 3.11.x 버전을 추가로 설치합니다.
brew install python@3.11

# Git Clone
git clone https://github.com/AutoFiC/llm-vs-sast.git
cd llm-vs-sast

# Directory Create
mkdir "본인이름"
cd "본인이름"

# Virtual Environment Create
python -m venv .venv
python3 -m venv .venv
python3.11 -m venv .venv

# Activate Virtual Environment
source .venv/bin/activate

# Essential Library install
pip install --upgrade pip
pip install -r requirements.txt
```

## 🥉 디렉토리 구성
```
llm-vs-sast
├─ hongseo
│  ├─ 1. Get Datasets (데이터 준비 과정)
│  │  └─ Vulnerability_Data_Original.zip (전처리 이전 데이터-115개 개별 파일)
│  ├─ 2. javascript_cve_parsing (데이터 수집 과정)
│  │  ├─ CVE-crawling-github.py (CVE 크롤링 후 github 레퍼런스만 추출)
│  │  └─ README.md
│  ├─ 3. Preprocessing (데이터 전처리 과정)
│  │  ├─ Javascript-to-AST.py (Javascript -> AST로 변환)
│  │  └─ tree-sitter-javascript (AST 변환 라이브러리)
│  ├─ 4. Model Test (테스트 과정)
│  │  ├─ Input_data
│  │  │  ├─ function_count_summary.csv (CVE별 함수 개수)
│  │  │  └─ input_dataset.json (전처리된 데이터)
│  │  └─ Model test code (모델 실험 코드)
│  │     ├─ Gpt4_test.py
│  │     └─ Meta_llama_test.py
│  └─ 5. Results (결론)
│     ├─ Cleansing_Metrics.ipynb (최종 모델 결과 병합 및 성능 평가)
│     ├─ Final Results (최종 모델 결과 병합)
│     │  ├─ Result.csv
│     │  └─ Result.xlsx
│     └─ Model Results (각 모델별 결과값 .jsonl)
│        ├─ results_gpt3.5.jsonl
│        ├─ results_gpt4.jsonl
│        ├─ results_llama3-8b.jsonl
│        ├─ results_mistral.jsonl
│        └─ results_semgrep.jsonl
├─ README.md
└─ requirements.txt
```
