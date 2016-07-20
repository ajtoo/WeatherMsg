import json
import requests
import smtplib

FORECAST_URL = "https://api.forecast.io/forecast/"

def main():
	coords = getLatLong()
	replyJSON = getForecast(coords[0], coords[1])
	#print(json.dumps(rJSON, sort_keys = True, indent=4, separators=(',', ': ')))		#[DEBUG]
	#printReport(replyJSON)
	sendInfo = readSendInfo()
	rJSON = getForecast(testLat, testLong)
	msgTxt = parseForMessage(rJSON)
	msg = "\r\n".join([
	"From: %s" % sendInfo[0],
	"To: %s" % sendInfo[2],
	"Subject:",
	"",
	msgTxt
	])
	sendMessage(sendInfo, msg)

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

def parseForMessage(jsonDict):
	apparentTemp = jsonDict['currently']['apparentTemperature']
	temp = jsonDict['currently']['temperature']
	summary = jsonDict['currently']['summary']
	msg = "\n" + summary + "\nApparent Temp: %f" % apparentTemp + "\ntemperature: %f" % temp + "\n"
	return msg

def sendMessage(sendInfo, message):
	"""sendInfo should be a list in the order of:[sending email, password, target email]"""
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(sendInfo[0], sendInfo[1])
	result = server.sendmail(sendInfo[0], [sendInfo[2]], message)
	#print(result)
	server.quit()

def getLatLong():
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	retList = [lat, lon]
	return retList

main()