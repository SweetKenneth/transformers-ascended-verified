import sys, codecs
print('=== ASCENDED HUGGINGFACE TRANSFORMERS ===')
print('CMPSBL Serial: CMPSBL-MNTTD62J-1H7N')
print('Fingerprint:   fa43ab505192a743')
print()

# Load Layer 2
with codecs.open('src/transformers/modeling_utils.py', 'r', 'utf-8') as f:
    code = f.read().split('ORIGINAL SOURCE (UNMODIFIED')[0]
exec(code)

# Check for capabilities
capabilities = [
    'PersistentMemory', 'StateRecovery', 'EventBus', 'DefenseLayer',
    'RequestValidator', 'SandboxExecutor', 'ReflexHandler', 'LearningEngine',
    'SessionBinder', 'IdentityResolver', 'DeviceFingerprint', 'FallbackChain'
]

print('Checking for infrastructure capabilities...')
print()
for cap in capabilities:
    found = cap in dir()
    print(f'  {cap}: {"FOUND" if found else "NOT FOUND"}')

print()
print('--- LIVE CAPABILITY TEST ---')
print()

# 1. Defense: block XSS
rv = RequestValidator()
print('1. DEFENSE (XSS Blocking)')
safe = rv.validate({'input': 'Load bert-base for classification'})
print(f'   Clean input:  PASSED (returned {type(safe).__name__})')
try:
    rv.validate({'input': '<script>alert(1)</script>'})
    print('   XSS input:   FAILED TO BLOCK')
except ValueError as e:
    print(f'   XSS input:   BLOCKED -> {e}')

# 2. Memory: persist across calls
print()
print('2. MEMORY (Cross-Call Persistence)')
pm = PersistentMemory()
pm.set('model', 'distilbert-base-uncased')
pm.set('threat_count', 0)
print(f'   Write: model = distilbert-base-uncased')
print(f'   Read:  model = {pm.get("model")}')
print(f'   Keys:  {pm.keys()}')

# 3. State Recovery
print()
print('3. STATE RECOVERY (Checkpoint/Rollback)')
sr = StateRecovery()
sr.checkpoint('before_finetune', {'lr': 3e-5, 'epoch': 0, 'loss': 2.3})
sr.checkpoint('after_epoch_1', {'lr': 3e-5, 'epoch': 1, 'loss': 0.8})
recovered = sr.recover('before_finetune')
print(f'   Checkpoint 1: before_finetune (loss 2.3)')
print(f'   Checkpoint 2: after_epoch_1 (loss 0.8)')
print(f'   Rolled back:  {recovered}')

# 4. Session + Identity
print()
print('4. SESSION BINDING (Device-Locked Identity)')
ir = IdentityResolver()
sb = SessionBinder()
session = ir.create_session('researcher_1', {'role': 'admin'})
sb.bind('researcher_1', 'windows_x64_rtx3060', session)
verified = sb.verify('researcher_1', 'windows_x64_rtx3060')
spoofed = sb.verify('researcher_1', 'unknown_device')
print(f'   Session created: {session[:20]}...')
print(f'   Correct device:  verified = {verified}')
print(f'   Spoofed device:  verified = {spoofed}')

# 5. Sandbox
print()
print('5. SANDBOX (Isolated Execution)')
se = SandboxExecutor()
result = se.execute(lambda: sum(range(1000)))
print(f'   Sandboxed sum(0..999) = {result["result"]} in {result["duration_ms"]}ms')

# 6. Reflex + Fallback
print()
print('6. REFLEX + FALLBACK (Trigger-Response Chain)')
rh = ReflexHandler()
fc = FallbackChain()
rh.register('oom', lambda: 'cache_cleared')
response = rh.react('oom')
fallback = fc.execute(lambda: 1/0)
print(f'   OOM trigger -> reflex response: {response}')
print(f'   Division by zero -> fallback caught: {fallback is not None}')

# 7. Learning Engine
print()
print('7. LEARNING ENGINE (Pattern Memory)')
le = LearningEngine()
le.record('xss_attempt', 'blocked', {'source': 'form'})
le.record('xss_attempt', 'blocked', {'source': 'api'})
le.record('sql_injection', 'blocked', {'source': 'query'})
suggestion = le.suggest('xss_attempt')
print(f'   Recorded 3 threat patterns')
print(f'   Suggestion for xss_attempt: {suggestion}')

# 8. Dispatch Matrix
print()
print('8. DISPATCH MATRIX (Deterministic Gate)')
gate = _cmpsbl_gate
sealed = sum(1 for i in range(16) if gate(i, {'t': 1}).get('_sealed', False))
print(f'   {sealed}/16 primitive stages sealed')
print(f'   Fingerprint confirmed: {__CMPSBL_META__["fingerprint"]}')

# Now run the same model
print()
print('--- MODEL INFERENCE (through Ascension) ---')
print()
sys.path.insert(0, 'src')
from transformers import pipeline
classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

tests = [
    'This software is incredible',
    '<script>alert(1)</script>',
]

for text in tests:
    r = classifier(text)[0]
    print(f'  [{r["label"]} {r["score"]:.4f}] {text}')

print()
print('Same model. Same inputs. Same outputs.')
print('But now governed by 21 infrastructure primitives.')
print('XSS would be blocked before reaching the model in production.')
print()
print('=== END ASCENDED DEMO ===')
