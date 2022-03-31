from tkinter import *
from tkinter import messagebox, ttk
import urllib

import config, gui

# if pwd is 'reset' then authorization status is cleared
def authorization(pwdEntry):
    authStatus = False

    try:
        remoteRaw = urllib.request.urlopen(config.urlPath + '/' + config.passwordFile).read()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s ' + config.passwordFile + ' information file.\n' + str(e.reason), parent=authWindow)
        elif hasattr(e, 'code'):
            messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n' + str(e.code), parent=authWindow)
    else:
        remoteRaw = remoteRaw.decode('UTF-8')
        pwdList = remoteRaw.split('\r\n')

        print(pwdEntry)
        print(pwdList)

        for temp in pwdList:
            if (temp == pwdEntry):
                authStatus = True
                break

        if (authStatus == True):
            print('auth worked')
        else:
            print('auth did not work')

#Please enter your information below in order to authorize your computer for the ' + config.privateBuildChannelName + ' build channel release. If successfully authorized, you may install and update the new build via the menubar. Your information may also be sent to the developer.'
def authWindow():
    authWindow = Toplevel(gui.window)
    authWindow.title(config.privateBuildChannelName + ' Build Channel Authorization')
    authWindow.geometry('300x300')

    #authFrame = ttk.Frame(authWindow).grid(column=0, row=0)
    #expFrame = ttk.Frame(authFrame, width=300, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
    ttk.Label(authWindow, text='This is a placeholder.').grid(column=0, row=0, columnspan=2, rowspan=2, pady=10)
    ttk.Separator(authWindow, orient='horizontal').grid(column=0, row=2, columnspan=2, rowspan=1, sticky=N)

    # entryFrame = ttk.Frame(authFrame, width=300, height=50).grid(column=0, row=3, columnspan=2, rowspan=2, sticky=N)
    ttk.Label(authWindow, text='Name:').grid(column=0, row=3, columnspan=1, rowspan=1, pady=10)
    nameEntry = ttk.Entry(authWindow).grid(column=1, row=3, columnspan=1, rowspan=1, pady=10)
    ttk.Label(authWindow, text='Password:').grid(column=0, row=4, columnspan=1, rowspan=1, pady=10)
    pwdEntry = ttk.Entry(authWindow).grid(column=1, row=4, columnspan=1, rowspan=1, pady=10)
    ttk.Separator(authWindow, orient='horizontal').grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N)

    # submitFrame = ttk.Frame(authFrame, width=300, height=50).grid(column=0, row=6, columnspan=2, rowspan=2, sticky=N)
    authButton = ttk.Button(authWindow, text='Authorize', command=lambda: authorization(pwdEntry)).grid(column=0, row=6, columnspan=2, rowspan=1, sticky=N, pady=10)
    cancelButton = ttk.Button(authWindow, text='Cancel', command=authWindow.destroy).grid(column=0, row=7, columnspan=2, rowspan=1, sticky=N, pady=10)
