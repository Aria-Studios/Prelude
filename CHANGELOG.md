# v3 - ~~April 2022~~ July 2023
> Note: v3 is an large improvement over previous versions, but work has begun on v4 which is planned to be an overhaul of the application that removes the need for you to build your own executable for each individual game. v3 should be 100% stable, but was not tested quite as thoroughly as v1 or v2 before the "official" release. That being said, it should be fine for usage, but we encourage you to wait for v4 if possible.

***Updated Module Requirements*** - Prelude now requires the [cryptography](https://pypi.org/project/cryptography/) and [discord-webhook](https://github.com/lovvskillz/python-discord-webhook) modules in addition to those previously required. Be sure to install those before updating to v3.
* Private Build Channel: a new feature which allows you to deploy and manage a secondary release channel, for use cases such as testing or early access builds.
* Installer friendly setup: if you set the local version to 0, the GUI will now say "install" instead of "update". This expands on your ability to ship a small initial download package with only the program files, which handle the actual game files for the users. Additionally, you can define a static message in the config values to be displayed when the local version is 0.
* Progress bar, now progressing: the progress bar has now been tied into the download process, so it will reflect the download progress! Shout out to [enumag](https://gitlab.com/enumag) for the assistance here!
* Improved memory usage: the archives used to be downloaded in full to the computer's RAM, before being written to the HDD. As part of the work on the progress bar, we fixed that so the process happens in much smaller incremental chunks. Shout out to [enumag](https://gitlab.com/enumag) for the assistance here!
* Code cleanup: as part of v2, the error handling was spun out into its own file, but this had the unintentional side effect of making it so some actions were being performed twice. After learning more about error handling, we've merged those functions back into the core script.
* Miscellaneous bug fixes:
  * The automatic update process will now disable the manual download options as there was some confusion on what to do there.
  * The local version file not found error was a bit vague, so we added some additional wording to make it clear that the program needs to be run in the same directory as the local version file.

# v2 - March 2022
* Code reorganization: the base code is now split up into several different files based on their use.
* Improved error handling: includes elegant error messages for corrupted zip archives and files in use by other programs and unable to be overwritten.
* Basic space warning: before the download process begins on any update, it will check the remote zip archive size and your available space, and it will warn if you there may not be enough room for the file (update process will still continue as normal).
* Improved Prelude updating procedure: the program will now check if there is a copy of itself within a downloaded zip archive and display a warning message that the archive must be manually installed by extracting the archive directly to the game directory before closing. More on this in the readme.

# v1 - March 2022
* Initial release.
