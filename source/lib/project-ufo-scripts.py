from mojo.subscriber import Subscriber
from mojo.subscriber import registerCurrentFontSubscriber
from mojo.subscriber import unregisterCurrentFontSubscriber
from mojo.UI import MenuBuilder
from os import path
from os import walk
from mojo.tools import CallbackWrapper

import ezui
from pathlib import Path
from mojo.extensions import setExtensionDefault
from mojo.extensions import getExtensionDefault
from mojo.extensions import registerExtensionDefaults
from mojo.extensions import removeExtensionDefault
import AppKit



script_menu_name = 'Project Scripts'
prefKey = 'com.okay.projectscripts'



class project_ufo_scripts(Subscriber):

    debug = True

    def build(self):
        self.current_ufo_root = ''
        self.project_menu_item = None
        self.relative_folder_root = getExtensionDefault(prefKey+'.relative_folder_root')
        self.relative_folder_scripts = getExtensionDefault(prefKey+'.relative_folder_scripts')

    def started(self):
        self.menubar = AppKit.NSApp().mainMenu()
        i = self.menubar.indexOfItemWithTitle_('Window')
        if i < 0:
            self.add_menu()

    def add_menu(self):
        i = self.menubar.indexOfItemWithTitle_('Window')
        self.project_menu = MenuBuilder(
            menu='main',
            title=script_menu_name,
            insert=i,
            items=[('ufo local scripts', None)]
        )
        self.project_menu_item = self.menubar.itemWithTitle_(script_menu_name)

    def destroy(self):
        try:
            self.menubar.removeItem_(self.project_menu_item)
        except:
            return

    def fontDocumentDidBecomeCurrent(self, info):
        if self.project_menu_item == None:
            self.add_menu()
        ufo = info['font']
        ufo_path = ufo.path

        # self.p('clear_project_menu ufo_path', ufo_path)
        if ufo_path == None:
            self.clear_project_menu()
            self.add_preferences_menuitem()
            self.current_ufo_root = None
            return

        ufo_folder_path, ufo_file_name = path.split(ufo_path)
        # self.p('clear_project_menu folder_path', ufo_folder_path)

        relative_folder_root = ufo_folder_path + '/' + self.relative_folder_root
        relative_folder_scripts = ufo_folder_path + '/' + self.relative_folder_scripts
        absolute_folder_root = str(Path(relative_folder_root).resolve())
        absolute_folder_scripts = str(Path(relative_folder_scripts).resolve())
        # self.p('absolute_folder_root   ', absolute_folder_root)
        # self.p('absolute_folder_scripts', absolute_folder_scripts)

        if absolute_folder_root != self.current_ufo_root:
            self.current_ufo_root = absolute_folder_root
            self.clear_project_menu()
            if path.isdir(absolute_folder_scripts):
                self.project_menu.addMenuFromPath(absolute_folder_scripts)
                # for (dirpath, dirnames, filenames) in walk(absolute_folder_scripts):
                #     self.p(dirpath, dirnames, filenames)
            self.add_preferences_menuitem()

    def fontDocumentDidClose(self, info):
        if len(AllFonts()) == 0 or CurrentFont() == None:
            self.clear_project_menu()

    def clear_project_menu(self):
        newItemArray = AppKit.NSMutableArray.alloc().init()
        blank = AppKit.NSArray.alloc().initWithArray_(newItemArray)
        self.project_menu_item.submenu().setItemArray_(blank)

    def add_preferences_menuitem(self):
        menu = self.project_menu_item.submenu()
        i = len(menu.itemArray())
        menu.insertItem_atIndex_(AppKit.NSMenuItem.separatorItem(), i)
        self.target = CallbackWrapper(self.open_preferences)
        newItem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Project Scripts Preferences', 'action:', '')
        newItem.setTarget_(self.target)
        menu.insertItem_atIndex_(newItem, i+1)

    def open_preferences(self, sender):
        PreferencesController()

    def p(self, *args):
        if self.debug == True:
            s = 'debug project ufo scripts '
            for x in args:
                s += str(x) + ' '
            print(s)

registerCurrentFontSubscriber(project_ufo_scripts)





class PreferencesController(ezui.WindowController):

    def build(self):
        initialDefaults = {
            prefKey+'.relative_folder_root': '/',
            prefKey+'.relative_folder_scripts': '/scripts',
        }
        # for v, p in initialDefaults.items():
            # removeExtensionDefault(v)
        registerExtensionDefaults(initialDefaults)

        content = '''
        !!!!! Set Paths
        Set the relative path from a *.ufo to the project’s root folder.
        [_ _]                       @folder_root
        Set the relative path from a *.ufo to the project’s scripts folder.
        [_ _]                       @folder_scripts
        ---
        # !!!!! Select Menu Location
        # (X) Project Scripts       @menu_location
        # ( ) Scripts > Project
        # ---
        (Save Preferences)          @save
        '''
        self.w = ezui.EZWindow(
            title='Project Scripts Preferences',
            size=('auto'),
            content=content,
            controller=self
        )

    def started(self):
        # self.w.getItem('menu_location').enable(False)
        relative_folder_root = getExtensionDefault(prefKey+'.relative_folder_root')
        relative_folder_scripts = getExtensionDefault(prefKey+'.relative_folder_scripts')
        self.w.getItem('folder_root').set(relative_folder_root)
        self.w.getItem('folder_scripts').set(relative_folder_scripts)
        self.w.open()

    def saveCallback(self, sender):
        relative_folder_root = self.w.getItem('folder_root').get()
        relative_folder_scripts = self.w.getItem('folder_scripts').get()
        # save preferences
        setExtensionDefault(prefKey+'.relative_folder_root', relative_folder_root)
        setExtensionDefault(prefKey+'.relative_folder_scripts', relative_folder_scripts)
        # restart project-ufo-scripts
        unregisterCurrentFontSubscriber(project_ufo_scripts)
        registerCurrentFontSubscriber(project_ufo_scripts)
        # close
        self.w.close()

    # def menu_locationCallback(self, sender):
    #     return




