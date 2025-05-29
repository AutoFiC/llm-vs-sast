from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re

# 모델 및 토크나이저 로딩
model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    use_auth_token=True,
)


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

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # 출력
    outputs = model.generate(
        **inputs,
        max_new_tokens=700,
        do_sample=False,
        repetition_penalty=1.2,
        eos_token_id=tokenizer.eos_token_id
    )

    # 출력 후처리
    raw_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    generated = raw_output[len(prompt):].strip()

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
with open("StarCoder_results.jsonl", "w", encoding="utf-8") as f_out:
    for sample in code_samples:
        output = analyze_code(sample["input"])
        result = {
            "CVE": sample["CVE"],
            "output": output
        }
        f_out.write(json.dumps(result, ensure_ascii=False) + "\n")

# 결과 확인 출력
with open("StarCoder_results.jsonl", "r", encoding="utf-8") as f_out:
    for line in f_out:
        data = json.loads(line)
        print(f"\nCVE: {data.get('CVE')}")
        print("\nOutput (Parsed JSON):")
        try:
            print(json.dumps(json.loads(data["output"]), indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(data["output"])
