

# Prelude Updater
Prelude Updater is a simple update utility designed for use with Pokémon fangames made using Pokémon Essentials and RPG Maker XP. This was written in Python and developed/tested on Windows, but it should theoretically work on any OS (given the appropriate development environment to compile the executable file). Once you've edited the variables and compiled the code, you can include the executable file in your game download. This program can be launched in order to check for any updates that are available. It can also be used to download those updates.

# Getting Started
1. Read the *entire* [File Setup and Structure section](#File_Setup_and_Structure) below before proceeding!
1. When you're ready, install [Python](https://www.python.org/downloads/) (if it asks, be sure to install the tkinter module as well).
1. Install any other dependencies (the only one should be the [requests module](https://docs.python-requests.org/en/latest/user/install/#install)).
1. Grab a copy of the source code for this project.
1. Open the `updater.py` file and edit the values at the beginning of the file; save and close the file.
1. Install [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html) and [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/).
1. Use one of the above to compile the source code into an executable file. auto-py-to-exe provides an easy to use GUI, while pyinstaller is a CLI program. I recommend auto-py-to-exe for simplicity's sake.
1. Setup the remote file structure, including the `version` information file.
1. Include the executable file and `version` information file in your base game download.

# File Setup and Structure
This section goes over how the program operates and should help you make the most of it, while reducing any errors experienced.

## "core" vs "patch"
One of the first things to understand is that this program operates under the assumption that you use two different kind of updates: core and patch. Core releases are major releases which add or edit a large number of files, wherein it is easier/better to assume that you need to ship the whole game package again rather than attempting to create a patch download. Patch releases are minor releases that add or edit a smaller number of files; additionally, this type of release is cumulative to the last core release you published.

## `version`
`version` is a simple file that contains a float value with your release information. As it is a float value (with up to two decimal points of precision), you should use a scheme such as `1.21` for version information. For our purposes, the program views the whole number (`1.##`) as the core release, and the decimal places (`#.01`) as patch releases. One important point to keep in mind with this program is that it cannot recognize the difference between values like `1.1` and `1.10`. This file is used in several different places, both remotely and locally and will be covered more later.

## `updater.py`
`updater.py` contains a few variables which are used in order to pull information from the local game installation and your remote server.

```Python
gameTitle = 'Game Title'
gameURL = 'https://reliccastle.com'
urlPath = 'http://domain.com/directory'
versionFile = 'version'
patchArchive = 'patch.zip'
coreArchive = 'core.zip'
```

* `gameTitle` is fairly self explanatory, it will insert your game's title into all the appropriate spots in the program interface.
* `gameURL` can be used for any URL you choose, such as a project thread on Relic Castle or a custom website. It will launch if the appropriate options is selected in the menu bar.
* `urlPath` is the *remote* URL path to the directory where your files will be stored. For example, if your website is `https://domain.com` and you will host the files in the `downloads` directory, you would put `https://domain.com/downloads` for this variable.
* `versionFile` is the name of the *local* ***and*** *remote* files that contain your version information. I recommend leaving it as the default `version` which can be edited fairly easily but will discourage users from tampering with it.
* `patchArchive` is the name of the *remote* ***zip*** archive that contains your latest patch/minor release.
* `coreArchive` is the name of the *remote* ***zip*** archive that contains your latest core/major release.

## `patch.zip`
The `patch.zip` archive should contain a copy of all files that have been updated since the latest ***core*** release -- in other words, it is a cumulative patch, not sequential. It should also be setup so that files can be directly unzipped from the game folder. This should also contain an updated `version` information file that matches to this patch release, which will overwrite the user's local copy when they update. See the screenshot below for what an example setup should look like.

![Example of patch.zip layout.](https://media.ariastudio.dev/misc/prelude-patch.png)

## `core.zip`
The `core.zip` archive should contain a copy of the full game directory. It should also be setup so that files can be directly unzipped from the game folder. This should also contain a `version` information file that matches to this core release. See the screenshot below for what an example setup should look like.

![Example of core.zip layout.](https://media.ariastudio.dev/misc/prelude-core.png)

## Local (Game Folder)
Locally, this program works off the assumption that it will be run in the same location as your game executable. This means that you'll need to include two (2) files with your base game: the `updater` executable and `version` information file. See the screenshot below for what an example setup should look like.

![Example of local folder layout.](https://media.ariastudio.dev/misc/prelude-local.png)

## Remote (Downloads Folder)
On the remote server, the setup is fairly simple: pick a location and put the `version` information file, `patch.zip` archive, and `core.zip` archive there. As long as it can be reached by an HTTP request, then the program can function correctly. See the screenshot below for what an example setup should look like.

![Example of remote folder layout.](https://media.ariastudio.dev/misc/prelude-remote.png)
