import sys
sys.path.insert(0, 'src')

# Load transformers through the ascended modeling_utils
from transformers import pipeline

# Load a small sentiment analysis model
print('Loading model through ascended Layer 2...')
classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

# Run some predictions
tests = [
    "This software is absolutely incredible",
    "The code is broken and nothing works",
    "CMPSBL is cognitive infrastructure for the future",
    "<script>alert('xss')</script> this is a malicious input",
]

print()
print('=== SENTIMENT ANALYSIS (through Ascension) ===')
print()
for text in tests:
    result = classifier(text)
    label = result[0]['label']
    score = result[0]['score']
    print(f'  [{label} {score:.4f}] {text[:60]}')

print()
print('Model loaded and ran through ascended modeling_utils.py')
print('Layer 1 (HuggingFace) handled the ML')
print('Layer 2 (CMPSBL) is governing the infrastructure')
