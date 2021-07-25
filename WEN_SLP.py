import requests
import json
import time
import datetime
from web3.auto import w3
from eth_account.messages import encode_defunct

def getRawMessage():
    # Function to get message to sign from axie

    # An exemple of a requestBody needed
    requestBody = {"operationName":"CreateRandomMessage","variables":{},"query":"mutation CreateRandomMessage {\n  createRandomMessage\n}\n"}
    # Send the request
    r = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}, data=requestBody)
    # Load the data into json format
    json_data = json.loads(r.text)
    # Return the message to sign
    return json_data['data']['createRandomMessage']

def getSignMessage(rawMessage, accountPrivateKey):
    # Function to sign the message got from getRawMessage function

    # Load the private key from the DataBase in Hex
    private_key = bytearray.fromhex(accountPrivateKey)
    message = encode_defunct(text=rawMessage)
    # Sign the message with the private key
    hexSignature = w3.eth.account.sign_message(message, private_key=private_key)
    # Return the signature
    return hexSignature

def submitSignature(signedMessage, message, accountAddress):
    # Function to submit the signature and get authorization

    # An example of a requestBody needed
    requestBody = {"operationName":"CreateAccessTokenWithSignature","variables":{"input":{"mainnet":"ronin","owner":"User's Eth Wallet Address","message":"User's Raw Message","signature":"User's Signed Message"}},"query":"mutation CreateAccessTokenWithSignature($input: SignatureInput!) {\n  createAccessTokenWithSignature(input: $input) {\n    newAccount\n    result\n    accessToken\n    __typename\n  }\n}\n"}
    # Remplace in that example to the actual signed message
    requestBody['variables']['input']['signature'] = signedMessage['signature'].hex()
    # Remplace in that example to the actual raw message
    requestBody['variables']['input']['message'] = message
    # Remplace in that example to the actual account address
    requestBody['variables']['input']['owner'] = accountAddress
    # Send the request
    r = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}, json=requestBody)
    # Load the data into json format
    json_data = json.loads(r.text)
    # Return the accessToken value
    return json_data['data']['createAccessTokenWithSignature']['accessToken']

def get_access_token(address, private):
	"""
	Get an access token as proof of authentication
	:return: The access token in string
	"""
	msg = getRawMessage()
	signed = getSignMessage(msg, private)
	token = submitSignature(signed, msg, address)
	return token

def get_price(currency, access_token):
	"""
	Get the price in USD for 1 ETH / SLP / AXS
	:return: The price in US of 1 token
	"""
	url = "https://axieinfinity.com/graphql-server-v2/graphql"
	body = {"operationName": "NewEthExchangeRate", "variables": {}, "query": "query NewEthExchangeRate {\n  exchangeRate {\n    " + currency.lower() + " {\n      usd\n      __typename\n    }\n    __typename\n  }\n}\n"}
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'authorization': 'Bearer ' + access_token}
	r = requests.post(url, headers=headers, json=body)
	try:
		json_data = json.loads(r.text)
	except ValueError as e:
		return e
	return json_data['data']['exchangeRate'][currency.lower()]['usd']


def claim_slp(ronin_address, access_token):
	"""
	Tells if you can claim SLP or not and WHEN
	:return: The time when it will be claimable
	"""
	url = 'https://game-api.skymavis.com/game-api/clients/' + ronin_address + '/items/1/claim'
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'authorization': 'Bearer ' + access_token}
	body = {}
	r = requests.post(url, headers=headers, json=body)

	try:
		json_data = json.loads(r.text)
	except ValueError as e:
		return e

	total = json_data['total']
	wait = time.time() - json_data['last_claimed_item_at']
	day = str(wait) // (24 * 3600)
	wait = wait % (24 * 3600)
	hour = str(wait) // 3600
	wait %= 3600
	m = str(wait) // 60
	wait %= 60
	s = str(wait)

	if wait > 1300000:
		response = "✅ **ABLE TO CLAIM**\n\n"
	else:
		response = "❌ **NOT ABLE TO CLAIM**\n\n"

	response += "Next claim is avaible in : " + day + " day(s) " + hour + " hour(s) " + m + " min " + s + " sec\n"
	response += "You farmed **" + str(total) + "** SLP ! \nAfter we split, you'll have : "
	response += str(int(int(total)*0.6)) + " SLP\nEquivalent to : "
	response += str(int((total * get_price('slp', access_token)) * 0.6)) + "$ 😃"
	return response
