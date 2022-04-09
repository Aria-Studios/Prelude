![Prelude interface.](https://media.ariastudio.dev/misc/prelude.png)

# Prelude
Prelude is a simple update utility designed for use with Pokémon fangames made using Pokémon Essentials and RPG Maker XP. It is written using Python 3.10.2 and was developed on Windows, has been tested extensively on Windows and Linux, but it does *not* work on MacOS at the moment. Once you've edited the configuration values and compiled the code, you can include the executable file in your base game download. This program can be launched in order to check for any updates that are available, then download and install those updates automatically. The program also has the functionality to display a message to users if there is something important that needs to be communicated to them. It can also be used to distribute in development copies of your game for whatever purpose, such as testing, Patreon rewards, etc.

# Features
* Check the game version, both locally and remotely
* Download and install the latest updates for a game automatically
* Display messages to the user under various circumstances
* Manage the distribution of a private build channel, for uses such as testing or early access

# Getting Started
## Requirements
* [Python](https://www.python.org/downloads/)
  * tkinter (be sure to select the option that includes this when you install Python)
  * [requests](https://docs.python-requests.org/en/latest/user/install/#install)
  * [cryptography](https://pypi.org/project/cryptography/)
  * [discord-webhook](https://github.com/lovvskillz/python-discord-webhook)
* [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html)
* [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/)
* Remote server to store the files

## Installation
1. Read the ***entire*** [File Setup and Structure section](#file-setup-and-structure) below before proceeding!
1. When you're ready, install Python (be sure to add `python` to your PATH), pyinstaller, auto-py-to-exe, and the four modules listed above.
1. Grab the [latest release](https://gitlab.com/ariastudios/prelude/-/releases) of the source code.
1. Setup the remote server's file structure similarly to how it is illustrated below.
1. Using the remote server's information, edit the values in `config.py`.
1. Using either auto-py-to-exe (a GUI-based program) or pyinstaller (a CLI-based program), compile the source code into an executable file targeting `updater.py`. I recommend auto-py-to-exe for the sake of simplicity.
1. Test the resulting program in order to make sure that everything functions correctly.
1. Begin including the necessary files in your game downloads.

# File Setup and Structure
This section goes over how the program operates and should help you make the most of it, while reducing any errors experienced. One caveat that should be kept in mind throughout the process as a whole is that due to Python limitations hidden files should not be used in your game downloads at all. It results in an error as the program will be unable to automatically extract the files and overwrite them. There is a built-in error message, but it is not intended for this purpose.

## `config.py`
`config.py` contains several values that you ***must*** set in order for the program to function. These are what defines how the program will function, including where the program will look for remote files.

```Python
gameTitle = 'Game Title'
urlPath = 'http://domain.com/directory'
versionFile = 'version'
coreArchive = 'core.zip'
patchArchive = 'patch.zip'

gameURL = 'https://reliccastle.com'
changelogURL = 'https://domain.com/changelog'
iconPath = 'icon.ico'
installMessage = 'This message will be displayed when the local version is 0.'
messageFile = 'message'

authMethod = ''
privateBuildChannelName = 'Private'
privateCoreArchive = 'private-core.zip'
privatePatchArchive = 'private-patch.zip'
privateMessageFile = 'privateMessage'
passwordFile = 'passwords'
tokenFile = 'authtoken'
encKey = ''
discordWebhookURL = ''
```

### Required Attributes
* `gameTitle` is fairly self explanatory, it will insert your game's title into all the appropriate spots in the program interface.
* `urlPath` is the *remote* URL path to the directory where your files will be stored. For example, if your website is `https://domain.com` and you will host the files in the `downloads` directory, you would put `https://domain.com/downloads` for this.
* `versionFile` is the name of the *local* ***and*** *remote* files that contain your version information. I recommend leaving it as the default "version" which can be edited fairly easily but will discourage users from tampering with it.
* `coreArchive` is the name of the *remote* ***zip*** archive that contains your latest core release.
* `patchArchive` is the name of the *remote* ***zip*** archive that contains your latest patch release.

### Miscellaneous Attributes (all optional)
* `gameURL` can be used for any URL you choose, such as a project thread on Relic Castle or a custom website, which can be launched from the relevant menu item in the program. If this is not defined, the menu item will be disabled.
* `changelogURL` should be used as a URL to whatever changelog you keep on your project, which will be launched when the relevant menu item is selected. If this is not defined, the menu item will be disabled.
* `iconPath` is a *local* path to the name of an .ico format image, which will be used for your program interface. If this is not defined, the program will use the default tkinter icon instead.
* `installMessage` is a string message that will display whenever the program is launched and the local version is set to 0, which can allow you to define a sort of "welcome" message for any new users or players that is different from the messages displayed to the rest of the users. If this is not defined, no message will be displayed.
* `messageFile` is the name of the *remote* file that contains any messages you want to display to users. If this is not defined, no message will be displayed.

### Private Build Channel Related Attributes
* `authMethod` (optional) is what determines how this feature as a whole behaves. If left undefined, the feature is disabled. If you define it as "none", it will allow anyone who uses the program to access the feature. If you define it as "password", it will require users to authorize their computer in order to access the feature.
* `privateBuildChannelName` (required if `authMethod` is defined) is the name of your private build channel release and will be the name of the directory the build is installed to. The program refers to it as "[NAME] Build Channel" so one word such as "Patreon" or "Testing" would be best.
* `privateCoreArchive` (required if `authMethod` is defined) is the name of the *remote* ***zip*** archive that contains your latest private build channel core release.
* `privatePatchArchive` (required if `authMethod` is defined)is the name of the *remote* ***zip*** archive that contains your latest private build channel patch release.
* `privateMessageFile` (optional) is the name of the *remote* file that contains any messages you want to display to users who can access the private build channel feature. If this is not defined, no message will be displayed.
* `passwordFile` (required if `authMethod` is defined as "password") is the name of the *remote* file that contains passwords that the program will check the user's input against in order to authorize their computer.
* `tokenFile` (required if `authMethod` is defined as "password") is the name of the *local* file that will be created in the game directory to store the authorization details that will be checked each time the program opens.
* `encKey` (required if `authMethod` is defined as "password") is a Fernet encryption key which is used to encrypt & decrypt the `tokenFile` in order to prevent users bypassing the authorization stage. This can be generated using the `utilityScript.py` file in the included scripts folder.
* `discordWebhookURL` (optional) is a Discord webhook URL which will be used to send a customized notification any time a user attempts to authorize their computer or if the stored `tokenFile` does not match their computer. If this is not defined, no notification or information will be sent.

## "core" vs "patch"
One of the first things to understand is that this program operates under the assumption that you use two different kind of updates: core and patch. Core releases are major releases which add or edit a large number of files, wherein it is easier/better to assume that you need to ship the whole game package again rather than attempting to create a patch download. Patch releases are minor releases that add or edit a smaller number of files; additionally, this type of release is ***cumulative*** to the last core release you published.

One *very* important thing to note is that the program cannot update itself as part of the update process. The program does have the functionality to check a downloaded archive for a file that possess the same name as it, and then display a warning message that the update must be manually applied (by extracting the downloaded archive directly into the game directory) before closing the program. This check will occur on any given archive, which means that you must make a choice in how to distribute an updated compiled program; this might mean having the updated updater be in a few patch releases or holding off for any updates until a new core release. This choice is up to you.

## `versionFile`
`versionFile` is a simple file that contains a float (number with a decimal place) value with your release information. This program is capable of up to four decimal points of precision (over 9000 patch releases), but has only been tested extensively using two decimal points of precision. As such, we recommend the use of a version scheme such as `1.23` for your project. The program will view the whole number (`1.##`) as the core release and the decimal places (`#.23`) as the patch release. The `versionFile` file included in your `coreArchive` should always indicate a core release (`1.0`, `2.0`, etc), while the file included in your `patchArchive` (if you have one) should always match with the remote server's `versionFile` file. One last important point to keep in mind with this program is that it cannot recognize the difference between values like `1.1` and `1.10`.

## `coreArchive`, `privateCoreArchive`
The `coreArchive` (or `privateCoreArchive`) archive should contain a copy of the full game directory. It should also be setup so that files can be directly unzipped from the game folder. A `coreArchive` should contain a `versionFile` information file that matches to this core release, which will overwrite the user's current local copy when they update. See the screenshot below for what an example setup should look like.

![Example of coreArchive layout.](https://media.ariastudio.dev/misc/prelude-core.png)

## `patchArchive`, `privatePatchArchive`
The `patchArchive` (or `privatePatchArchive`) archive should contain a copy of ***all files that have been updated since the latest core release*** -- in other words, it is a cumulative patch, not sequential. It should also be setup so that files can be directly unzipped from the game folder. A `patchArchive` should contain an updated `versionFile` information file that matches to this patch release, which will overwrite the user's current local copy when they update. See the screenshot below for what an example setup should look like.

![Example of patchArchive layout.](https://media.ariastudio.dev/misc/prelude-patch.png)

## Local (Game Folder)
Locally, this program works off the assumption that it will be run in the same location as your game executable. This means that you'll need to include two (2) files with your base game: the executable itself and `versionFile` information file. See the screenshot below for what an example setup should look like.

![Example of local folder layout.](https://media.ariastudio.dev/misc/prelude-local.png)

## Remote (Downloads Directory)
On the remote server, the setup is fairly simple: pick a location and upload the files relevant to your particular setup. This means at least uploading the `versionFile` information file, `coreArchive` archive, and `patchArchive` archive; however, it could also include the `message` information file (if you're making use of this feature), `privateCoreArchive` archive, `privatePatchArchive` archive, `passwordFile` information file, or `privateMessageFile` information file (if you're making use of any of the private build channel feature). As long as it can be reached by a standard HTTP request, then the program can function correctly. See the screenshot below for what an example setup should look like.

![Example of remote folder layout.](https://media.ariastudio.dev/misc/prelude-remote.png)

## `messageFile`, `installMessage`, `privateMessageFile`
These are what enable you to communicate with users! `installMessage` is static and defined as a string in your `config.py` file before compiling, so it cannot change. `messageFile` and `privateMessageFile` (depending on your use case) are defined as file names which are hosted in your remote server, and can be edited to allow for the contents to change over time.  You could use this for anything, such as communicating that the next release will be a large core download or if there are special events ongoing in your game (such as a Mystery Gift). These three types of messages are all displayed under different circumstances, so keep that in mind while setting things up. `installMessage` is only displayed if the contents of the local `versionFile` is 0. `messageFile` is only displayed if the contents of the local `versionFile` is *not* 0. `privateMessageFile` is only displayed if the `authMethod` is set to "none" or if the computer is authorized when the `authMethod` is set to "password". After the messages has been dismissed, they can be displayed again via the relevant menu option. If the file is *empty*, the program will not display anything. Likewise if any of these values were not defined in `config.py`, then the program will not display anything (if none of these values were defined, the relevant menu option will be disabled). If any of the files are not present in your remote server directory when the in the case it tries to retrieve their contents, the program will display an error message anytime it is started or if the menu item is triggered. See the screenshot below for what an example message can look like.

![Example of a displayed message.](https://media.ariastudio.dev/misc/prelude-message.png)

# Private Build Channel
The private build channel feature enables you to manage and distribute two types of releases through the same updater concurrently. The first is the regular release channel which is open to anyone using the updater. The second is the private build channel which can be as restricted as you want it to be. This is determined by how you define your `authMethod` in `config.py`. If you use "none", that will enable anyone to install the latest private build channel core and patch releases. Alternatively, you can use the "password" option to create an entry barrier, as it will require users to provide a password and authenticate their computer in order to proceed. Additionally, you could choose to use a single password for every person or individual passwords for individual people (or some combination such as passwords given based on groups).

## Password Authorization
The password `authMethod` is a powerful tool that allows you to control who can or cannot access the private build channel. The passwords themselves (as stored in `passwordFile`) could be a single password for the entire group, several different passwords for different groups of people, or individual passwords for each individual person. Users can attempt to authorize their computer by inputting their name (this is not checked, but is used for the notification if you define `discordWebhookURL`) and password. If successful, that information along with their computer login username is written into a local `tokenFile` and encrypted. This file is how the program recognizes a computer is authorized or not. Each time the program starts, if that file is present, it checks the status of the authorization to determine if it is still valid. You are also able to remotely reset all authorization states by changing the contents of the `passwordFile` to "reset".

![Example of the authorization screen for the password authentication method.](https://media.ariastudio.dev/misc/prelude-authorization.png)

## Private Build Installation
The private build channel differs from the regular release channel in that it does *not* track any version information. These are seen as dynamic builds which can change rapidly. There are two menu options available for users to use to install the latest builds. The first option is a core install option which deletes the old build and installs the current latest core fresh. The second option is for a patch installation, which simply follows the same basic process as the regular patching process. Note that the private build is stored in a subdirectory of the game directory itself, which is named based on the `privateBuildChannelName` defined in `config.py`.

## `utilityScript.py`
Depending on your use case, the private build channel feature could need to support quite a few people! To make things easier for you, you can use the `utilityScript.py` file in the scripts directory to automate some things! It is able to do the following:
1. Generate a Fernet encryption key (this is required if you use the password `authMethod`)
1. Generate a list of given number of passwords as needed in your `passwordFile` to be uploaded directly to your remote directory for authentication purposes
1. Send a test email invitation using your provided text to check formatting and such before mass inviting people
1. Send emails to several people based on a CSV containing a name & email, along with your `passwordFile`, and your provided text.

# Testing
Prelude is tested against several different scenarios before any new code release. You can look at the list of scenarios we test against [here](https://docs.google.com/spreadsheets/d/188AKWlHg5QAhtioRswFOT3Xm4uZ1Rmn-n1u9BfvxH-o/edit?usp=sharing) and if you can think of any scenarios that are not covered by those in the list, please let us know so we can add those to our slate for next time.

# Future Plans
* Add more error handling.
* More authentication methods for the private build channel feature.
* Bug fixes (please let us know if you encounter any bugs and we will work to address those in the next release if possible)
* If you have any ideas for features, please feel free to let us know and we will evaluate whether it is feasible, worthwhile, or within the scope of the program to implement.
