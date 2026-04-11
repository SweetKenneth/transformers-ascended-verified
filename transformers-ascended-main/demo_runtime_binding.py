import sys
sys.path.insert(0, 'src')

print("=== CMPSBL RUNTIME BINDING PROOF ===\n")

# Load Layer 2
import codecs
with codecs.open('src/transformers/modeling_utils.py', 'r', 'utf-8') as f:
    code = f.read().split('ORIGINAL SOURCE (UNMODIFIED')[0]
exec(code)

# Hook into HuggingFace pipeline
from transformers.pipelines.base import Pipeline
from transformers import pipeline

print("Applying runtime hook...")

original_call = Pipeline.__call__

def wrapped_call(self, *args, **kwargs):
    print("\n[CMPSBL] Intercepted execution")

    pm = PersistentMemory()
    pm.set("last_input", str(args[0]) if args else "unknown")

    rv = RequestValidator()
    try:
        rv.validate({"input": str(args[0])})
    except Exception as e:
        print("[CMPSBL BLOCKED]:", e)
        raise

    result = original_call(self, *args, **kwargs)

    pm.set("last_output", result)
    print("[CMPSBL] Memory written")

    return result

Pipeline.__call__ = wrapped_call

print("Hook applied.\n")

# Run real model
clf = pipeline("sentiment-analysis")

tests = [
    "I love this system",
    "<script>alert(1)</script>"
]

for t in tests:
    try:
        print("Input:", t)
        print("Output:", clf(t))
    except Exception as e:
        print("Blocked:", e)

print("\n=== END RUNTIME PROOF ===")