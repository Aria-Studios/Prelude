# # # # # # # # # # # # # #
#         Prelude         #
# # # # # # # # # # # # # #

# OPTIONAL: Title of your game (highly recommended, there will be
# obvious gaps in the interface if not defined)
gameTitle = 'Game Title'

# OPTIONAL: A URL link to your game's information
gameURL = 'https://reliccastle.com'

# REQUIRED: The URL path to where the remote files are stored, NO TRAILING SLASHES
urlPath = 'https://domain.com/downloads'

# OPTIONAL: The message file name, NO STARTING OR TRAILING SLASHES (highly recommended,
# message contents are controlled from the remote server, cannot be changed through update process)
messageFile = 'message'

# OPTIONAL: message if local version is 0
installMessage = 'This is a test.'

# REQUIRED: The version file name, NO STARTING OR TRAILING SLASHES
versionFile = 'version'

# REQUIRED: The core file name, MUST BE ZIP format
coreArchive = 'core.zip'

# REQUIRED: The patch file name, MUST BE ZIP FORMAT
patchArchive = 'patch.zip'

# OPTIONAL: name of private build channel
privateBuildChannelName = 'Private'

# OPTIONAL: authorization method for private build channel
authMethod = ''

# OPTIONAL: remote password file
passwordFile = 'password'

# OPTIONAL: local authtoken file
tokenFile = 'authtoken'

# OPTIONAL: Fernet key for authtoken encryption
cryptKey = ''
