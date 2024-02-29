# !/usr/bin/env python
# -*- coding: utf-8 -*-

#----------------------------------------------
#   ScriptName  : MSFbxExporter
#   Author      : Atsushi Hirata
#   Since       : 2023/12
#   Update      : None
#----------------------------------------------

import os
import maya.cmds as cmds
from maya.common.ui import LayoutManager
import maya.mel as mel

windowName = "MSFbxExporter"
window_width = 500
window_height = 250

current_path = '' 
seltboneList = [] 

rigName = "F4Ucorsair_RIG"
rigInSceneName = rigName + ":RIG"
timeRangeMin = 0
timeRangeMax = 180
#接頭語
sceneNum = "s01"
cutNum = "c01"
modelName = "F4U"
#総リグ数
allBone = []

#filepath取得
current_path = cmds.file(query=True, location=True)
current_dir = os.path.dirname(current_path)

def mainPrc(self):
    global selboneList
    #ボーンを選択
    sl_rig = rigName + ":F4U_base_jnt"
    cmds.select(sl_rig , r=True, hi=True)
    selboneList = cmds.ls( selection = True)
    #アニメーションのベイク
    bakeAnim(selboneList)
    #コントローラの削除
    #deleteCnt(selboneList)
    #FBXエクスポート
    exportFbx(selboneList)

def deleteCnt(selboneList):
    #ボーンを選択
    sl_cnt = rigName + ":CNT"
    cmds.select(sl_cnt , r=True, hi=True)
    delcntList = cmds.ls( selection = True)
    cmds.delete(delcntList)

def exportFbx(selboneList):
    global sceneNum
    global cutNum
    global modelName
    global rigName
    #textboxからの取得
    sceneNum = cmds.textField('sceneNumTx', q=True, text=True)
    cutNum = cmds.textField('cutNumTx', q=True, text=True)
    modelName = cmds.textField('modelNameTx', q=True, text=True)
    rigName = cmds.textField('rigNameTx', q=True, text=True)

    #ファイルパス
    saveFbxName = sceneNum + cutNum + "_" + modelName + ".fbx"
    save_dir = current_dir + "/" + sceneNum + cutNum
    save_path = current_dir + "/" + sceneNum + cutNum + "/" + saveFbxName

    #保存先ディレクトリの確認
    try:
        os.makedirs(save_dir)
    except FileExistsError:
        pass
    print("save " + save_dir)

    #上書き保存の確認
    if(os.path.exists(save_path) == True):
        print("上書き保存します")

    #ファイルの保存
    #cmds.file( save_path, exportSelected = True, type = 'FBX', options = "fbx", preserveReferences = True, force = True,  es=True)
    mel.eval(('FBXExport -f \"{}\" -s').format(save_path))

def bakeAnim(selboneList):
    cmds.select(selboneList)
    bakeframe = str(timeRangeMin) + ":" + str(timeRangeMax)
    cmds.bakeResults(sm=True, t=(0,180), sb= 1, oversamplingRate=1, dic=True, pok=True, sac=True, ral=False, bol=False, cp=False, s=True)

def bakeMode(self):
    global allBone
    allBone = cmds.textField('allBakeNum', q=True, text=True)
    for n in allBone:
        if (n == 0):
            cmds.select(rigName)
            cmds.bakeResults(sm=True, t=(0,180), sb= 1, oversamplingRate=1, dic=True, pok=True, sac=True, ral=False, bol=False, cp=False, s=True)
        else:
            bakerig = rigName + str(n)
            cmds.select(bakerig)
            cmds.bakeResults(sm=True, t=(0,180), sb= 1, oversamplingRate=1, dic=True, pok=True, sac=True, ral=False, bol=False, cp=False, s=True)

def GUI():
    global windowName
    global sceneNum
    global cutNum
    global modelName
    global rigName
    #既にGUIが存在する時に古いほうを消す処理
    if cmds.window(windowName, ex=1):
        cmds.deleteUI(windowName)

    cmds.window(windowName, title=windowName, rtf=True, w=window_width, h=window_height, mnb=False, mxb=False, s=True)
    #GUIを作成
    with LayoutManager(cmds.tabLayout(imw=1, imh=1)) as tabs:
        with LayoutManager(cmds.rowColumnLayout("SetFbxInfo" ,numberOfColumns=2, columnAttach=(1, 'right', 0), rowSpacing=[10,10], columnWidth=[(1, 100), (2, 250)] )) as columns:
            cmds.text( label='SceneNumber' )
            cmds.textField('sceneNumTx', tx="s01", ed=True)
            cmds.text( label='CutNumber' )
            cmds.textField('cutNumTx', tx="c01", ed=True)
            cmds.text( label='ModelName' )
            cmds.textField('modelNameTx', tx="F4U01", ed=True)
            cmds.text( label='RigName' )
            cmds.textField('rigNameTx', tx="F4Ucorsair_RIG", ed=True)
            cmds.text(label='example :')
            cmds.text(label=' F4Ucorsair_RIG')
            exportButton = cmds.button(l="FbxExport", w=window_width, h= 35, c=mainPrc, bgc=(0.5,0.5,1))
        with LayoutManager(cmds.rowColumnLayout("BakeMode" ,numberOfColumns=2, columnAttach=(1, 'right', 0), rowSpacing=[10,10], columnWidth=[(1, 100), (2, 250)] )) as columns:
            cmds.text( label='AllRig' )
            cmds.textField('allBakeNum', tx="1", ed=True)
            bakeButton = cmds.button(l="BakeAll", w=window_width, h= 35, c=bakeMode, bgc=(0.5,0.5,1))   
    cmds.showWindow(windowName)

def MSFbxExporter():
    GUI()

if __name__ == '__main__':  
    MSFbxExporter()
