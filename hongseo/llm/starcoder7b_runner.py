# Essential Library Ready
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
# Model checkpoint
model_name = "bigcode/starcoderbase-7b"
# tokenizer, model load
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16, resume_download=True)
# prompt write
prompt = """
### Instruction:
You are a security expert. Analyze the following JavaScript code and do the following:

1) Identify the specific lines or parts of the code that contain security vulnerabilities.
2) Explain **clearly why these parts are vulnerable and what risks they pose**.
3) Suggest **conceptual ways to fix or mitigate these vulnerabilities without providing any code**.

**Do NOT include any code snippets or repeated code. Provide only explanations and recommendations.**

### JavaScript Code:
```javascript
const { exec } = require('child_process');\nconst express = require('express');\nconst app = express();\napp.get('/readfile', (req, res) => {\n  const filename = req.query.filename;\n  exec(`cat ${filename}`, (error, stdout, stderr) => {\n    if (error) {\n      res.status(500).send(`Error: ${stderr}`);\n      return;\n    }\n    res.send(stdout);\n  });\n});\napp.listen(3000, () => {\n  console.log('Server running on port 3000');\n});\n
"""
# tokenizer operate
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
# result generation
output = model.generate(
    **inputs,
    max_new_tokens=500,
    do_sample=True,
    eos_token_id=tokenizer.eos_token_id
)
# result print
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text[len(prompt):])
