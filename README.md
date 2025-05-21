# llm-vs-sast

논문을 작성하기 전에 **LLM 모델과 SAST 도구의 성능**을 비교하는 Repository입니다.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python) ![CodeBERT](https://img.shields.io/badge/Code-v0.2.3-green) ![Status](https://img.shields.io/badge/status-developing-orange)


## 🛠 개발 환경
```bash
Language : Python 3.11.x
Virtual Environment : venv
IDE : Visual Studio Code / PyCharm / Jupyter Notebook
Package Manager : pip
Essential Library : requirements.txt
```



## ️☝️ 개발 환경 구축 -> (Windows)
```bash
# Python Version Check
python --version
python3 --version

# 만약 파이썬 버전이 3.11.x가 아닌 경우, 기존 파이썬을 지우지 않고 Python 3.11.x 버전을 추가로 설치합니다.
py -3.11 --version
```
```bash
# Git Clone
git clone https://github.com/AutoFiC/llm-vs-sast.git
cd llm-vs-sast
```
```bash
# Directory Create
mkdir "본인이름"
cd "본인이름"
```
```bash
# Virtual Environment Create
python -m venv .venv
python3 -m venv .venv
py -3.11 venv .venv
```
```bash
# Activate Virtual Environment
.venv\Scripts\activate
```
```bash
# Essential Library install
pip install -r requirements.txt
```


## ✨ 개발 환경 구축 -> (Mac/Ubuntu)
```bash
# Python Version Check
python --version
python3 --version

# 만약 파이썬 버전이 3.11.x가 아닌 경우, 기존 파이썬을 지우지 않고 Python 3.11.x 버전을 추가로 설치합니다.
brew install python@3.11
```
```bash
# Git Clone
git clone https://github.com/AutoFiC/llm-vs-sast.git
cd llm-vs-sast
```
```bash
# Directory Create
mkdir "본인이름"
cd "본인이름"
```
```bash
# Virtual Environment Create
python -m venv .venv
python3 -m venv .venv
python3.11 -m venv .venv
```
```bash
# Activate Virtual Environment
.venv/bin/activate
```
```bash
# Essential Library install
pip install --upgrade pip
pip install -r requirements.txt
```
