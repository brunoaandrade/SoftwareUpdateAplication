import os.path
from git import *
import xml.etree.ElementTree
import urllib2
from xml.dom import minidom
from confirmpopup import *

from kivy.logger import Logger

import logging

logging.Logger.manager.root = Logger
logging.basicConfig(filename="supdates.txt",
                    level=logging.INFO,
                    datefmt='%H:%M:%S',
                    filemode='w')
logger = logging.getLogger().getChild(__name__)

git_url = None
repository_dir = None
localVersion = None
userType = None
localTypeVersion = None
localBetaVersion = None
localAlphaVersion = None
closeToUpdate = None
updatesOn = None

# //////////// /////////////////////////////////////////        functions              ///////////////////////////////////////////////////////////////////////////////////////////
#                    main                                        Logical Implementation of update

#                    openSoftware():                             Open software- Runs Beeconnect

#                    readLocalXmlFile():                         Read Local XML File - Read data with user settings

#                    updateSoftware():                           Update Software - Compare local Version with Server Version

#                    update():                                   Update - Download last version from server get

#                    getserialRaspberryPI():                     serial RaspberryPI

#                    internet_on():                              Internet Connection - Check for internet connection

#                    replaceValueInXml(value, field):            Replace value in xml

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           Logical Implementation of update

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def main():
    logger.info("Starting software")
    runningFirstTime = True
    readLocalXmlFile()
    while str(runningFirstTime) == "True" or str(closeToUpdate) == "True":
        logger.info("Update variables-> runningFirstTime= " + str(runningFirstTime) + "  updatesOn= " + str(
            updatesOn) + "  closeToUpdate= " + str(closeToUpdate))
        if internet_on() and (updatesOn == "True" or updatesOn == "Auto" or closeToUpdate == "True"):
            updateSoftware()
        openSoftware()
        runningFirstTime = "False"


# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           Open software- Runs Beeconnect

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def openSoftware():
    os.chdir(repository_dir)
    os.system('python main')
    os.chdir('..')


# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           Read Local XML File - Read data with user settings

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def readLocalXmlFile():
    global git_url
    global repository_dir
    global localVersion
    global userType
    global localTypeVersion
    global localBetaVersion
    global closeToUpdate
    global updatesOn
    global localAlphaVersion
    logger.info("Reading Local XML File")
    # ////////////  read local XML file with Software Information  ////////////
    xmldoc = minidom.parse('localInformation.xml')
    itemlist = xmldoc.getElementsByTagName('version')
    localVersion = itemlist[0].attributes['value'].value
    itemlist = xmldoc.getElementsByTagName('type')
    localTypeVersion = itemlist[0].attributes['value'].value
    itemlist = xmldoc.getElementsByTagName('userType')
    userType = itemlist[0].attributes['value'].value
    itemlist = xmldoc.getElementsByTagName('betaVersion')
    localBetaVersion = itemlist[0].attributes['value'].value
    itemlist = xmldoc.getElementsByTagName('updatesOn')
    updatesOn = itemlist[0].attributes['value'].value
    itemlist = xmldoc.getElementsByTagName('closeToUpdate')
    closeToUpdate = itemlist[0].attributes['value'].value
    itemlist = xmldoc.getElementsByTagName('gitURL')
    git_url = itemlist[0].attributes['value'].value
    itemlist = xmldoc.getElementsByTagName('repositoryDir')
    repository_dir = itemlist[0].attributes['value'].value
    itemlist = xmldoc.getElementsByTagName('alphaVersion')
    localAlphaVersion = itemlist[0].attributes['value'].value
    return


# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           Update Software - Compare local Version with Server Version

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def updateSoftware():
    # ////////////  get software beeconect if it is not installed  ////////////
    if not os.path.exists(repository_dir):
        os.makedirs(repository_dir)
        os.chdir(repository_dir)
        Repo.clone_from(git_url, repository_dir)
        os.chdir('..')
    # ////////////  read beeverycreative XML file with Last Software Information  ////////////
    file = urllib2.urlopen('https://www.beeverycreative.com/public/software/BEESOFT/updates_beeConect.xml')
    file1 = open('updates_beeConect.xml', 'w+')
    file1.write(file.read())  # python will convert \n to os.linesep
    file1.close()
    file.close()

    # ////////////  read beeverycreative XML file with Last Software Information  ////////////
    e = xml.etree.ElementTree.parse('updates_beeConect.xml')
    print "read xml file"

    iterator = e.iter()
    for node in iterator:
        if (str(node.tag) == 'Version_alpha'):
            beeConnect_last_version_alpha = str(node.attrib.get('value'))
        elif (str(node.tag) == 'VersionBeta_alpha'):
            beeConnect_last_versionalpha_alpha = str(node.attrib.get('value'))
        elif (str(node.tag) == 'Log_alpha'):
            beeConnect_last_log_alpha = str(node.attrib.get('value'))
        elif (str(node.tag) == 'Version_beta'):
            beeConnect_last_version_beta = str(node.attrib.get('value'))
        elif (str(node.tag) == 'VersionBeta_beta'):
            beeConnect_last_versionbeta_beta = str(node.attrib.get('value'))
        elif (str(node.tag) == 'Log_beta'):
            beeConnect_last_log_beta = str(node.attrib.get('value'))
        elif (str(node.tag) == 'Version_stable'):
            beeConnect_last_version = str(node.attrib.get('value'))
        elif (str(node.tag) == 'Log_stable'):
            beeConnect_last_log = str(node.attrib.get('value'))

    local_version_split = localVersion.split(".")
    beeConnect_last_version_split = beeConnect_last_version.split(".")
    beeConnect_last_version_beta_split = beeConnect_last_version_beta.split(".")
    beeConnect_last_version_alpha_split = beeConnect_last_version_alpha.split(".")

    # check if the application is using beta software alpha or stable
    # 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0.

    if userType == "stable":
        if (beeConnect_last_version_split[0] > local_version_split[0]):
            update("stable", beeConnect_last_version, "0",beeConnect_last_log)
        elif beeConnect_last_version_split[0] == local_version_split[0] and beeConnect_last_version_split[1] > \
                local_version_split[1]:
            update("stable", beeConnect_last_version, "0",beeConnect_last_log)
        elif beeConnect_last_version_split[0] == local_version_split[0] and beeConnect_last_version_split[1] == \
                local_version_split[1] \
                and beeConnect_last_version_split[2] > local_version_split[2]:
            update("stable", beeConnect_last_version, "0",beeConnect_last_log)

    elif userType == "beta":
        # check what version is more recent: beta or stable
        # if beta is more recent that stable
        # compare date beta with date stable on Server
        if (beeConnect_last_version_beta_split[2] > beeConnect_last_version_split[2]) or \
                (beeConnect_last_version_beta_split[2] == beeConnect_last_version_split[2] and
                         beeConnect_last_version_beta_split[1] > beeConnect_last_version_split[1]) or \
                (beeConnect_last_version_beta_split[2] == beeConnect_last_version_split[2] and
                         beeConnect_last_version_beta_split[1] == beeConnect_last_version_split[1] and
                         beeConnect_last_version_beta_split[0] > beeConnect_last_version_split[0]):
            # check if  version is more recent than local version
            if (beeConnect_last_version_beta_split[0] > local_version_split[0]):
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )
            elif beeConnect_last_version_beta_split[0] == local_version_split[0] and beeConnect_last_version_beta_split[
                1] > local_version_split[1]:
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )
            elif beeConnect_last_version_beta_split[0] == local_version_split[0] and beeConnect_last_version_beta_split[
                1] == local_version_split[1] \
                    and beeConnect_last_version_beta_split[2] > local_version_split[2]:
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )
            # check beta_version with local beta_version
            elif beeConnect_last_version_beta_split[0] == local_version_split[0] and beeConnect_last_version_beta_split[
                1] == local_version_split[1] \
                    and beeConnect_last_version_beta_split[2] == local_version_split[
                        2] and beeConnect_last_versionbeta_beta > localBetaVersion:
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )
        # if stable is more recent that beta
        else:
            beeConnect_last_version = beeConnect_last_version.split(".")
            if (beeConnect_last_version[0] > local_version_split[0]):
                update("stable", beeConnect_last_version, "0",beeConnect_last_log)
            elif beeConnect_last_version[0] == local_version_split[0] and beeConnect_last_version[1] > \
                    local_version_split[1]:
                update("stable", beeConnect_last_version, "0",beeConnect_last_log)
            elif beeConnect_last_version[0] == local_version_split[0] and beeConnect_last_version[1] == \
                    local_version_split[1] \
                    and beeConnect_last_version[2] > local_version_split[2]:
                update("stable", beeConnect_last_version, "0",beeConnect_last_log)
            # if same version on device as in server, ann the user have beta and in the server we have stable
            elif beeConnect_last_version[0] == local_version_split[0] and beeConnect_last_version[1] == \
                    local_version_split[1] \
                    and beeConnect_last_version[2] == local_version_split[2] and localTypeVersion == "beta":
                update("stable", beeConnect_last_version, "0",beeConnect_last_log)

    elif userType == "alpha":
        # check what version is more recent: beta or stable or alpha
        # if alpha is more recent that beta
        # if beta is more recent that stable
        # compare alpha with beta on Server
        if (beeConnect_last_version_alpha_split[2] > beeConnect_last_version_beta_split[2]) or \
                (beeConnect_last_version_alpha_split[2] == beeConnect_last_version_beta_split[2] and
                         beeConnect_last_version_alpha_split[1] > beeConnect_last_version_beta_split[1]) or \
                (beeConnect_last_version_alpha_split[2] == beeConnect_last_version_beta_split[2] and
                         beeConnect_last_version_alpha_split[1] == beeConnect_last_version_beta_split[1] and
                         beeConnect_last_version_alpha_split[0] > beeConnect_last_version_beta_split[0]):
            # check if alpha version is more recent than local version
            if (beeConnect_last_version_alpha_split[0] > local_version_split[0]):
                update("alpha", beeConnect_last_version_alpha, beeConnect_last_versionalpha_alpha,beeConnect_last_log_alpha)
            elif beeConnect_last_version_alpha_split[0] == local_version_split[0] and \
                            beeConnect_last_version_alpha_split[1] > local_version_split[1]:
                update("alpha", beeConnect_last_version_alpha, beeConnect_last_versionalpha_alpha,beeConnect_last_log_alpha)
            elif beeConnect_last_version_alpha_split[0] == local_version_split[0] and \
                            beeConnect_last_version_alpha_split[1] == local_version_split[1] \
                    and beeConnect_last_version_alpha_split[2] > local_version_split[2]:
                update("alpha", beeConnect_last_version_alpha, beeConnect_last_versionalpha_alpha,beeConnect_last_log_alpha)
            # check beta_version with local beta_version
            elif beeConnect_last_version_alpha_split[0] == local_version_split[0] and \
                            beeConnect_last_version_alpha_split[1] == local_version_split[1] \
                    and beeConnect_last_version_alpha_split[2] == local_version_split[
                        2] and beeConnect_last_versionalpha_alpha > localAlphaVersion:
                update("alpha", beeConnect_last_version_alpha, beeConnect_last_versionalpha_alpha,beeConnect_last_log_alpha)

        # check what version is more recent: beta or stable
        # if beta is more recent that stable
        # compare version beta with version stable on Server
        elif (beeConnect_last_version_beta_split[2] > beeConnect_last_version_split[2]) or \
                (beeConnect_last_version_beta_split[2] == beeConnect_last_version_split[2] and
                         beeConnect_last_version_beta_split[1] > beeConnect_last_version_split[1]) or \
                (beeConnect_last_version_beta_split[2] == beeConnect_last_version_split[2] and
                         beeConnect_last_version_beta_split[1] == beeConnect_last_version_split[1] and
                         beeConnect_last_version_beta_split[0] > beeConnect_last_version_split[0]):
            # check if  version is more recent than local version
            if (beeConnect_last_version_beta_split[0] > local_version_split[0]):
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )
            elif beeConnect_last_version_beta_split[0] == local_version_split[0] and beeConnect_last_version_beta_split[
                1] > local_version_split[1]:
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )
            elif beeConnect_last_version_beta_split[0] == local_version_split[0] and \
                            beeConnect_last_version_beta_split[1] == local_version_split[1] and \
                            beeConnect_last_version_beta_split[2] > local_version_split[2]:
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )
            # check beta_version with local beta_version
            elif beeConnect_last_version_beta_split[0] == local_version_split[0] and beeConnect_last_version_beta_split[
                1] == local_version_split[1] \
                    and beeConnect_last_version_beta_split[2] == local_version_split[
                        2] and beeConnect_last_versionbeta_beta > localBetaVersion:
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )
            elif beeConnect_last_version_beta_split[0] == local_version_split[0] and beeConnect_last_version_beta_split[
                1] == local_version_split[1] \
                    and beeConnect_last_version_beta_split[2] == local_version_split[2] and (
                        localTypeVersion == "alpha"):
                update("beta", beeConnect_last_version_beta, beeConnect_last_versionbeta_beta,beeConnect_last_log_beta )

        # if stable is more recent that beta
        else:
            if (beeConnect_last_version[0] > local_version_split[0]):
                update("stable", beeConnect_last_version, "0",beeConnect_last_log)
            elif beeConnect_last_version[0] == local_version_split[0] and beeConnect_last_version[1] > \
                    local_version_split[1]:
                update("stable", beeConnect_last_version, "0",beeConnect_last_log)
            elif beeConnect_last_version[0] == local_version_split[0] and beeConnect_last_version[1] == \
                    local_version_split[1] \
                    and beeConnect_last_version[2] > local_version_split[2]:
                update("stable", beeConnect_last_version, "0",beeConnect_last_log)
            # if same version on device as in server, ann the user have beta and in the server we have stable
            elif beeConnect_last_version[0] == local_version_split[0] and beeConnect_last_version[1] == \
                    local_version_split[1] \
                    and beeConnect_last_version[2] == local_version_split[2] and (
                            localTypeVersion == "beta" or localTypeVersion == "alpha"):
                update("stable", beeConnect_last_version, "0",beeConnect_last_log)


# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           Update - Download last version from server

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def update(beta_or_stable_or_alpha, version, betaAlphaVersion,updateInformation):
    global updatesOn
    isUpdate = False
    if (updatesOn == "True" and closeToUpdate == "False"):
        # ask the user
        popup = PopupTest()
        popup.set_updateInformation(updateInformation,version,betaAlphaVersion,beta_or_stable_or_alpha)
        popup.run()
        isUpdate = popup.get_update()
    elif updatesOn == 'Auto' or closeToUpdate == "True":
        isUpdate = True

    logger.info("Update = " + str(isUpdate))
    # if the user says ok
    if isUpdate:
        global localTypeVersion
        global localBetaVersion
        global localAlphaVersion
        global localVersion

        replaceValueInXml(str(version), 'version')
        localVersion = "stable"

        os.chdir(repository_dir)
        os.system('git pull')
        os.chdir('..')

        if (beta_or_stable_or_alpha == "stable"):
            os.chdir(repository_dir)
            os.system('git checkout beeconnect_' + version)
            os.chdir('..')
            replaceValueInXml('stable', 'type')
            replaceValueInXml('0', 'betaVersion')
            replaceValueInXml('0', 'alphaVersion')
            localTypeVersion = "stable"
            localBetaVersion = "0"
            localAlphaVersion = "0"

        elif (beta_or_stable_or_alpha == "beta"):
            os.chdir(repository_dir)
            print('git checkout beeconnect_' + version + "_beta_" + betaAlphaVersion)
            os.system('git checkout beeconnect_' + version + "_beta_" + betaAlphaVersion)
            os.chdir('..')
            replaceValueInXml('beta', 'type')
            replaceValueInXml(str(betaAlphaVersion), 'betaVersion')
            replaceValueInXml('0', 'alphaVersion')
            localTypeVersion = "beta"
            localBetaVersion = str(betaAlphaVersion)
            localAlphaVersion = "0"
        else:
            os.chdir(repository_dir)
            print('git checkout beeconnect_' + version + "_alpha_" + betaAlphaVersion)
            os.system('git checkout beeconnect_' + version + "_alpha_" + betaAlphaVersion)
            os.chdir('..')
            replaceValueInXml('alpha', 'type')
            replaceValueInXml(str(betaAlphaVersion), 'alphaVersion')
            replaceValueInXml('0', 'betaVersion')
            localTypeVersion = "alpha"
            localBetaVersion = "0"
            localAlphaVersion = str(betaAlphaVersion)


# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           Replace value in xml

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def replaceValueInXml(value, field):
    xmldoc = minidom.parse('localInformation.xml')
    firstchild = xmldoc.getElementsByTagName(field)[0]
    firstchild.attributes["value"].value = value
    print xmldoc.getElementsByTagName(field)[0].attributes["value"].value

    file_handle = open("localInformation.xml", "wb")
    xmldoc.writexml(file_handle)
    file_handle.close()

    return


# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           Internet Connection - Check for internet connection

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           get serial RaspberryPI

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def getserialRaspberryPI():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial
# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#                           Main

# //////////// ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    main()

