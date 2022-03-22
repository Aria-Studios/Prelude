# v1 - March 2022
* Initial release.

# v2 - TBA
* Code reorganization: the base code is now split up into several different files based on their use.
* Improved error handling: includes elegant error messages for corrupted zip archives and files in use by other programs and unable to be overwritten.
* Basic space warning: before the download process begins on any update, it will check the remote zip archive size and your available space, and it will warn if you there may not be enough room for the file (update process will still continue as normal).
* Improved Prelude updating procedure: the program will now check if there is a copy of itself within a downloaded zip archive and display a warning message that the archive must be manually installed by extracting the archive directly to the game directory before closing. More on this in the readme.
