import maya.cmds as cmds
import maya.mel as mel

dirPath = r''
fbxFiles = []


def sel_directory_files():
    '''Select a directory to batch fbx'''
    # var to write
    global fbxFiles
    global dirPath
    # Select folder
    Dir = cmds.fileDialog2(dir='path/to/dir', dialogStyle=2, fileMode=2)  # Select my directory
    print(dir)
    myString = Dir[0]
    myString = myString.replace("/", "\\")
    dirPath =  myString 
    print(dirPath)
    fbxFiles = cmds.getFileList(folder=dirPath, filespec='*.fbx')  # Get Fbx In directory

def deleteTranslateBones():
    '''Delete Translate bones'''
    bones = cmds.ls(type="joint", long=False)
    print(bones)

    # we are using mel but we can use Pymel
    # ---  EXEMPLE WITH PYMEL --------------------------
    # import pymel.core as pm
    # attr = pm.PyNode("CBHFBXASC045MANFBXASC045RightArm.translateZ")
    # attr.disconnect()

    for i in bones:
        cmds.select(i, r=True)
        # delete translation
        deleteConnection(str(i) + ".translateZ")
        deleteConnection(str(i) + ".translateX")
        deleteConnection(str(i) + ".translateY")


def deleteConnection(attr):
    print(attr)
    inputs = cmds.listConnections(attr, source=True, destination=False, plugs=True)
    if inputs:
        input = inputs[0]
        cmds.disconnectAttr(input, attr)


def processFbx():
    for i in fbxFiles:
        newscene()
        importFbx(dirPath + "\\" + i)
        deleteTranslateBones()
        exportFbx(dir + "\\" + i)
        print(dirPath + "\\" + i)

def newscene():
    cmds.file(f=True, new=True)


def importFbx(fullpath):
    cmds.file(fullpath, i=True, mergeNamespacesOnClash=True, namespace=':');


def exportFbx(fullpath):
    # set settings
    mel.eval('FBXExportFileVersion "FBX201000"')
    mel.eval('FBXExportInputConnections -v 0')
    # export selection
    myString = fullpath
    myString = myString.replace("\\", "\\\\")
    print(myString)
    myArg = r'file -force -options "fbx" -type "FBX export" -pr -ea ' + '"' + myString + '"'
    #print(myArg)
    mel.eval(myArg)  # remove -s to export all


if __name__ == '__main__':
    newscene()
    sel_directory_files()
    processFbx()
