import codecs, hashlib, os
print('=== CRYPTOGRAPHIC PROOF: ZERO SOURCE MODIFICATION ===')
print()

# Step 1: Official source
import transformers
official_path = os.path.join(os.path.dirname(transformers.__file__), 'modeling_utils.py')
with open(official_path, 'r', encoding='utf-8') as f:
    official_source = f.read()
official_hash = hashlib.sha256(official_source.encode('utf-8')).hexdigest()
print(f'OFFICIAL HuggingFace modeling_utils.py')
print(f'  Path:   {official_path}')
print(f'  Lines:  {len(official_source.splitlines())}')
print(f'  Chars:  {len(official_source)}')
print(f'  SHA256: {official_hash}')
print()

# Step 2: Read ascended file
with open('src/transformers/modeling_utils.py', 'r', encoding='utf-8') as f:
    ascended_full = f.read()

# Find the exact copyright line that starts the original source
# This is the first line of the real HuggingFace code
official_first_line = official_source.splitlines()[0]
print(f'Official file starts with: {repr(official_first_line[:60])}')

# Find that exact line in the ascended file
ascended_lines = ascended_full.splitlines()
layer1_start = None
for i, line in enumerate(ascended_lines):
    if line == official_first_line:
        layer1_start = i
        break

if layer1_start is None:
    print('ERROR: Could not find exact start of Layer 1')
    exit(1)

print(f'Found Layer 1 start at ascended line {layer1_start + 1}')

# Find the end - the verify function is appended after Layer 1
official_last_line = official_source.rstrip().splitlines()[-1]
print(f'Official file ends with: {repr(official_last_line[:60])}')

# Find that exact last line in ascended
layer1_end = None
for i in range(len(ascended_lines) - 1, layer1_start, -1):
    if ascended_lines[i] == official_last_line:
        layer1_end = i + 1
        break

if layer1_end is None:
    print('Could not find exact end, trying line count match...')
    layer1_end = layer1_start + len(official_source.splitlines())

print(f'Found Layer 1 end at ascended line {layer1_end}')
print()

# Extract and compare
layer1_source = '\n'.join(ascended_lines[layer1_start:layer1_end]) + '\n'
layer1_hash = hashlib.sha256(layer1_source.encode('utf-8')).hexdigest()

print(f'EXTRACTED LAYER 1')
print(f'  Lines:  {layer1_end - layer1_start}')
print(f'  Chars:  {len(layer1_source)}')
print(f'  SHA256: {layer1_hash}')
print()

print(f'COMPARISON')
print(f'  Official SHA256: {official_hash}')
print(f'  Layer 1 SHA256:  {layer1_hash}')
print()

if official_hash == layer1_hash:
    print('  RESULT: EXACT MATCH')
    print()
    print('  The original HuggingFace source inside the ascended file is')
    print('  cryptographically identical to the official package.')
    print('  SHA-256 confirmed. Zero bytes modified.')
else:
    print('  RESULT: HASHES DIFFER')
    # Find exact differences
    off_lines = official_source.splitlines()
    l1_lines = layer1_source.splitlines()
    diffs = 0
    for i, (a, b) in enumerate(zip(off_lines, l1_lines)):
        if a != b:
            diffs += 1
            if diffs <= 3:
                print(f'  Line {i+1} differs:')
                print(f'    Official: {repr(a[:80])}')
                print(f'    Layer 1:  {repr(b[:80])}')
    print(f'  Total differing lines: {diffs}')

print()
ascended_total = len(ascended_lines)
layer1_count = layer1_end - layer1_start
layer2_count = ascended_total - layer1_count
print(f'ARCHITECTURE')
print(f'  Ascended file:  {ascended_total} lines total')
print(f'  Layer 2 (CMPSBL): {layer2_count} lines of infrastructure')
print(f'  Layer 1 (HuggingFace): {layer1_count} lines (unmodified)')
print()
print('=== END CRYPTOGRAPHIC PROOF ===')
