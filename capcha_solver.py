import requests
import time

site_key = "6Ldcxr0pAAAAAJHH36kl4FAjwPK41HqrxwqVujk_"  # site key of your target site
site_url = "https://app.lanify.ai"  # page url of your target site
solver_api = {'2capcha':'will_add_soon'}

def capsolver(api_key):
    payload = {
        "clientKey": api_key,
        "task": {
            "type": 'ReCaptchaV2TaskProxyLess',
            "websiteKey": site_key,
            "websiteURL": site_url
        }
    }
    res = requests.post("https://api.capsolver.com/createTask", json=payload)
    resp = res.json()
    task_id = resp.get("taskId")
    if not task_id:
        print("Failed to create task:", res.text)
        return
    print(f"Got taskId: {task_id} / Getting result...")

    while True:
        time.sleep(3)  # delay
        payload = {"clientKey": api_key, "taskId": task_id}
        res = requests.post("https://api.capsolver.com/getTaskResult", json=payload)
        resp = res.json()
        status = resp.get("status")
        if status == "ready":
            return resp.get("solution", {}).get('gRecaptchaResponse')
        if status == "failed" or resp.get("errorId"):
            print("Solve failed! response:", res.text)
            return

