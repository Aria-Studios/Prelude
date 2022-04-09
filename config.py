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
gameURL = 'https://reliccastle.com'

# OPTIONAL: change log URL
changelogURL = 'https://domain.com/changelog'

# OPTIONAL: local path to window icon, MUST BE .ICO FORMAT
iconPath = 'icon.ico'

# OPTIONAL: message if local version is 0
installMessage = 'This message will be displayed when the local version is 0.'

# OPTIONAL: The message file name, NO STARTING OR TRAILING SLASHES (highly recommended,
# message contents are controlled from the remote server, cannot be changed through update process)
messageFile = 'message'


# Private Build Channel related
# feature configuration options

# OPTIONAL: authorization method for private build channel
authMethod = ''

# REQUIRED (if authMethod is defined): name of private build channel
privateBuildChannelName = 'Private'

# REQUIRED (if authMethod is defined): core file name, MUST BE ZIP format
privateCoreArchive = 'private-core.zip'

# REQUIRED (if authMethod is defined): patch file name, MUST BE ZIP format
privatePatchArchive = 'private-patch.zip'

# OPTIONAL: build channel messages
privateMessageFile = 'privateMessage'

# OPTIONAL: remote password file
passwordFile = 'passwords'

# OPTIONAL: local authtoken file
tokenFile = 'authtoken'

# REQUIRED (if authMethod is password): Fernet key for authtoken encryption
encKey = ''

# OPTIONAL: Discord webhook URL for authorization related notifications
discordWebhookURL = ''
