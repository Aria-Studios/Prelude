# TODO: fix styling in new window
# TODO: download/install related code

from tkinter import *
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
from discord_webhook import DiscordWebhook, DiscordEmbed
import os, urllib

import config, gui

# os.mkdir(config.privateBuildChannelName)
def messages():
    if (config.privateMessageFile != ''):
        try:
            messageContent = urllib.request.urlopen(config.urlPath + '/' + config.privateMessageFile).read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s ' + config.privateMessageFile + ' information file.\n\n' + str(e.reason), parent=gui.window)
            elif hasattr(e, 'code'):
                messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)

        messageContent = messageContent.decode('UTF-8')

        if (messageContent != ''):
            messagebox.showinfo(config.privateBuildChannelName + ' Build Channel Message', messageContent, parent=gui.window)

def discordNotification(name, pwd, var):
    webhook = DiscordWebhook(url=config.discordWebhookURL)

    if (var == 'Success' or var == 'Failure'):
        embed = DiscordEmbed(title='Updater Notification', description='User has attempted to authorize their computer for:')
        embed.add_embed_field(name='Game Title:', value=config.gameTitle)
        embed.add_embed_field(name='Channel:', value=config.privateBuildChannelName)
        embed.add_embed_field(name='User:', value=name, inline=False)
        embed.add_embed_field(name='Password:', value=pwd, inline=False)
        embed.add_embed_field(name='Result:', value=var, inline=False)
        embed.set_footer(text='Powered by Prelude v3')
    else:
        embed = DiscordEmbed(title='Updater Notification', description='User has attempted to use a ' + config.tokenFile + ' that does not match their computer.')
        embed.add_embed_field(name='Game Title:', value=config.gameTitle)
        embed.add_embed_field(name='Channel:', value=config.privateBuildChannelName)
        embed.add_embed_field(name='User:', value=name, inline=False)
        embed.add_embed_field(name='Password:', value=pwd, inline=False)
        embed.add_embed_field(name='Computer Login:', value=var, inline=False)
        embed.set_footer(text='Powered by Prelude v3')

    webhook.add_embed(embed)
    webhook.execute()

def checkStatus():
    try:
        remoteRaw = urllib.request.urlopen(config.urlPath + '/' + config.passwordFile).read()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s ' + config.passwordFile + ' information file.\n\n' + str(e.reason), parent=gui.window)
            gui.close()
        elif hasattr(e, 'code'):
            messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
            gui.close()
    else:
        remoteRaw = remoteRaw.decode('UTF-8')
        pwdList = remoteRaw.split('\r\n')

        if ('reset' in pwdList):
            os.remove(config.tokenFile)
            messagebox.showwarning(config.privateBuildChannelName + ' Authorization', 'Authorization status for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel has been reset by the ' + config.gameTitle + ' developers.\n\nYou will need to reauthorize this computer.', parent=gui.window)
            messages()

    try:
        file = open(config.tokenFile, 'rb')
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local ' + config.tokenFile + ' file cannot be found.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
        gui.close()
    else:
        key = Fernet(config.cryptKey)
        localToken = file.read()
        file.close()

        localToken = key.decrypt(localToken)
        localToken = localToken.decode('UTF-8')
        localToken = localToken.split('\n')

        if (os.getlogin() not in localToken):
            os.remove(config.tokenFile)

            if (config.discordWebhookURL != ''):
                discordNotification(localToken[0], localToken[1], os.getlogin())

            messagebox.showwarning(config.privateBuildChannelName + ' Authorization', 'The local ' + config.tokenFile + ' for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel is not correct.\n\nYou will need to reauthorize this computer.', parent=gui.window)

        if (os.path.exists(config.tokenFile) == True):
            gui.privateBuildChannel.entryconfigure('Authorization', state='disabled')
            gui.privateBuildChannel.entryconfigure('Install ' + config.privateBuildChannelName + ' Build', command=None, state=NORMAL)
            gui.privateBuildChannel.entryconfigure('Update ' + config.privateBuildChannelName + ' Build', command=None, state=NORMAL)

def authorization(authWindow, nameEntry, pwdEntry):
    try:
        remoteRaw = urllib.request.urlopen(config.urlPath + '/' + config.passwordFile).read()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s ' + config.passwordFile + ' information file.\n\n' + str(e.reason), parent=authWindow)
            gui.close()
        elif hasattr(e, 'code'):
            messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=authWindow)
            gui.close()
    else:
        remoteRaw = remoteRaw.decode('UTF-8')
        pwdList = remoteRaw.split('\r\n')
        pwdList.pop()

        if (pwdEntry in pwdList):
            key = Fernet(config.cryptKey)
            encToken = key.encrypt(bytes(nameEntry + '\n' + pwdEntry + '\n' + os.getlogin(), 'UTF-8'))

            file = open(config.tokenFile, 'wb')
            file.write(encToken)
            file.close()

            if (config.discordWebhookURL != ''):
                discordNotification(nameEntry, pwdEntry, 'Success')

            gui.privateBuildChannel.entryconfigure('Authorization', state='disabled')
            gui.privateBuildChannel.entryconfigure('Install ' + config.privateBuildChannelName + ' Build', command=None, state=NORMAL)
            gui.privateBuildChannel.entryconfigure('Update ' + config.privateBuildChannelName + ' Build', command=None, state=NORMAL)

            messagebox.showinfo(config.privateBuildChannelName + ' Authorization', 'Authorization Successful: your computer has been authorized for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel.\n\nPlease use the menu options to install & update the build as necessary.', parent=authWindow)
            messages()
            authWindow.destroy()
        else:
            if (config.discordWebhookURL != ''):
                discordNotification(nameEntry, pwdEntry, 'Failure')

            messagebox.showwarning(config.privateBuildChannelName + ' Authorization', 'Authorization Failed: your computer has not been authorized for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel.\n\nIf you believe this is in error, contact the ' + config.gameTitle + ' developers.', parent=authWindow)

#Please enter your information below in order to authorize your computer for the ' + config.privateBuildChannelName + ' build channel release. If successfully authorized, you may install and update the new build via the menubar. Your information may also be sent to the developer.'
def createAuthWindow():
    authWindow = Toplevel(gui.window)
    authWindow.title(config.privateBuildChannelName + ' Build Channel Authorization')
    authWindow.geometry('300x300')

    #authFrame = ttk.Frame(authWindow).grid(column=0, row=0)
    #expFrame = ttk.Frame(authFrame, width=300, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
    ttk.Label(authWindow, text='This is a placeholder.').grid(column=0, row=0, columnspan=2, rowspan=2, pady=10)
    ttk.Separator(authWindow, orient='horizontal').grid(column=0, row=2, columnspan=2, rowspan=1, sticky=N)

    # entryFrame = ttk.Frame(authFrame, width=300, height=50).grid(column=0, row=3, columnspan=2, rowspan=2, sticky=N)
    ttk.Label(authWindow, text='Name:').grid(column=0, row=3, columnspan=1, rowspan=1, pady=10)
    nameEntry = ttk.Entry(authWindow)
    nameEntry.grid(column=1, row=3, columnspan=1, rowspan=1, pady=10)
    ttk.Label(authWindow, text='Password:').grid(column=0, row=4, columnspan=1, rowspan=1, pady=10)
    pwdEntry = ttk.Entry(authWindow)
    pwdEntry.grid(column=1, row=4, columnspan=1, rowspan=1, pady=10)
    ttk.Separator(authWindow, orient='horizontal').grid(column=0, row=5, columnspan=2, rowspan=1, sticky=N)

    # submitFrame = ttk.Frame(authFrame, width=300, height=50).grid(column=0, row=6, columnspan=2, rowspan=2, sticky=N)
    authButton = ttk.Button(authWindow, text='Authorize', command=lambda: authorization(authWindow, nameEntry.get(), pwdEntry.get())).grid(column=0, row=6, columnspan=2, rowspan=1, sticky=N, pady=10)
    cancelButton = ttk.Button(authWindow, text='Close', command=authWindow.destroy).grid(column=0, row=7, columnspan=2, rowspan=1, sticky=N, pady=10)
