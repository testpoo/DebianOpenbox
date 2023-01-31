#!/usr/bin/env python3
# coding=utf-8

# --- Start of user config ---
applications_dirs = ("/usr/share/applications", )
image_dir_base = "/usr/share/icons/"
icon_Theme = "Papirus-Light/24x24"
image_cat_prefix = "applications-"
application_groups = ("Office", "Development", "Graphics", "Internet", "Games", "System", "Multimedia", "Utilities", "Settings")
application_groups_zh = ("办公", "开发", "图形", "互联网", "游戏", "系统",  "多媒体", "实用工具", "设置")
group_aliases = {"Audio":"Multimedia","AudioVideo":"Multimedia","Network":"Internet","Game":"Games", "Utility":"Utilities", "GTK":"",  "GNOME":""}
ignoreList = ("python3.11", "feh", "pcmanfm-desktop-pref")
simpleOBheader = False
apps = (("终端", "terminal", "x-terminal-emulator"),("浏览器", "browser", "x-www-browser"),("文件", "system-file-manager", "pcmanfm"))
closes = (("锁屏", "system-lock-screen", "slock"),("挂起", "system-log-out", "systemctl -i suspend",),("休眼", "system-hibernate", "systemctl -i hibernate"),("重启", "system-reboot", "systemctl -i reboot"),("关机", "system-shutdown", "systemctl -i poweroff"))
# --- End of user config ---

import glob

class dtItem(object):
  def __init__(self, fName):
    self.Name = ""
    self.Exec = ""
    self.Icon = ""
    self.Categories = ()

  def addName(self, data):
    self.Name = data

  def addExec(self, data):
    if len(data) > 3 and data[-2] == '%':
      data = data[:-2].strip()
    self.Exec = data

  def addIcon(self, data):
    self.Icon = ""
    di = data.strip()
    dix = di.find("/")
    if dix == 0:
      self.Icon = di
      return
    temp_apps = glob.glob(image_dir_base + icon_Theme + "/apps/" + di + ".*")
    temp_devices = glob.glob(image_dir_base + icon_Theme + "/devices/" + di + ".*")
    if len(temp_apps) > 0:
      self.Icon = temp_apps[0]
    elif len(temp_devices) > 0:
      self.Icon = temp_devices[0]
    return

  def addCategories(self, data):
    self.Categories = data

def getCatIcon(cat):
  temp_apps = glob.glob(image_dir_base + icon_Theme + "/apps/" + image_cat_prefix + cat.lower() + ".*")
  temp_actions = glob.glob(image_dir_base + icon_Theme + "/actions/" + cat.lower() + ".*")
  if len(temp_apps) > 0:
    return temp_apps[0]
  elif len(temp_actions) > 0:
    return temp_actions[0]
  return ""

def process_category(cat, curCats,  appGroups = application_groups,  aliases = group_aliases ):
  if cat in aliases:
    if aliases[cat] == "":
      return ""
    cat = aliases[cat]
  if cat in appGroups and cat not in curCats:
    curCats.append(cat)
    return cat
  return ""

def process_dtfile(dtf,  catDict):
  active = False
  fh = open(dtf,  "r")
  lines = fh.readlines()
  this = dtItem(dtf)
  for l in lines:
    l = l.strip()
    if l == "[Desktop Entry]":
      active = True
      continue
    if active == False:
      continue
    if l == None or len(l) < 1 or l[0] == '#':
      continue
    if l[0] == '[' and l !=  "[Desktop Entry]":
      active = False
      continue
    eqi = l.split('=')
    if len(eqi) < 2:
      continue
    if eqi[0] == "Name[zh_CN]":
      this.addName(eqi[1])
    elif eqi[0] == "Name" and this.Name == "":
      this.addName(eqi[1])
    elif eqi[0] == "Exec":
      this.addExec(eqi[1])
    elif eqi[0] == "Icon":
      this.addIcon(eqi[1])
    elif eqi[0] == "Categories":
      if eqi[1] and eqi[1][-1] == ';':
        eqi[1] = eqi[1][0:-1]
      cats = []
      dtCats = eqi[1].split(';')
      for cat in dtCats:
        result = process_category(cat,  cats)
      this.addCategories(cats)
    else:
      continue
  if len(this.Categories) > 0:
    for cat in this.Categories:
      catDict[cat].append(this)

categoryDict = {}

if __name__ == "__main__":
  def makeItems(name, icon_Theme, icon, command, image_dir_base):
    return "<item label=\"" + name +"\" icon=\"" + image_dir_base + icon_Theme + "/apps/" + icon + ".svg\"><action name=\"Execute\"><execute>" + command + "</execute></action></item>"
  def makeObItems(name, icon_Theme, icon, command, image_dir_base):
    return "<item label=\"" + name +"\" icon=\"" + image_dir_base + icon_Theme + "/apps/" + icon + ".svg\"><action name=\"" + command + "\" /></item>"

  for appGroup in application_groups:
    categoryDict[appGroup] = []

  for appDir in applications_dirs:
    appDir += "/*.desktop"
    dtFiles = glob.glob(appDir)

    for dtf in dtFiles:
      skipFlag = False
      for ifn in ignoreList:
        if dtf.find(ifn) >= 0:
          skipFlag = True
      if skipFlag == False:
        process_dtfile(dtf,  categoryDict)

  if simpleOBheader == True:
    print('<openbox_pipe_menu>')
  else:
    print('<?xml version="1.0" encoding="UTF-8" ?><openbox_pipe_menu xmlns="http://openbox.org/"  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xsi:schemaLocation="http://openbox.org/" >')

  for app in apps:
    print(makeItems(app[0], icon_Theme, app[1], app[2], image_dir_base))
  print("<separator />")
  for key in categoryDict:
    if categoryDict[key] == []:
      continue
    catStr = "<menu id=\"openbox-%s\" label=\"%s\" " % (key, application_groups_zh[application_groups.index(key)])
    tmp = getCatIcon(key)
    catStr += "icon=\"%s\"" % tmp
    print(catStr,  ">")
    for app in categoryDict[key]:
      progStr = "<item "
      progStr += "label=\"%s\" "  % app.Name
      progStr += "icon=\"%s\" " % app.Icon
      progStr += "><action name=\"Execute\"><command><![CDATA["
      progStr += "%s]]></command></action></item>"  % app.Exec
      print(progStr)
    print("</menu>")
  print("<separator />")
  print(makeItems("配置OpenBox    ", icon_Theme, "preferences-theme", "obconf", image_dir_base))
  print(makeObItems("重置OpenBox", icon_Theme, "systemback", "Reconfigure", image_dir_base))
  print(makeObItems("重启OpenBox", icon_Theme, "system-reboot", "Restart", image_dir_base))
  print(makeObItems("退出OpenBox", icon_Theme, "system-shutdown", "Exit", image_dir_base))
  print("<separator />")
  for close in closes:
    print(makeItems(close[0], icon_Theme, close[1], close[2], image_dir_base))
  print("</openbox_pipe_menu>")