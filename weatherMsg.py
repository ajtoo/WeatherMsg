import json
import requests
import smtplib

FORECAST_URL = "https://api.forecast.io/forecast/"

def main():
	testLat = 38.539352
	testLong = -121.728444
	replyJSON = getForecast(testLat, testLong)
	#print(json.dumps(rJSON, sort_keys = True, indent=4, separators=(',', ': ')))		#[DEBUG]
	printReport(replyJSON)
	print("hit [enter] to close this dialogue")
	input()

def readAPIKey():
	"""gets api key from hidden, read-only file; key is obtained by registering with The Dark SkyForecast"""
	keyFile = open('.key', 'r')
	key = keyFile.read()
	return key

def readSendInfo():
	"""gets email, password, and email that points to text messaging endpoint"""
	info = [line.rstrip('\n') for line in open('.email', 'r')]
	return info
	
def getForecast(latitude, longitude):
	"""calls to api to get the weather, returns JSON with data contained"""
	apiKey = readAPIKey()
	url = FORECAST_URL + apiKey + "/%f,%f" %(latitude, longitude)
	r = requests.get(url)
	rJSON = json.loads(r.text)
	return rJSON

def printReport(weatherJSON):
	"""print weather report from JSON object in a non-JSON format"""
	currentData = weatherJSON['currently']
	weekForecast = weatherJSON['daily']
	print(currentData)
	print(weekForecast)


readSendInfo()