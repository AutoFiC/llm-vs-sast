# Essential Library
from tree_sitter import Language, Parser
import json
# Build Language Library (In this project > javascript)
Language.build_library(
  'build/my-languages.so',
  [
    'tree-sitter-javascript'
  ]
)

# tree-sitter-javascript will used!
JAVASCRIPT_LANGUAGE = Language('build/my-languages.so', 'javascript')

# Code Parser and adapt
parser = Parser()
parser.set_language(JAVASCRIPT_LANGUAGE)

# do parsing code
def parse_code(source_code):
    parsed = parser.parse(bytes(source_code, "utf8"))
    return parsed

# basic bad code
code = """\
const { exec } = require('child_process');
const express = require('express');
const app = express();
app.get('/readfile', (req, res) => {
  const filename = req.query.filename;
  exec(`cat ${filename}`, (error, stdout, stderr) => {
    if (error) {
      res.status(500).send(`Error: ${stderr}`);
      return;
    }
    res.send(stdout);
  });
});
app.listen(3000, () => {
  console.log('Server running on port 3000');
});
"""

# run parsing function
tree = parse_code(code)

# result will return like this
result = {
    "instruction": "Detect whether the following code contains vulnerabilities.",
    "input": code,
    "output": 0,
    "idx": 19066
}

# like json
print(json.dumps(result, indent=4))

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 취약점을 학습시키고 어떤 부분이 취약한지 알아낼 수 있도록 학습 진행
# training_sample = {
#     "instruction": "Analyze the code and explain any security vulnerabilities.",
#     "input": """\
#
# """,
#     "output": "This code is vulnerable to command injection. It directly inserts user-controlled input into a shell command using exec(). An attacker could inject additional commands such as `; rm -rf /`."
# }

# 취약한 부분만 학습시키면 안되고, 안전한 코드도 학습을 진행
# training_sample = {
#     "instruction": "Analyze the code and explain any security vulnerabilities.",
#     "input": """\
#
# """,
#
#     "output": "This code is relatively safe as it does not execute shell commands. However, if the filename is not validated, it could allow access to unintended files (path traversal)."
# }

# 이후 주어진 코드에서 어느 부분이 안전하지 않은지 설명하도록 하는 코드 (취약한지/취약한 라인/설명 작성)
# {
#   "instruction": ""Analyze the code. If it contains a vulnerability, return whether it is vulnerable, the line numbers where vulnerabilities exist, and a short explanation of the issue."",
#   "input": "const { exec } = require('child_process');\nconst userInput = req.query.filename;\nexec(`cat ${userInput}`, ... );",
#   "output": {
#     "vulnerable": ?,
#     "vulnerable_lines": ?,
#     "explanation": "?"
#   }
# }
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 만약 취약한 코드와 안전한 코드를 학습하고 코드를 수정하는 알고리즘의 경우 학습을 진행한다면 (output에서 왜 취약한지 설명해야됨)
# training_sample = {
#     "instruction": "Compare the two code snippets and explain which one contains a vulnerability and why.",
#     "input": {
#         "insecure_code": """\
#
# """,
#
#         "secure_code": """\
# """
#     },
#     "output": "The first code uses exec with unsanitized user input, allowing command injection. The second code avoids this by using fs.readFile and sanitizing the file path.",
#     "idx": 10001
# }

# 취약한 코드를 보고, 수정하는 역할을 함
# {
#   "instruction": "Given some code, determine if it is vulnerable. If it is, return a secure version and explain what was fixed.",
#   "input": "const { exec } = require('child_process');\nconst userInput = req.query.filename;\nexec(`cat ${userInput}`, (err, stdout, stderr) => {\n  res.send(stdout);\n});",
#   "output": ?
# }
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
