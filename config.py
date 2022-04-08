# # # # # # # # # # # # # #
#         Prelude         #
# # # # # # # # # # # # # #

# REQUIRED: Title of your game
gameTitle = 'Game Title'

# REQUIRED: The URL path to where the remote files are stored, NO TRAILING SLASHES
urlPath = 'https://media.ariastudio.dev/prelude'

# REQUIRED: The version file name, NO STARTING OR TRAILING SLASHES
versionFile = 'version'

# REQUIRED: The core file name, MUST BE ZIP format
coreArchive = 'core.zip'

# REQUIRED: The patch file name, MUST BE ZIP FORMAT
patchArchive = 'patch.zip'


# Miscellaneous feature
# configuration options

# OPTIONAL: A URL link to your game's information
gameURL = 'https://reliccastle.com'

# OPTIONAL: change log URL
changelogURL = ''

# OPTIONAL: local path to window icon
iconPath = ''

# OPTIONAL: message if local version is 0
installMessage = 'This is a test.'

# OPTIONAL: The message file name, NO STARTING OR TRAILING SLASHES (highly recommended,
# message contents are controlled from the remote server, cannot be changed through update process)
messageFile = 'message'


# Private Build Channel related
# feature configuration options

# OPTIONAL: authorization method for private build channel
authMethod = 'password'

# OPTIONAL: name of private build channel
privateBuildChannelName = 'Private'

# OPTIONAL: build channel messages
privateMessageFile = 'privateMessage'

# OPTIONAL: remote password file
passwordFile = 'passwords'

# OPTIONAL: local authtoken file
tokenFile = 'authtoken'

# OPTIONAL: Fernet key for authtoken encryption
cryptKey = ''

# OPTIONAL: Discord webhook URL for authorization related notifications
discordWebhookURL = ''
