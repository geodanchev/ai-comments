import json


config_file = "config.json"
config = {}
with open(config_file) as f:
    config = json.load(f)


def getOpenAIEndpoint():
    return config["openAI_endpoint"]

def getOpenAIKey():
    return config["openAI_key"]

def getMongoAddress():
    return config["db_host"]

def getMongoDBName():
    return config["db_name"]