#!/usr/bin/env python3
# coding=utf-8

# config
applications_dirs = ("/usr/share/applications", )
icon_Theme = ["/usr/share/icons/Papirus-Light/24x24/apps/",'/usr/share/icons/Papirus-Light/24x24/devices/','/usr/share/icons/Papirus-Light/24x24/actions/','/usr/share/icons/Papirus/22x22/apps/applications-']
alias = {"Audio":"Multimedia","AudioVideo":"Multimedia","Network":"Internet","Game":"Games", "Utility":"Utilities", "GTK":"",  "GNOME":""}
categories = {"Office":"办公",  "Development":"开发",  "Graphics":"图形", "Internet":"互联网",  "Games":"游戏", "System":"系统",  "Multimedia":"多媒体",  "Utilities":"实用工具",  "Settings":"设置"}
ignoreList = ("python3.11", "feh", "pcmanfm-desktop-pref", "org.xfce.mousepad-settings")
apps = (("终端", "terminal", "x-terminal-emulator"),("浏览器", "browser", "x-www-browser"),("文件", "system-file-manager", "pcmanfm"))
closes = (("锁屏", "system-lock-screen", "slock"),("挂起", "system-log-out", "systemctl -i suspend",),("休眼", "system-hibernate", "systemctl -i hibernate"),("重启", "system-reboot", "systemctl -i reboot"),("关机", "system-shutdown", "systemctl -i poweroff"))

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
    if data.find("/") == 0:
      self.Icon = data
    for icons in icon_Theme:
      temp = glob.glob(icons + data + ".*")
      if len(temp) > 0:
        self.Icon = temp[0]
        break

  def addCategories(self, data):
    self.Categories = data

def getCatIcon(cat):
  for icons in icon_Theme:
    temp = glob.glob(icons + cat.lower() + ".*")
    if len(temp) > 0:
      return temp[0]
      break

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
    if l[0]== '[' and l !=  "[Desktop Entry]":
      active = False
      continue
    eqi = l.split('=')
    if eqi[0] == "Name":
      this.addName(eqi[1])
    elif eqi[0] == "Name[zh_CN]":
      this.addName(eqi[1])
    elif eqi[0] == "Exec":
      this.addExec(eqi[1])
    elif eqi[0] == "Icon":
      this.addIcon(eqi[1])
    elif eqi[0] == "Categories":
      dtCats = eqi[1].split(';')[0:-1]
      this.addCategories(dtCats)
  if len(this.Categories) > 0:
    for cat in this.Categories:
      if cat in categories:
        if cat in alias:
          cat = alias[cat]
        if cat in catDict:
          catDict[cat].append(this)
        else:
          catDict[cat] = [this]

categoryDict = {}

if __name__ == "__main__":
  def makeItems(name, icon_Theme, icon, command):
    return "<item label=\"" + name +"\" icon=\"" + icon_Theme + icon + ".svg\"><action name=\"Execute\"><execute>" + command + "</execute></action></item>"
  def makeObItems(name, icon_Theme, icon, command):
    return "<item label=\"" + name +"\" icon=\"" + icon_Theme  + icon + ".svg\"><action name=\"" + command + "\" /></item>"

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

  print('<openbox_pipe_menu>')

  for app in apps:
    print(makeItems(app[0], icon_Theme[0], app[1], app[2]))
  print("<separator />")
  for key in categoryDict:
    if categoryDict[key] == []:
      continue
    if key in categories:
      catStr = "<menu id=\"openbox-%s\" label=\"%s\" " % (key, categories[key])
    else:
      catStr = "<menu id=\"openbox-%s\" label=\"%s\" " % (key, key)
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
  print(makeItems("配置OpenBox    ", icon_Theme[0], "preferences-theme", "obconf"))
  print(makeObItems("重置OpenBox", icon_Theme[0], "systemback", "Reconfigure"))
  print(makeObItems("重启OpenBox", icon_Theme[0], "system-reboot", "Restart"))
  print(makeObItems("退出OpenBox", icon_Theme[0], "system-shutdown", "Exit"))
  print("<separator />")
  for close in closes:
    print(makeItems(close[0], icon_Theme[0], close[1], close[2]))
  print("</openbox_pipe_menu>")