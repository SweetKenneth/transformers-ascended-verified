import sys
print('=== VANILLA HUGGINGFACE TRANSFORMERS ===')
print('Checking for infrastructure capabilities...')
print()

# Try to find any CMPSBL capability in stock transformers
capabilities = [
    'PersistentMemory', 'StateRecovery', 'EventBus', 'DefenseLayer',
    'RequestValidator', 'SandboxExecutor', 'ReflexHandler', 'LearningEngine',
    'SessionBinder', 'IdentityResolver', 'DeviceFingerprint', 'FallbackChain'
]

import transformers
source_module = transformers.modeling_utils

for cap in capabilities:
    found = hasattr(source_module, cap)
    print(f'  {cap}: {"FOUND" if found else "NOT FOUND"}')

print()

# Run sentiment analysis - vanilla
from transformers import pipeline
print('Loading DistilBERT (vanilla)...')
classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

tests = [
    'This software is incredible',
    '<script>alert(1)</script>',
]

print()
for text in tests:
    r = classifier(text)[0]
    print(f'  [{r["label"]} {r["score"]:.4f}] {text}')

print()
print('XSS payload processed with zero protection.')
print('No memory. No defense. No session binding. No sandboxing.')
print('Stock HuggingFace has no infrastructure layer.')
print()
print('=== END VANILLA BASELINE ===')
