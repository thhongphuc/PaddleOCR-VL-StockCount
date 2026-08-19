import urllib.request
import urllib.parse
import json
import time

print("Testing /api/scan with sample_1_fmcg...")
data = urllib.parse.urlencode({'sample_id': 'sample_1_fmcg'}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/api/scan', data=data, method='POST')

t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=120) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        t1 = time.time()
        print(f"Success in {round(t1 - t0, 2)}s!")
        print("Model used:", res_data.get("model_used"))
        print("Total items:", len(res_data.get("items", [])))
        print("Metadata:", res_data.get("metadata"))
        print("KPIs:", res_data.get("kpi"))
except Exception as e:
    print("Error calling /api/scan:", e)
