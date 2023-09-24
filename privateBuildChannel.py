# import relevant modules & script files
from tkinter import *
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
from discord_webhook import DiscordWebhook, DiscordEmbed
import lzma, os, py7zr, urllib

import setup, gui

# checks to see if any messages can or should be displayed and does so
def messages():
    if (setup.privateBuildChannelAuthMethod == 'none' or (setup.privateBuildChannelAuthMethod == 'password' and os.path.exists('authToken') == True)):
        try:
            messageContent = urllib.request.urlopen(setup.privateBuildChannelURLPath + '/privateMessage').read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s private message information file.\n\n' + str(e.reason), parent=gui.window)
            elif hasattr(e, 'code'):
                messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
        else:
            messageContent = messageContent.decode('UTF-8')
            if (messageContent != ''):
                messagebox.showinfo(setup.privateBuildChannelName + ' Build Channel Message', messageContent, parent=gui.window)

# sends notification to specified Discord webhook based on passed variables
def discordNotification(name, pwd, var):
    webhook = DiscordWebhook(url=setup.discordWebhookURL)

    embed = DiscordEmbed(title='Updater Notification')
    embed.add_embed_field(name='Game Title:', value=setup.gameTitle)
    embed.add_embed_field(name='Channel:', value=setup.privateBuildChannelName)
    embed.add_embed_field(name='User:', value=name, inline=False)
    embed.add_embed_field(name='Password:', value=pwd, inline=False)
    if (var == 'Success' or var == 'Failure'):
        embed.set_description('User has attempted to authorize their computer for:')
        embed.add_embed_field(name='Result:', value=var, inline=False)
    else:
        embed.set_description('User has attempted to use an authToken file that does not match their computer.')
        embed.add_embed_field(name='Computer Login:', value=var, inline=False)
    embed.set_footer(text='Powered by Prelude v3')

    webhook.add_embed(embed)
    webhook.execute()

# checks the authorization status of the computer, based on the authMethod
def checkStatus():
    # enables the install options if authMethod is "none"
    if (setup.privateBuildChannelAuthMethod == 'none'):
        gui.privateBuildChannel.entryconfigure('Install Latest ' + setup.privateBuildChannelName + ' Build', state=NORMAL)
    elif (setup.privateBuildChannelAuthMethod == 'password'):
        if (os.path.exists('authToken') == True):
            # checks if the remote passwordFile for "reset" in order to reset auth status
            try:
                remoteRaw = urllib.request.urlopen(setup.privateBuildChannelURLPath + '/passwords').read()
            except urllib.error.URLError as e:
                if hasattr(e, 'reason'):
                    messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s password information file.\n\n' + str(e.reason), parent=gui.window)
                    gui.close()
                elif hasattr(e, 'code'):
                    messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
                    gui.close()
            else:
                remoteRaw = remoteRaw.decode('UTF-8')
                pwdList = remoteRaw.split('\r\n')

                if ('reset' in pwdList):
                    messages()
                    os.remove('authToken')
                    messagebox.showwarning(setup.privateBuildChannelName + ' Authorization', 'Authorization status for the ' + setup.gameTitle + ' ' + setup.privateBuildChannelName + ' build channel has been reset by the ' + setup.gameTitle + ' developers.\n\nYou will need to reauthorize this computer at a later date.', parent=gui.window)

            # checks if the tokenFile details match the current computer
        if (os.path.exists('authToken') == True):
            try:
                file = open('authToken', 'rb')
            except FileNotFoundError:
                messagebox.showerror('Prelude Error', 'Local authToken file cannot be found.\n\nContact the ' + setup.gameTitle + ' developers.', parent=gui.window)
                gui.close()
            else:
                key = Fernet(setup.privateBuildChannelEncKey)
                localToken = file.read()
                file.close()

                localToken = key.decrypt(localToken)
                localToken = localToken.decode('UTF-8')
                localToken = localToken.split('\n')

                if (os.getlogin() not in localToken):
                    os.remove('authToken')

                    if (setup.discordWebhookURL != ''):
                        discordNotification(localToken[0], localToken[1], os.getlogin())

                    messagebox.showwarning(setup.privateBuildChannelName + ' Authorization', 'The local authToken file for the ' + setup.gameTitle + ' ' + setup.privateBuildChannelName + ' build channel is not correct.\n\nYou will need to reauthorize this computer.', parent=gui.window)

            # if the tokenFile still exists, enable the install options
            if (os.path.exists('authToken') == True):
                gui.privateBuildChannel.entryconfigure('Authorization', state='disabled')
                if (os.path.exists(setup.privateBuildChannelName) == True):
                    gui.privateBuildChannel.entryconfigure('Install Latest ' + setup.privateBuildChannelName + ' Build', state=NORMAL)
                else:
                    gui.privateBuildChannel.entryconfigure('Install Latest ' + setup.privateBuildChannelName + ' Build', state=NORMAL)

        # if the tokenFile never existed, enables the authorization option
        else:
            gui.privateBuildChannel.entryconfigure('Authorization', state=NORMAL)

# checks the user input to see if it can authorize the computer
def authorization(authWindow, nameEntry, pwdEntry):
    try:
        remoteRaw = urllib.request.urlopen(setup.privateBuildChannelURLPath + '/passwords').read()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s password information file.\n\n' + str(e.reason), parent=authWindow)
            gui.close()
        elif hasattr(e, 'code'):
            messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=authWindow)
            gui.close()
    else:
        remoteRaw = remoteRaw.decode('UTF-8')
        pwdList = remoteRaw.split('\r\n')

        if (pwdList[len(pwdList)-1] == ''):
            pwdList.pop()

        # if the auth status has been reset, do not allow it to re-authorize
        if ('reset' in pwdList):
            messagebox.showwarning(setup.privateBuildChannelName + ' Authorization', 'Authorization status for the ' + setup.gameTitle + ' ' + setup.privateBuildChannelName + ' build channel has been reset by the ' + setup.gameTitle + ' developers.\n\nYou will need to reauthorize this computer at a later date.', parent=gui.window)
            authWindow.destroy()
        # if the entered password matches, create the tokenFile to store auth status, also enables the install options immediately
        elif (pwdEntry in pwdList):
            key = Fernet(setup.privateBuildChannelEncKey)
            encToken = key.encrypt(bytes(nameEntry + '\n' + pwdEntry + '\n' + os.getlogin(), 'UTF-8'))

            file = open('authToken', 'wb')
            file.write(encToken)
            file.close()

            if (setup.discordWebhookURL != ''):
                discordNotification(nameEntry, pwdEntry, 'Success')

            gui.privateBuildChannel.entryconfigure('Authorization', state='disabled')
            gui.privateBuildChannel.entryconfigure('Install Latest ' + setup.privateBuildChannelName + ' Build', state=NORMAL)

            messagebox.showinfo(setup.privateBuildChannelName + ' Authorization', 'Authorization Successful: your computer has been authorized for the ' + setup.gameTitle + ' ' + setup.privateBuildChannelName + ' build channel.\n\nPlease use the menu options to install & update the build as necessary.', parent=authWindow)
            messages()
            authWindow.destroy()
        # if the entered password did not match, displays message and allows more attempts
        else:
            if (setup.discordWebhookURL != ''):
                discordNotification(nameEntry, pwdEntry, 'Failure')

            messagebox.showwarning(setup.privateBuildChannelName + ' Authorization', 'Authorization Failed: your computer has not been authorized for the ' + setup.gameTitle + ' ' + setup.privateBuildChannelName + ' build channel.\n\nIf you believe this is in error, contact the ' + setup.gameTitle + ' developers.', parent=authWindow)

def testAuth(authWindow, nameEntry, pwdEntry, updateTarget):
    try:
        updateFile = py7zr.SevenZipFile(updateTarget, mode='r')
    except py7zr.PasswordRequired:
        flag = False
        while (flag == False):
            try:
                updateFile = py7zr.SevenZipFile(updateTarget, mode='r', password=pwdEntry)
                updateFile.extractall(path=setup.privateBuildChannelName)
                updateFile.close()
                authWindow.destroy()
            except lzma.LZMAError:
                messagebox.showwarning(setup.privateBuildChannelName + ' Authorization', 'Authorization Failed: your computer has not been authorized for the ' + setup.gameTitle + ' ' + setup.privateBuildChannelName + ' build channel.\n\nIf you believe this is in error, contact the ' + setup.gameTitle + ' developers.', parent=authWindow)

# creates the authorization GUI window
def testPassword(updateTarget):
    authWindow = Toplevel(gui.window)
    authWindow.title(setup.privateBuildChannelName + ' Build Channel Authorization')
    authWindow.geometry('300x250')

    expFrame = ttk.Frame(authWindow, width=300, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
    ttk.Label(authWindow, text='Please enter your information below in order to authorize your computer for the ' + setup.privateBuildChannelName + ' build channel release. If successfully authorized, you may install and update the new build via the menubar. Your information may also be sent to the developer.', wraplength=250).grid(column=0, row=0, columnspan=2, rowspan=2, pady=10)
    ttk.Separator(authWindow, orient='horizontal').grid(column=0, row=2, columnspan=2, rowspan=1, sticky=N)

    entryFrame = ttk.Frame(authWindow, width=300, height=50).grid(column=0, row=3, columnspan=2, rowspan=2, sticky=N)
    ttk.Label(authWindow, text='Name:').grid(column=0, row=3, columnspan=1, rowspan=1, pady=10)
    nameEntry = ttk.Entry(authWindow)
    nameEntry.grid(column=1, row=3, columnspan=1, rowspan=1, pady=10)
    ttk.Label(authWindow, text='Password:').grid(column=0, row=4, columnspan=1, rowspan=1, pady=10)
    pwdEntry = ttk.Entry(authWindow)
    pwdEntry.grid(column=1, row=4, columnspan=1, rowspan=1, pady=10)
    ttk.Separator(authWindow, orient='horizontal').grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N)

    submitFrame = ttk.Frame(authWindow, width=300, height=50).grid(column=0, row=6, columnspan=2, rowspan=2, sticky=N)
    authButton = ttk.Button(authWindow, text='Authorize', command=lambda: testAuth(authWindow, nameEntry.get(), pwdEntry.get(), updateTarget)).grid(column=0, row=6, columnspan=1, rowspan=1, sticky=N, pady=10)
    cancelButton = ttk.Button(authWindow, text='Close', command=authWindow.destroy).grid(column=1, row=6, columnspan=1, rowspan=1, sticky=N, pady=10)