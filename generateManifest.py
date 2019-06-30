#coding:utf-8

import os
import sys
import json
import hashlib
import subprocess



# 改变当前工作目录 
#需要自己修改路径
os.chdir("D:/Develop/hotupdate/")


#需要自己修改路径
assetsDir = {
    #MyProj文件夹下需要进行热跟的文件夹
    "searchDir" : ["src", "res"],
    #需要忽略的文件夹
    "ignorDir" : ["cocos", "framework", ".svn"],
    #需要忽略的文件
    "ignorFile":[".DS_Store"],
}

#需要自己修改路径
versionConfigFile   = "version_info.json"  #版本信息的配置文件路径
versionManifestPath = "version/version.manifest"    #由此脚本生成的version.manifest文件路径
projectManifestPath = "version/project.manifest"    #由此脚本生成的project.manifest文件路径

class SearchFile:
    def __init__(self):
        self.fileList = []

        for k in assetsDir:
            if (k == "searchDir"):
                for searchdire in assetsDir[k]:                 
                    self.recursiveDir(searchdire)

    def recursiveDir(self, srcPath):
        ''' 递归指定目录下的所有文件'''
        dirList = []    #所有文件夹  

        files = os.listdir(srcPath) #返回指定目录下的所有文件，及目录（不含子目录）

        for f in files:         
            #目录的处理
            if (os.path.isdir(srcPath + '/' + f)):              
                if (f[0] == '.' or (f in assetsDir["ignorDir"])):
                    #排除隐藏文件夹和忽略的目录
                    pass
                else:
                    #添加非需要的文件夹                                  
                    dirList.append(f)

            #文件的处理
            elif (os.path.isfile(srcPath + '/' + f)) and (f not in assetsDir["ignorFile"]):               
                self.fileList.append(srcPath + '/' + f) #添加文件

        #遍历所有子目录,并递归
        for dire in dirList:        
            #递归目录下的文件
            self.recursiveDir(srcPath + '/' + dire)

    def getAllFile(self):
        ''' get all file path'''
        return tuple(self.fileList)


def CalcMD5(filepath):
    """generate a md5 code by a file path"""
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        return md5obj.hexdigest()


def getVersionInfo():
    '''get version config data'''
    configFile = open(versionConfigFile,"r")
    json_data = json.load(configFile)

    configFile.close()
    # json_data["version"] = json_data["version"] + '.' + str(GetSvnCurrentVersion())
    json_data["version"] = json_data["version"]
    return json_data


def GenerateVersionManifestFile():
    ''' 生成大版本的version.manifest'''
    json_str = json.dumps(getVersionInfo(), indent = 2)
    fo = open(versionManifestPath,"w")  
    fo.write(json_str)  
    fo.close()


def GenerateProjectManifestFile():
    searchfile = SearchFile()
    fileList = list(searchfile.getAllFile())
    project_str = {}
    project_str.update(getVersionInfo())
    dataDic = {}
    for f in fileList:      
        dataDic[f] = {"md5" : CalcMD5(f)}
        print f

    project_str.update({"assets":dataDic})
    json_str = json.dumps(project_str, sort_keys = True, indent = 2)

    fo = open(projectManifestPath,"w")  
    fo.write(json_str)  
    fo.close()

if __name__ == "__main__":
    GenerateVersionManifestFile()
    GenerateProjectManifestFile()