import os
import ftplib
Host = 'YourHostAddress'
Port = '21'
Username = 'YourServerUsername'
Password = 'YourServerPassword'
LocalDirFile = 'ModDirectory.txt'


def main(host, user, password, port='21'):
    if not os.path.exists(LocalDirFile):
        InstancesDir = input('[First Time Setup]> Please Paste Your Mod Folder Location Here: ')
        with open(LocalDirFile, 'w') as file:
            file.write(InstancesDir)
    else:
        with open(LocalDirFile, 'r') as file:
            InstancesDir = file.read()
    success, param2 = getLocalModsList(InstancesDir)
    if not success:
        print('Could Not Retrieve Local Mods: ' + param2)
        print('Resetting Directory Folder...\n')
        if os.path.exists(LocalDirFile):
            os.remove(LocalDirFile)
        main()
        exit()
    modsInstalled = param2
    print('Total Mods Installed: ' + str(len(modsInstalled)))
    server = serverLogin(host, user, password, port)
    if not server:
        print('Could Not Login To Server. Most Likely The Internet Is Down Locally Or Server Side.')
        input('Program Could Not Continue. Press Enter To Exit Program')
        exit()
    serverMods = getServerModsList(server)
    if not serverMods:
        print('Could Not Gather Server Mods. Most Likely The Internet Is Down Locally Or Server Side.')
        input('Program Could Not Continue. Press Enter To Exit Program')
        exit()
    print('Total Mods On Server: ' + str(len(serverMods)))
    okMods = []
    modsThatNeedInstalling = []
    modsThatNeedUninstalling = []
    for mod in serverMods:
        if mod in modsInstalled:
            okMods.append(mod)
        else:
            modsThatNeedInstalling.append(mod)
    for mod in modsInstalled:
        if mod not in serverMods:
            modsThatNeedUninstalling.append(mod)
    print('Total Mods That Need To Be Installed: ' + str(len(modsThatNeedInstalling)))
    print('Total Mods That Need To Be Uninstalled: ' + str(len(modsThatNeedUninstalling)))
    print('Total Mods That Match: ' + str(len(okMods)) +
          ' (' + str((len(okMods) * 100/len(serverMods))) + '%)')
    if modsThatNeedUninstalling:
        UninstallFiles(modsThatNeedUninstalling)
    if modsThatNeedInstalling:
        InstallFiles(server, modsThatNeedInstalling)
    server.quit()
    input('\nProgram Finished Successfully. Press Enter To Exit Or Just The Close Program.')
    exit()


def getLocalModsList(localDir):
    if not os.path.exists(localDir):
        return False, 'Path Does Not Exist.'
    else:
        if localDir.split('\\')[-1] != 'mods':
            localDir = localDir + '\\mods'
            if not os.path.exists(localDir):
                return False, 'Path Is Not Mods Folder Or Does Not Contain Mods Folder.'
        os.chdir(localDir)
        mods = os.listdir()

        return True, mods


def getServerModsList(server):
    try:
        server.cwd('mods')
        serverMods = []
        server.dir(serverMods.append)
        for i in range(len(serverMods)):
            serverMods[i] = serverMods[i][55:]
        return serverMods
    except Exception as e:
        print(e)
        return None


def serverLogin(host, user, password, port='21'):
    try:
        server = ftplib.FTP(host=host)
        server.login(user, password)
        return server
    except Exception as e:
        print(e)
        return None


def UninstallFiles(files, localDir=None):
    success = []
    print(f"Uninstalling {len(files)} Files...")
    for file in files:
        try:
            os.remove(file)
            print('Successfully Uninstalled ' + file)
            success.append(file)
        except Exception as e:
            print(e)
    print('Successful Removals: ' + str(len(success)) +
          ' (' + str((len(success) * 100 / len(files))) + '%)')


def InstallFiles(server, files, serverDir=None, localDir=None):
    success = []
    print(f"Installing {len(files)} Files...")
    for file in files:
        try:
            server.retrbinary("RETR " + file, open(file, 'wb').write)
            print('Successfully Installed ' + file)
            success.append(file)
        except Exception as e:
            print(e)
    print('Successful Transfers: ' + str(len(success)) +
          ' (' + str((len(success) * 100/len(files))) + '%)')


if __name__ == '__main__':
    main(Host, Username, Password, Port)
