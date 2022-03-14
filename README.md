

# Prelude Updater
Prelude is a simple update utility designed for use with Pokémon fangames made using Pokémon Essentials and RPG Maker XP. This was written in Python and developed/tested on Windows, but it should theoretically work on any OS (given the appropriate development environment to compile the executable file). Once you've edited the variables and compiled the code, you can include the executable file in your game download. This program can be launched in order to check for any updates that are available, then download and install those updates automatically. The program also has functionality to display a message to users if there is something important that needs to be communicated to them.

# Getting Started
1. Read the *entire* [File Setup and Structure section](#file-setup-and-structure) below before proceeding!
1. When you're ready, install [Python](https://www.python.org/downloads/) (if it asks, be sure to install the tkinter module as well).
1. Install any other dependencies (the only one should be the [requests module](https://docs.python-requests.org/en/latest/user/install/#install)).
1. Grab a copy of the source code for this project.
1. Open the `updater.py` file and edit the values at the beginning of the file; save and close the file.
1. Install [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html) and [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/).
1. Use one of the above to compile the source code into an executable file. auto-py-to-exe provides an easy to use GUI, while pyinstaller is a CLI program. I recommend auto-py-to-exe for simplicity's sake.
1. Setup the remote file structure.
1. Begin including the necessary files in your game downloads.

# File Setup and Structure
This section goes over how the program operates and should help you make the most of it, while reducing any errors experienced.

## "core" vs "patch"
One of the first things to understand is that this program operates under the assumption that you use two different kind of updates: core and patch. Core releases are major releases which add or edit a large number of files, wherein it is easier/better to assume that you need to ship the whole game package again rather than attempting to create a patch download. Patch releases are minor releases that add or edit a smaller number of files; additionally, this type of release is cumulative to the last core release you published.

## `message`
`message` is what enables you to communicate any important information to users, hosted only in your remote directory. You could use this for anything, such as communicating that the next release will be a large core download or if there are special events ongoing in your game (such as a Mystery Gift). If the file has content, the message will automatically be displayed when the program is started. After it has been dismissed, it can be displayed again via the relevant menu option. If the file is *empty*, the program will not display anything and the menu option will be disabled. See the screenshot below for what an example message will look like.

![Example of displayed message.](https://media.ariastudio.dev/misc/prelude-message.png)

## `version`
`version` is a simple file that contains a float value with your release information. As it is a float value (with up to two decimal points of precision), you should use a scheme such as `1.21` for version information. For our purposes, the program views the whole number (`1.##`) as the core release, and the decimal places (`#.01`) as patch releases. One important point to keep in mind with this program is that it cannot recognize the difference between values like `1.1` and `1.10`. This file is used in several different places, both remotely and locally and will be covered more later.

## `updater.py`
`updater.py` contains a few variables which are used in order to pull information from the local game installation and your remote server.

```Python
gameTitle = 'Game Title'
gameURL = 'https://reliccastle.com'
urlPath = 'http://domain.com/directory'
messageFile = 'message'
versionFile = 'version'
coreArchive = 'core.zip'
patchArchive = 'patch.zip'
```

* `gameTitle` is fairly self explanatory, it will insert your game's title into all the appropriate spots in the program interface.
* `gameURL` can be used for any URL you choose, such as a project thread on Relic Castle or a custom website. It will launch if the appropriate options is selected in the menu bar.
* `urlPath` is the *remote* URL path to the directory where your files will be stored. For example, if your website is `https://domain.com` and you will host the files in the `downloads` directory, you would put `https://domain.com/downloads` for this variable.
* `messageFile` is the name of the *remote* file that contains any messages you want to display to users.
* `versionFile` is the name of the *local* ***and*** *remote* files that contain your version information. I recommend leaving it as the default `version` which can be edited fairly easily but will discourage users from tampering with it.
* `coreArchive` is the name of the *remote* ***zip*** archive that contains your latest core/major release.
* `patchArchive` is the name of the *remote* ***zip*** archive that contains your latest patch/minor release.

## `core.zip`
The `core.zip` archive should contain a copy of the full game directory. It should also be setup so that files can be directly unzipped from the game folder. This should also contain a `version` information file that matches to this core release. See the screenshot below for what an example setup should look like.

![Example of core.zip layout.](https://media.ariastudio.dev/misc/prelude-core.png)

## `patch.zip`
The `patch.zip` archive should contain a copy of all files that have been updated since the latest ***core*** release -- in other words, it is a cumulative patch, not sequential. It should also be setup so that files can be directly unzipped from the game folder. This should also contain an updated `version` information file that matches to this patch release, which will overwrite the user's local copy when they update. See the screenshot below for what an example setup should look like.

![Example of patch.zip layout.](https://media.ariastudio.dev/misc/prelude-patch.png)

## Local (Game Folder)
Locally, this program works off the assumption that it will be run in the same location as your game executable. This means that you'll need to include two (2) files with your base game: the `updater` executable and `version` information file. See the screenshot below for what an example setup should look like.

![Example of local folder layout.](https://media.ariastudio.dev/misc/prelude-local.png)

## Remote (Downloads Directory)
On the remote server, the setup is fairly simple: pick a location and put the `message` information file, `version` information file, `core.zip` archive, and `patch.zip` archive there. As long as it can be reached by an HTTP request, then the program can function correctly. See the screenshot below for what an example setup should look like.

![Example of remote directory layout.](https://media.ariastudio.dev/misc/prelude-remote.png)
