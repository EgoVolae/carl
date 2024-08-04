from decouple import config


class Configuration:
	# Constants
	PROJECT_NAME = 'Carl'
	VERSION = '1.0.0'
	
	CARL_BOT_TOKEN = config('CARL_BOT_TOKEN')