import requests
import os
import time

Customer_env = os.environ['Customer_env']
url = "http://10.206.93.72:8080/ords/dbinfo/auto/{}".format(Customer_env)
profile_details_url = "http://10.206.93.72:8080/ords/dbinfo/profile/profile_name/{}".format(Customer_env)
timeout = time.time() + 60 * 480


def create_env_in_db():
    print("url:", url)
    print("Inside create Env.")
    pipeline_name = os.environ['pipeline_name']
    build_number = os.environ['build_number']
    build_url = os.environ['build_url']
    print(pipeline_name, build_number, build_url)
    data = '{"status":"LOCK","pipeline_name":"' + pipeline_name + '","build_number":"' + build_number + '",' \
        '"build_link":"' + build_url + '","pass_rate":"0","ci_server":"Azure DevOps"}'
    headers = {"Content-type": "application/json"}
    print("data:", data)
    r = requests.post(url, data=data, headers=headers)
    return r.status_code


def get_lock_unlock_status():
    while True:
        r = requests.get(url=url)
        data = r.json()
        if not data["items"]:
            print("Environment is not present in Database table. Creating Environment.")
            code = create_env_in_db()
            if code == 200:
                print("Environment Entered in DB Successfully. Locking the environment and executing Pipeline.")
                create_env_in_db()
                break
            else:
                print("Environment Creation Failed. Please retry.")
                exit(1)
        else:
            status = data["items"][0]["status"]
            if status == "UNLOCK":
                print("Environment is unlocked.")
                break
            else:
                if time.time() < timeout:
                    continue
                else:
                    pipeline_name = data["items"][0]["pipeline_name"]
                    print("Environment is Locked by pipeline - '{}'. Request Timeout.".format(pipeline_name))
                    exit(1)


def get_env_up_down_status():
    r = requests.get(url=profile_details_url).json()
    res = r["items"]
    up_status = []
    for env in res:
        url = ""
        if env["nginx_url"] is None:
            url = env["web_app_url"]
        else:
            url = env["nginx_url"]
        print(url)
        try:
            req = requests.get(url)
            up_status.append(req.status_code)
        except:
            print("No response from Nginx Server.")

    if 200 in up_status and len(up_status) > 1:
        print("One of the Cluster Environment is UP. Checking for lock status.")
        get_lock_unlock_status()
    elif 200 in up_status and len(up_status) == 1:
        print("Environment is up. Checking for lock status.")
        get_lock_unlock_status()
    else:
        print("Environment is down. Pipeline cannot execute.")
        exit(1)

get_env_up_down_status()