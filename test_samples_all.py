import sys
import urllib.request
import urllib.parse
import json
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

for sample_id in ["sample_2_electronics", "sample_3_pharma"]:
    print(f"\n--- Testing /api/scan with {sample_id} ---")
    data = urllib.parse.urlencode({'sample_id': sample_id}).encode('utf-8')
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
            for item in res_data.get("items", [])[:3]:
                print(f"  > [{item['sku']}] {item['description']} - Book: {item['book_qty']} | Actual: {item['actual_qty']} | Var: {item['variance']} ({item['status']})")
    except Exception as e:
        print(f"Error calling /api/scan with {sample_id}:", e)
