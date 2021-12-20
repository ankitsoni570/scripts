import base64
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, cc_email)
import os
import json
import sys

AZURE_DEVOPS_PAT = os.environ['PAT']
authorization = str(base64.b64encode(bytes(':' + AZURE_DEVOPS_PAT, 'ascii')), 'ascii')
headers = {
    'Accept': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic ' + authorization
}

url = 'https://dev.azure.com/GPP-SP/Automation/_settings/agentqueues?__rt=fps&__ver=2'
try:
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
except requests.exceptions.HTTPError as err:
    print(err)


# creating list of all the Agents
def get_our_agents_name(pools):
    result = []
    for pool in pools:
        if pool['owner']['displayName'] == 'Eduard Dubilyer' or pool['owner']['displayName'] == 'Ankit Soni' or pool['owner']['displayName'] == 'Azure Pipelines':
            result.append(pool['name'])
    return result


# creating list of busy agents
def get_busy_agents(agents):
    result = []
    for agent in agents:
        result.append(agent['name'])
    return result


# getting agent utilization details
def get_utilization_details(agt_pool, bsy_agt, agt_data):
    for p in agt_pool:
        if p in bsy_agt:
            for d in agt_data:
                if p == d['name']:
                    print(p, ': Queued Jobs - ', d['queuedRequestCount'], '/ Assigned Jobs - ',
                          d['assignedRequestCount'], '/ Running Jobs - ', d['runningRequestCount'])
        else:
            print(p, ': Free')


def send_mail():
    mail_flag = "false"
    subject = 'Automation Agent Queue Status'
    to_emails = [
        ('ankit.soni@finastra.com', 'Ankit Soni'),
        ('eduard.dubilyer@finastra.com', 'Eduard Dubilyer')
    ]
    mail_body = ''
    with open('./output.txt') as file:
        for line in file:
            # while line := file.readline().rstrip():
            tmp = line.split(':')
            if "Free" not in tmp[1]:
                queued_jobs = tmp[1].split("/")[0].split("-")[1]
                if int(queued_jobs) >= 5:
                    mail_flag = "true"
            mail_body += '<tr><td><b>' + tmp[0] + '</b></td><td><b>' + tmp[1] + '</b></td></tr>'
    if mail_flag == "true":
        data_ = '<html><head><style>table {font-family: arial, sans-serif; border-collapse: collapse; width: 100%;} td {' \
                'border: 1px solid #dddddd; text-align: left; padding: 8px;}</style></head><body><h4>Hi All,' \
                '</h4><p>Please find the below agent queue status ' \
                'detail.</p>' \
                '<br/> <table>' + mail_body + '</table><br/>Thanks and Regards</p><p>Automation Infra ' \
                                            'Team</p></body></html>'
        message = Mail(
            from_email='automation.infra@finastra.com',
            to_emails=to_emails,
            is_multiple=True,
            subject=subject,
            html_content=data_
        )
        
        sg = SendGridAPIClient(os.environ['API_KEY'])
        response = sg.send(message)
        print(response.status_code, response.body, response.headers) 
    else:
        print("Email flag is: {}".format(mail_flag))


pools_data = data['fps']['dataProviders']['data']['ms.vss-build-web.agent-pools-data-provider']['taskAgentPools']
agent_data = data['fps']['dataProviders']['data']['ms.vss-build-web.agent-pools-data-provider'][
    'taskAgentPoolStatusList']
agents_pools = get_our_agents_name(pools_data)
busy_agents = get_busy_agents(agent_data)
original_stdout = sys.stdout
sys.stdout = open("output.txt", "w")
get_utilization_details(agents_pools, busy_agents, agent_data)
sys.stdout = original_stdout
send_mail()