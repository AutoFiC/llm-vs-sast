from openai import OpenAI
import os
import json
import re
client = OpenAI(api_key="yourapi")

# 분석 함수 정의
def analyze_code(code_snippet):
    prompt = f"""
You are a security-focused LLM. ONLY return this exact JSON format:
{{
  "vulnerability_count": number,
  "vulnerabilities": [
    {{
      "description": "text",
      "risk": "Low | Medium | High",
      "conceptual_fix": "text",
      "line": number
    }}
  ]
}}

STRICT RULES:
- ONLY output one JSON block. No explanations, no sample input/output.
- Do NOT suggest SQL fixes unless the code is related to databases.
- Ensure the JSON is properly closed.

JavaScript Code:
{code_snippet}
"""

    # GPT-4로 API 호출
    response = client.chat.completions.create(
        model="gpt-4o",  # 혹은 "gpt-4-turbo" 등
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0  # 보안 분석이라 temperature를 낮게 설정
    )

    generated = response.choices[0].message.content.strip()

    # JSON 블록 추출
    try:
        json_data = json.loads(generated)
        return json.dumps(json_data, ensure_ascii=False)
    except json.JSONDecodeError:
        json_matches = re.findall(r'\{[\s\S]*?"vulnerabilities"\s*:\s*\[[\s\S]*?\][\s\S]*?\}', generated)
        if json_matches:
            return json_matches[0]
        else:
            return json.dumps({
                "vulnerability_count": 0,
                "vulnerabilities": [],
                "note": "No valid JSON detected."
            }, ensure_ascii=False)


# 데이터 불러오기
with open("./input_dataset.json", "r", encoding="utf-8") as f:
    code_samples = json.load(f)

# 분석 및 저장
with open("GPT4_results.jsonl", "w", encoding="utf-8") as f_out:
    for sample in code_samples:
        output = analyze_code(sample["input"])
        result = {
            "CVE": sample["CVE"],
            "output": output
        }
        f_out.write(json.dumps(result, ensure_ascii=False) + "\n")

# 결과 확인 출력
with open("GPT4_results.jsonl", "r", encoding="utf-8") as f_out:
    for line in f_out:
        data = json.loads(line)
        print(f"\nCVE: {data.get('CVE')}")
        print("\nOutput (Parsed JSON):")
        try:
            print(json.dumps(json.loads(data["output"]), indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(data["output"])
