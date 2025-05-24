import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# 모델 로딩
model_name = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# GPU가 있다면 사용, 없으면 CPU 사용
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 디렉토리 설정
dataset_dir = "./dataset"
result_dir = "./results"
os.makedirs(result_dir, exist_ok=True)

# 코드 파일 분석
for filename in os.listdir(dataset_dir):
    if filename.endswith((".js")):
        filepath = os.path.join(dataset_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            # 문자열 읽어오기기
            code = f.read() 

        # 프롬프트 생성
        instruction = """
        You are a security expert. Review the following JavaScript code:

        1. Identify any security vulnerabilities.
        2. Explain why they are vulnerabilities.
        3. Suggest how to fix or rewrite the vulnerable parts.

        ###Code:

        """

        input_text = instruction + code

        # 토크나이징
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length = 2048).to(device)

        # 생성
        outputs = model.generate(**inputs, max_new_tokens=512, pad_token_id=tokenizer.eos_token_id)

        # 디코딩
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # 결과 저장
        output_path = os.path.join(result_dir, filename.replace(".", "_") + "_result.txt")
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(result)

        print("분석 완료")
