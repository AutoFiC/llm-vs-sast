import glob
import os
import json
from tree_sitter import Language, Parser

# 빌드할 언어들 (필요한 경우만!)
Language.build_library(
    'build/my-languages.so',
    [
        'tree-sitter-javascript'
    ]
)

# 언어별 파서 준비
LANGUAGES = {
    'js': Language('build/my-languages.so', 'javascript')
}


def get_language_by_extension(file_extension):
    return LANGUAGES.get(file_extension, None)


def parse_code(source_code, language):
    parser = Parser()
    parser.set_language(language)
    parsed = parser.parse(bytes(source_code, "utf8"))
    return parsed


# 확장자별로 파일 찾기
all_files = glob.glob("CVE-*.*")  # js, py 등 모두 찾기
new_results = []

for file_path in all_files:
    file_extension = file_path.split('.')[-1]
    language = get_language_by_extension(file_extension)

    if not language:
        print(f"지원하지 않는 확장자: {file_extension}. 스킵.")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = parse_code(code, language)
    result = {
        "CVE": file_path.split('.')[0],
        "instruction": "Detect whether the following code contains vulnerabilities.",
        "input": code
    }
    new_results.append(result)

# 기존 results.json 불러오기
all_results = []
if os.path.exists('results.json'):
    with open('results.json', 'r', encoding='utf-8') as existing_file:
        try:
            all_results = json.load(existing_file)
        except json.JSONDecodeError:
            all_results = []

# 새 결과 추가
all_results.extend(new_results)
with open('results.json', 'w', encoding='utf-8') as output_file:
    json.dump(all_results, output_file, indent=4, ensure_ascii=False)

print("결과가 results.json 파일에 추가 저장되었습니다.")
