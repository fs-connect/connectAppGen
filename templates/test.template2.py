# CONFIGURATION
# All server configuration fields will be available in the 'params' dictionary.
{% for k,v in r.params.items() %}{{ k }} = params["{{ v }}"] 
{% endfor %}

headers = {"content-type": "application/json", "Authorization": "Bearer " + str(slack_app_token)}
response = {}

## Verify all APIs required for the App return valid values back and are authenticated
URL = "https://slack.com/api/channels.list"
request = urllib.request.Request(URL,  headers=headers)
resp = urllib.request.urlopen(request)
json_resp = json.loads(resp.read())
if "channels" not in json_resp:
   response["succeeded"] = False
   response["result_msg"] = str(json_resp)   
else:
	USER_URL = "https://slack.com/api/users.list"
	request = urllib.request.Request(USER_URL,  headers=headers)
	resp = urllib.request.urlopen(request)
	json_resp = json.loads(resp.read())

	if "members" not in json_resp:
	   response["succeeded"] = False
	   response["result_msg"] = str(json_resp)
	else:	
		IM_URL = "https://slack.com/api/im.list"
		request = urllib.request.Request(IM_URL,  headers=headers)
		resp = urllib.request.urlopen(request)
		json_resp = json.loads(resp.read())

		if "ims" not in json_resp:
		   response["succeeded"] = False
		   response["result_msg"] = str(json_resp)
		else:
			response["succeeded"] = True
			response["result_msg"] = "Successfuly Connected and authenticated with Slack workspace " + slack_workspace