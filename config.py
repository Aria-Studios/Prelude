# from cryptography.fernet import Fernet

configFile = open('configData', 'r')
config = configFile.read()
configFile.close()
config = config.split('\n')

gameTitle = config[0]
urlPath = config[1]
gameURL = config[2]
changelogURL = config[3]
operatingSystem = config[4]

try:
    privateConfigFile = open('privateConfigData', 'r')
    privateBuildConfig = privateConfigFile.read()
    privateConfigFile.close()
    privateBuildConfig = privateBuildConfig.split('\n')

    privateBuildChannelURLPath = privateBuildConfig[0]
    privateBuildChannelName = privateBuildConfig[1]
    privateBuildChannelAuthMethod = privateBuildConfig[2]
    privateBuildChannelEncKey = privateBuildConfig[3]
    discordWebhookURL = privateBuildConfig[4]
    privateBuildChannelChangelogURL = privateBuildConfig[5]
except FileNotFoundError:
    privateBuildChannelAuthMethod = ''

""" configFile = open('configData', 'rb')
config = configFile.read()
configFile.close()

encKeyFile = open('encKey', 'r')
progEncKey = Fernet(encKeyFile.read())
encKeyFile.close()

config = progEncKey.decrypt(config)
config = config.decode('UTF-8')
config = config.split('\n')"""