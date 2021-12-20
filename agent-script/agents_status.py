import base64
import requests
import os

AZURE_DEVOPS_PAT = os.environ['PAT']
authorization = str(base64.b64encode(bytes(':' + AZURE_DEVOPS_PAT, 'ascii')), 'ascii')
headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic ' + authorization
}

url = 'https://dev.azure.com/GPP-SP/Automation/_settings/agentqueues?__rt=fps&__ver=2'
data = requests.get(url, headers=headers).json()


# creating list of all the Agents
def get_our_agents_name(pools):
    result = []
    for pool in pools:
        if pool["owner"]["displayName"] == "Eduard Dubilyer" or pool["owner"]["displayName"] == "Ankit Soni":
            result.append(pool["name"])
    return result


# creating list of busy agents
def get_busy_agents(agents):
    result = []
    for agent in agents:
        result.append(agent["name"])
    return result


# getting agent utilization details
def get_utilization_details(agt_pool, bsy_agt, agt_data):
    for p in agt_pool:
        if p in bsy_agt:
            for d in agt_data:
                if p == d["name"]:
                    print(p, ": Queued Jobs:", d["queuedRequestCount"], "/ Assigned Jobs:",
                          d["assignedRequestCount"], "/ Running Jobs:", d["runningRequestCount"])
        else:
            print(p, "agent is free.")


pools_data = data['fps']['dataProviders']['data']['ms.vss-build-web.agent-pools-data-provider']['taskAgentPools']
agent_data = data['fps']['dataProviders']['data']['ms.vss-build-web.agent-pools-data-provider'][
    'taskAgentPoolStatusList']
agents_pools = get_our_agents_name(pools_data)
busy_agents = get_busy_agents(agent_data)
get_utilization_details(agents_pools, busy_agents, agent_data)
