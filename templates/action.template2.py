import urllib.request

# CONFIGURATION
# All server configuration fields will be available in the 'params' dictionary.
{% for k,v in r.params.items() %}{{ k }} = params["{{ v }}"] 
{% endfor %}

# Actions Parameters 
{% for k,v in r.actions_params.items() %}{{ k }} = actions_params["{{ v }}"] 
{% endfor %}

# There are five debug levels for python: critical, error, warning, info, debug, which have values 1-5 respectively.
# A user can control the debug level by setting the plugin debug level.
logging.critical("The server url is {}".format(url))

if channel.lower() == "default":
	channel = default_channel

payload = 'payload={"text": "%s", "username":"%s", "channel":"%s"}' % (message, bot_name, channel)

request = urllib.request.Request(url, data=bytes(payload, encoding="utf-8"))

r = urllib.request.urlopen(request, context=ssl_context)
response = {}

# For actions, the response object must have a field named "succeeded" to denote if the action suceeded or not.
# The field "troubleshooting" is optional to display user defined messages in CounterACT for actions. The field
# "cookie" is available for continuous/cancellable actions to store information for the same action. For this example,
# the cookie stores the id of the user, which will be used to delete the same user when this action is cancelled.
if r.getcode() == 200:
	response["succeeded"] = True
else:
	response["succeeded"] = False
	response["troubleshooting"] = "Failed action. Response code: {}".format(r.getcode())