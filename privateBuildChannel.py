# import relevant modules & script files
from tkinter import *
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet
from discord_webhook import DiscordWebhook, DiscordEmbed
import lzma, os, py7zr, sys, threading, urllib

import config, gui

# checks to see if any messages can or should be displayed and does so
def messages():
    if (config.privateBuildChannelAuthMethod != ''):
        try:
            messageContent = urllib.request.urlopen(config.privateBuildChannelURLPath + '/privateMessage').read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                messagebox.showerror('Prelude Error', 'Failed to reach the remote server\'s private message information file.\n\n' + str(e.reason), parent=gui.window)
            elif hasattr(e, 'code'):
                messagebox.showerror('Prelude Error', 'Server could not fulfill the request.\n\n' + str(e.code), parent=gui.window)
        else:
            messageContent = messageContent.decode('UTF-8')
            if (messageContent != ''):
                messagebox.showinfo(config.privateBuildChannelName + ' Build Channel Message', messageContent, parent=gui.window)
    
        gui.privateBuildChannel.entryconfigure('Display ' + config.privateBuildChannelName + ' Build Messages', state=NORMAL)

# sends notification to specified Discord webhook based on passed variables
def discordNotification(name, pwd, var):
    webhook = DiscordWebhook(url=config.discordWebhookURL)

    embed = DiscordEmbed(title='Updater Notification')
    embed.add_embed_field(name='Game Title:', value=config.gameTitle)
    embed.add_embed_field(name='Channel:', value=config.privateBuildChannelName)
    embed.add_embed_field(name='User:', value=name, inline=False)
    embed.add_embed_field(name='Password:', value=pwd, inline=False)
    if (var == 'Success' or var =='Failure'):
        embed.set_description('User has attempted to authorize their computer for:')
        embed.add_embed_field(name='Result:', value=var, inline=False)
    else:
        embed.set_description('User has attempted to use an authToken file that does not match their computer or the archive password.')
        embed.add_embed_field(name='Computer Login:', value=var, inline=False)
    embed.set_footer(text='Powered by Prelude v4 (Alpha)')

    webhook.add_embed(embed)
    webhook.execute()

def checkAuth(updateTarget, flag):
    try:
        file = open('authToken', 'rb')
    except FileNotFoundError:
        messagebox.showerror('Prelude Error', 'Local authToken file cannot be found.\n\nContact the ' + config.gameTitle + ' developers.', parent=gui.window)
    else:
        key = Fernet(config.privateBuildChannelEncKey)
        localToken = file.read()
        file.close()

        localToken = key.decrypt(localToken)
        localToken = localToken.decode('UTF-8')
        localToken = localToken.split('\n')

        if (os.getlogin() not in localToken):
            os.remove('authToken')
            if (config.discordWebhookURL != ''):
                discordNotification(localToken[0], localToken[1], os.getlogin())

            messagebox.showwarning(config.privateBuildChannelName + ' Authorization', 'The local authToken file for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel is not correct.\n\nYou will need to reauthorize this computer.', parent=gui.window)
            createAuthWindow(updateTarget, flag)
        else:
            try:
                updateFile = py7zr.SevenZipFile(updateTarget, mode='r')
            except py7zr.PasswordRequired:
                try:
                    updateFile = py7zr.SevenZipFile(updateTarget, mode='r', password=localToken[1])

                    updateFile.extractall(path=config.privateBuildChannelName)
                    updateFile.close()
                    flag.set()
                except lzma.LZMAError:
                    os.remove('authToken')
                    if (config.discordWebhookURL != ''):
                        discordNotification(localToken[0], localToken[1], os.getlogin())

                    messagebox.showwarning(config.privateBuildChannelName + ' Authorization', 'The local authToken file for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel is not correct.\n\nYou will need to reauthorize this computer.', parent=gui.window)
                    createAuthWindow(updateTarget, flag)

def createAuth(authWindow, nameEntry, pwdEntry, updateTarget, flag):
    try:
        updateFile = py7zr.SevenZipFile(updateTarget, mode='r')
    except py7zr.PasswordRequired:
        try:
            updateFile = py7zr.SevenZipFile(updateTarget, mode='r', password=pwdEntry)
            
            if (config.privateBuildChannelEncKey != ''):
                key = Fernet(config.privateBuildChannelEncKey)
                encToken = key.encrypt(bytes(nameEntry + '\n' + pwdEntry + '\n' + os.getlogin(), 'UTF-8'))

                file = open('authToken', 'wb')
                file.write(encToken)
                file.close()

            if (config.discordWebhookURL != ''):
                discordNotification(nameEntry, pwdEntry, 'Success')
            
            messagebox.showinfo(config.privateBuildChannelName + ' Authorization', 'Authorization Successful: your computer has been authorized for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel.', parent=authWindow)

            authWindow.destroy()

            if (os.path.basename(sys.argv[0]) in updateFile.getnames()):
                for fileName in updateFile.getnames():
                    if (fileName == os.path.basename(sys.argv[0])):
                        updateFile.extract(path='Scripts', targets=os.path.basename(sys.argv[0]))
                        os.rename('Scripts/' + os.path.basename(sys.argv[0]), 'new-' + os.path.basename(sys.argv[0]))
                    else:
                        updateFile.extract(fileName)
                    updateFile.reset()
            else:
                updateFile.extractall(path=config.privateBuildChannelName)
            updateFile.close()
            flag.set()
        except lzma.LZMAError:
            if (config.discordWebhookURL != ''):
                discordNotification(nameEntry, pwdEntry, 'Failure')

            messagebox.showwarning(config.privateBuildChannelName + ' Authorization', 'Authorization Failed: your computer has not been authorized for the ' + config.gameTitle + ' ' + config.privateBuildChannelName + ' build channel.\n\nIf you believe this is in error, contact the ' + config.gameTitle + ' developers.', parent=authWindow)

# creates the authorization GUI window
def createAuthWindow(updateTarget, flag):
    authWindow = Toplevel(gui.window)
    authWindow.title(config.privateBuildChannelName + ' Build Channel Authorization')
    authWindow.geometry('300x250')

    expFrame = ttk.Frame(authWindow, width=300, height=50).grid(column=0, row=0, columnspan=2, rowspan=2, sticky=N)
    ttk.Label(authWindow, text='Please enter your information below in order to authorize your computer for the ' + config.privateBuildChannelName + ' build channel release. Your information may also be sent to the developer and stored on your computer for future updates.', wraplength=250).grid(column=0, row=0, columnspan=2, rowspan=2, pady=10)
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
    authButton = ttk.Button(authWindow, text='Authorize', command=lambda: createAuth(authWindow, nameEntry.get(), pwdEntry.get(), updateTarget, flag)).grid(column=0, row=6, columnspan=1, rowspan=1, sticky=N, pady=10)
    cancelButton = ttk.Button(authWindow, text='Close', command=authWindow.destroy).grid(column=1, row=6, columnspan=1, rowspan=1, sticky=N, pady=10)