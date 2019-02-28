# -*- coding:UTF-8 -*-

import sys, os, time
import base64, hashlib

cwd = '/'.join(sys.argv[0].split('/')[:-1])
licensFolderPath = cwd+'/licensefiles'
SNFilePath = cwd+'/appscript/SN.dat'


def createLicense(licenseInfo):
    licensString = ''' License content'''
    licenseFileFolder ='/'.join([licensFolderPath, licenseInfo['device_code']])
    licenseFileName = '/'.join([licenseInfo['device_code']+'_%s.lic'%dateNow])
    licenseFilePath = '/'.join([licenseFileFolder, licenseInfo['device_code']+'_%s.lic'%dateNow])
    if not os.path.exists(licenseFileFddolder):
        os.makedirs(licenseFileFolder)
    with open(licenseFilePath, 'wb') as LFO:
        LFO.write(licensString.encode('utf-8'))
    return [licenseFilePath, licensString]
