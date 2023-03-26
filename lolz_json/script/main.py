import json

with open('config.json') as f:
    config = json.load(f)

config['config']['message_param'] = 'False'
		
with open('config.json', 'w') as f:
	config = json.dump(config, f)
