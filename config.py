# # # # # # # # # # # # # #
#         Prelude         #
# # # # # # # # # # # # # #

# REQUIRED: Title of your game
gameTitle = 'Game Title'

# REQUIRED: The URL path to where the remote files are stored, NO TRAILING SLASHES
urlPath = 'https://domain.com/downloads'

# REQUIRED: The version file name, NO STARTING OR TRAILING SLASHES
versionFile = 'version'

# REQUIRED: The core file name, MUST BE ZIP format
coreArchive = 'core.zip'

# REQUIRED: The patch file name, MUST BE ZIP FORMAT
patchArchive = 'patch.zip'


# Miscellaneous feature
# configuration options

# OPTIONAL: A URL link to your game's information
gameURL = ''

# OPTIONAL: A URL link to your game's changelog
changelogURL = ''

# OPTIONAL: The local path to a window icon, MUST BE ICO FORMAT
iconPath = ''

# OPTIONAL: A message which can be displayed (if the local version is 0)
installMessage = ''

# OPTIONAL: The message file name, NO STARTING OR TRAILING SLASHES
messageFile = 'message'


# Private Build Channel related
# feature configuration options

# OPTIONAL: The authorization method for the private build channel
# OPTIONS: '', 'none', 'password'
authMethod = ''

# REQUIRED (if authMethod is defined): The name of the private build channel
privateBuildChannelName = 'Private'

# REQUIRED (if authMethod is defined): The private build channel core file name, MUST BE ZIP format
privateCoreArchive = 'private-core.zip'

# REQUIRED (if authMethod is defined): The private build channel patch file name, MUST BE ZIP format
privatePatchArchive = 'private-patch.zip'

# OPTIONAL: The private build channel message file name, NO STARTING OR TRAILING SLASHES
privateMessageFile = 'privateMessage'

# REQUIRED (if authMethod is password): The private build channel password file name, NO STARTING OR TRAILING SLASHES
passwordFile = 'passwords'

# REQUIRED (if authMethod is password): The name of the local token that will be created to store authentication data
tokenFile = 'authtoken'

# REQUIRED (if authMethod is password): A Fernet key for encryption purposes
encKey = ''

# OPTIONAL: A Discord webhook URL for authorization related notifications
discordWebhookURL = ''
