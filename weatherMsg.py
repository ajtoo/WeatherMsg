import json
import requests

def main():
	print("hit [enter] to close this dialogue")
	input()

def readAPIKey():
	keyFile = open('.key', 'r')
	key = keyFile.read()
	return key

main()