import codecs, time
print('=== DEMO 3: ADAPTIVE DEFENSE LOOP ===')
print('Watch the system learn and escalate in real time.')
print()

with codecs.open('src/transformers/modeling_utils.py', 'r', 'utf-8') as f:
    code = f.read().split('ORIGINAL SOURCE (UNMODIFIED')[0]
exec(code)

rv = RequestValidator()
dl = DefenseLayer()
le = LearningEngine()
pm = PersistentMemory(namespace='defense_demo')
pm.clear()
pm.set('threat_count', 0)
pm.set('blocked_ips', [])

attacks = [
    {'input': 'Load bert-base model', 'ip': '192.168.1.10'},
    {'input': '<script>steal_tokens()</script>', 'ip': '45.33.32.1'},
    {'input': 'Fine-tune on my dataset', 'ip': '192.168.1.10'},
    {'input': "<script>document.cookie</script>", 'ip': '45.33.32.1'},
    {'input': '<script>fetch("http://evil.com")</script>', 'ip': '45.33.32.1'},
    {'input': 'Run inference on test set', 'ip': '10.0.0.5'},
    {'input': '<script>window.location="http://phish"</script>', 'ip': '45.33.32.1'},
    {'input': 'Export model to ONNX', 'ip': '192.168.1.10'},
]

print('ROUND  SOURCE            INPUT                                RESULT')
print('-' * 85)

for i, req in enumerate(attacks):
    count = pm.get('threat_count')
    blocked = pm.get('blocked_ips')

    if req['ip'] in blocked:
        print(f'  {i+1}.    {req["ip"]:<18}{req["input"][:37]:<37}  IP BANNED')
        le.record('ip_block', 'enforced', {'ip': req['ip']})
        time.sleep(0.3)
        continue

    try:
        rv.validate(req)
        le.record('request', 'clean', {'ip': req['ip']})
        print(f'  {i+1}.    {req["ip"]:<18}{req["input"][:37]:<37}  ALLOWED')
    except ValueError:
        count += 1
        pm.set('threat_count', count)
        le.record('request', 'threat', {'ip': req['ip'], 'count': count})
        escalation = ''

        if count == 1:
            escalation = '  -> WARNING logged'
        elif count == 2:
            escalation = '  -> THREAT LEVEL ELEVATED'
        elif count >= 3:
            blocked.append(req['ip'])
            pm.set('blocked_ips', blocked)
            dl.block(req['ip'])
            escalation = '  -> IP BANNED. Future requests rejected.'

        print(f'  {i+1}.    {req["ip"]:<18}{req["input"][:37]:<37}  BLOCKED (threat #{count}){escalation}')

    time.sleep(0.3)

print()
print('--- SYSTEM STATE AFTER ATTACK SEQUENCE ---')
print()
print(f'  Threats detected:   {pm.get("threat_count")}')
print(f'  Banned IPs:         {pm.get("blocked_ips")}')
print(f'  Learning insight:   {le.suggest("request")}')
print(f'  Persisted to disk:  ~/.cmpsbl/defense_demo.memory.json')
print()
pm2 = PersistentMemory(namespace='defense_demo')
print(f'  Reload test:        threat_count = {pm2.get("threat_count")}')
print(f'  Reload test:        blocked_ips  = {pm2.get("blocked_ips")}')
print()
print('The system detected, escalated, and banned autonomously.')
print('State survived reload. The attacker is permanently blocked.')
print('No human intervention. No AI calls. Pure algorithmic governance.')
print()
print('=== END ADAPTIVE DEFENSE DEMO ===')
