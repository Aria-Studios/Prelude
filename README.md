![Prelude interface.](https://media.ariastudio.dev/misc/prelude.png)

# Prelude
Prelude is a simple update utility designed for use with Pokémon fangames made using Pokémon Essentials and RPG Maker XP. It is written using Python 3.10.2 and developed/tested on Windows, but it should theoretically work on any OS (given the appropriate development environment to compile the executable file). Once you've edited the variables and compiled the code, you can include the executable file in your base game download. This program can be launched in order to check for any updates that are available, then download and install those updates automatically. The program also has the functionality to display a message to users if there is something important that needs to be communicated to them.

# Features
* Check the game version, both locally and remotely
* Download and install the latest updates for a game
* Display a message through the program which can be changed remotely at any time

# Getting Started
## Requirements
* [Python](https://www.python.org/downloads/)
 * tkinter (be sure to select the option that includes this when you install Python)
 * [requests](https://docs.python-requests.org/en/latest/user/install/#install)
* [pyinstaller](https://pyinstaller.readthedocs.io/en/stable/installation.html)
* [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/)
* Remote server to store the files

## Installation
1. Read the ***entire*** [File Setup and Structure section](#file-setup-and-structure) below before proceeding!
1. When you're ready, install Python (be sure to add `python` to your PATH), pyinstaller, auto-py-to-exe, and the two modules listed above.
1. Grab the [latest release](https://gitlab.com/ariastudios/prelude/-/releases) of the source code.
1. Setup the remote server's file structure similarly to how it was illustrated below.
1. Using the remote server's information, edit the values at the beginning of `updater.py`.
1. Using either auto-py-to-exe (a GUI-based program) or pyinstaller (a CLI-based program), compile the source code into an executable file. I recommend auto-py-to-exe for the sake of simplicity.
1. Test the resulting program in order to make sure that everything functions correctly.
1. Begin including the necessary files in your game downloads.

# File Setup and Structure
This section goes over how the program operates and should help you make the most of it, while reducing any errors experienced.

## "core" vs "patch"
One of the first things to understand is that this program operates under the assumption that you use two different kind of updates: core and patch. Core releases are major releases which add or edit a large number of files, wherein it is easier/better to assume that you need to ship the whole game package again rather than attempting to create a patch download. Patch releases are minor releases that add or edit a smaller number of files; additionally, this type of release is ***cumulative*** to the last core release you published.

## `version`
`version` is a simple file that contains a float (number with a decimal place) value with your release information. This program is capable of up to four decimal points of precision (over 9000 patch releases), but has only been tested extensively using two decimal points of precision. As such, we recommend the use of a version scheme such as `1.23` for your project. The program will view the whole number (`1.##`) as the core release and the decimal places (`#.23`) as the patch release. One important point to keep in mind with this program is that it cannot recognize the difference between values like `1.1` and `1.10`. Another is that the `version` file that is distributed in your `core.zip` and `patch.zip` should always match with the remote server's `version` file.

## `message`
`message` is what enables you to communicate any important information to users, hosted only in your remote server directory. You could use this for anything, such as communicating that the next release will be a large core download or if there are special events ongoing in your game (such as a Mystery Gift). If the file has content, the message will automatically be displayed when the program is started. After it has been dismissed, it can be displayed again via the relevant menu option. If the file is *empty*, the program will not display anything when started. If you did not define a value for the message file, the program will not check for messages when started and the menu item will be disabled. If you defined a value for the message file, but the file is not present in your remote server directory, the program will display an error message anytime it is started or if the menu item is triggered. See the screenshot below for what an example message can look like.

![Example of displayed message.](https://media.ariastudio.dev/misc/prelude-message.png)

## `updater.py`
`updater.py` contains the code which runs the program, as well as several values that you ***must*** set in order for the program to function. These are what defines what files the program will look for and where it will look for them. One *very* important thing to note is that the program cannot update itself as part of the update process; in other words, if you need to change these values at a later point, you'll need to distribute an updated executable file which can then replace the old executable.

```Python
gameTitle = 'Game Title'
gameURL = 'https://reliccastle.com'
urlPath = 'http://domain.com/directory'
messageFile = 'message'
versionFile = 'version'
coreArchive = 'core.zip'
patchArchive = 'patch.zip'
```

* `gameTitle` (optional) is fairly self explanatory, it will insert your game's title into all the appropriate spots in the program interface. If you do not define this, it can result in obviously empty spots in the program interface.
* `gameURL` (optional) can be used for any URL you choose, such as a project thread on Relic Castle or a custom website, which can be launched from the relevant menu item in the program. If this is not defined, the menu item will be disabled.
* `urlPath` (required) is the *remote* URL path to the directory where your files will be stored. For example, if your website is `https://domain.com` and you will host the files in the `downloads` directory, you would put `https://domain.com/downloads` for this.
* `messageFile` (optional) is the name of the *remote* file that contains any messages you want to display to users.
* `versionFile` (required) is the name of the *local* ***and*** *remote* files that contain your version information. I recommend leaving it as the default `version` which can be edited fairly easily but will discourage users from tampering with it.
* `coreArchive` (required) is the name of the *remote* ***zip*** archive that contains your latest core release.
* `patchArchive` (required) is the name of the *remote* ***zip*** archive that contains your latest patch release.

## `core.zip`
The `core.zip` archive should contain a copy of the full game directory. It should also be setup so that files can be directly unzipped from the game folder. This should contain a `version` information file that matches to this core release, which will overwrite the user's current local copy when they update. See the screenshot below for what an example setup should look like.

![Example of core.zip layout.](https://media.ariastudio.dev/misc/prelude-core.png)

## `patch.zip`
The `patch.zip` archive should contain a copy of ***all files that have been updated since the latest core release*** -- in other words, it is a cumulative patch, not sequential. It should also be setup so that files can be directly unzipped from the game folder. This should contain an updated `version` information file that matches to this patch release, which will overwrite the user's current local copy when they update. See the screenshot below for what an example setup should look like.

![Example of patch.zip layout.](https://media.ariastudio.dev/misc/prelude-patch.png)

## Local (Game Folder)
Locally, this program works off the assumption that it will be run in the same location as your game executable. This means that you'll need to include two (2) files with your base game: the `updater` executable and `version` information file. See the screenshot below for what an example setup should look like.

![Example of local folder layout.](https://media.ariastudio.dev/misc/prelude-local.png)

## Remote (Downloads Directory)
On the remote server, the setup is fairly simple: pick a location and put the `version` information file, `core.zip` archive, `patch.zip` archive, and the `message` information file (if you're making use of this feature) there. As long as it can be reached by a standard HTTP request, then the program can function correctly. See the screenshot below for what an example setup should look like.

![Example of remote folder layout.](https://media.ariastudio.dev/misc/prelude-remote.png)

# Future Plans
* Add more error handling.
* Cleaning up the code organization.
* Alpha/beta track releases.
