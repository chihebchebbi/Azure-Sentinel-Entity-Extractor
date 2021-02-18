import requests
import json
import termcolor
import sys
# install termocolor module: pip3 install termcolor

banner = """

Azure Sentinel Entity Extractor 

Usage: python3 Azure-Sentinel-Entities.py <SystemAlertId>

"""

print (termcolor.colored(banner,'blue'))

# Add the rquired fields
Azure_AD_Tenant = "Azure_AD_Tenant_HERE"
Client_ID = "Client_ID_HERE"
Client_Secret = "Client_Secret_HERE"
ResourceGroup = "ResourceGroup_HERE"
Workspace = "Workspace_HERE"
Subscription = "Subscription_ID"
SystemAlertId = str(sys.argv[1])

print(SystemAlertId) 

# Get the Access Token

Url = "https://login.microsoftonline.com/"+Azure_AD_Tenant+"/oauth2/token"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload='grant_type=client_credentials&client_id='+ Client_ID+'&resource=https%3A%2F%2Fmanagement.azure.com&client_secret='+Client_Secret
response = requests.post(Url, headers=headers, data=payload).json()
Access_Token = response["access_token"]
print("[+] Access Token Received Successfully")

# Send the query 
Url2= "https://management.azure.com/subscriptions/"+Subscription+"/resourceGroups/"+ResourceGroup+"/providers/Microsoft.OperationalInsights/workspaces/"+Workspace+"/api/query?api-version=2020-08-01"
payl2 = "\n \"query\": \"SecurityAlert | where SystemAlertId == \'"+SystemAlertId+"\'\"\n"
payload2="{"+payl2+"}"
Auth = 'Bearer '+Access_Token
headers2 = {
  'Authorization': Auth ,
  'Content-Type': 'text/plain'
}

response2 = requests.post(Url2, headers=headers2, data=payload2).json()
print("[+] Incident Details were received Successfully")

#Entities loading
Entities = response2["Tables"][0]["Rows"][0][21] 
Parsed_Entities = json.loads(Entities)
print(Parsed_Entities)
print("[+] Entities were received Successfully")


        
