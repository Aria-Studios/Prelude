from tkinter import *
from tkinter import messagebox, ttk
import os, requests, sys, urllib, zipfile

import config, gui

# Error handling for checking to see if local files exist
def localCheck(fileToCheck):
    if (fileToCheck == config.versionFile):
        try:
            open(fileToCheck)
        except FileNotFoundError:
            messagebox.showerror('Prelude Error', 'Local ' + fileToCheck + ' information file cannot be found.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
            gui.close()
        else:
            try:
                float(open(fileToCheck).read())
            except ValueError:
                messagebox.showerror('Prelude Error', 'Local ' + fileToCheck + ' information file contains invalid contents.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
                gui.close()
            else:
                return False
    else:
        try:
            updateFile = zipfile.ZipFile(fileToCheck, 'r')
            updateFile.extractall()
        except FileNotFoundError:
            messagebox.showerror('Prelude Error', 'Local archive ' + fileToCheck + ' cannot be found.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
            gui.close()
        except zipfile.BadZipFile:
            messagebox.showerror('Prelude Error', 'Local archive ' + fileToCheck + ' is corrupted.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
            gui.close()
        except PermissionError:
            if (os.path.basename(sys.argv[0]) in updateFile.namelist()):
                messagebox.showwarning('Prelude Warning', 'Warning: this update must be manually installed. Please extract the ' + fileToCheck + ' archive directly into the game directory.', parent=gui.window)
                gui.close()
            else:
                messagebox.showerror('Prelude Error', 'Local archive ' + fileToCheck + ' contains files currently being used by other programs.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
                gui.close()
        else:
            return False

# Error handling for checking to see if remote files can be reached
def remoteCheck(fileToCheck):
    try:
        urllib.request.urlopen(config.urlPath + '/' + fileToCheck).read()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s ' + fileToCheck + ' information file.\n' + str(e.reason), parent=gui.window)
            if (fileToCheck == config.versionFile):
                gui.close()
        elif hasattr(e, 'code'):
            messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n' + str(e.code), parent=gui.window)
            if (fileToCheck == config.versionFile):
                gui.close()
    else:
        if (fileToCheck == config.versionFile):
            try:
                float(urllib.request.urlopen(config.urlPath + '/' + fileToCheck).read())
            except ValueError:
                messagebox.showerror('Prelude Error', 'Remote ' + fileToCheck + ' information file contains invalid contents.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
                gui.close()
            else:
                return False
        return False

# Error handling for downloading zip archives
def downloadCheck(fileToCheck):
    try:
        dl = requests.get(config.urlPath + '/' + fileToCheck, timeout=30)
        dl.raise_for_status()
    except requests.exceptions.HTTPError as error:
        messagebox.showerror('Prelude Error', 'HTTP error: #' + str(error) + '.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.ConnectionError:
        messagebox.showerror('Prelude Error', 'Connection error. \nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.TooManyRedirects:
        messagebox.showerror('Prelude Error', 'Server connection exceeded maximum number of redirects.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    except requests.exceptions.Timeout:
        messagebox.showerror('Prelude Error', 'Server connection timed out, try again later.', parent=gui.window)
        gui.close()
    except requests.exceptions.RequestException as error:
        messagebox.showerror('Prelude Error', 'Error: ' + str(error) + '.\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    else:
        return False
