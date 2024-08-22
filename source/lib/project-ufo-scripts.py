from mojo.subscriber import Subscriber
from mojo.subscriber import registerCurrentFontSubscriber
from mojo.UI import MenuBuilder
from os import path
# from os import walk
import AppKit



script_folder_name = 'scripts'
script_menu_name = 'Project Scripts'



class project_ufo_scripts(Subscriber):

    debug = True

    def build(self):
        self.current_ufo_folder = ''
        self.project_menu_item = None

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
        self.menubar.removeItem_(self.project_menu_item)

    def fontDocumentDidBecomeCurrent(self, info):
        if self.project_menu_item == None:
            self.add_menu()
        ufo = info['font']
        ufo_path = ufo.path
        self.clear_project_menu()
        if ufo_path == None:
            self.current_ufo_folder = None
            return
        folder_path, file_name = path.split(ufo_path)
        if folder_path == self.current_ufo_folder:
            return
        self.current_ufo_folder = folder_path
        script_folder = self.current_ufo_folder + '/' + script_folder_name
        if path.isdir(folder_path + '/' + script_folder_name):
            self.project_menu.addMenuFromPath(script_folder)
            # debug
            # for (dirpath, dirnames, filenames) in walk(script_folder):
            #     print(dirpath, dirnames, filenames)

    def fontDocumentDidClose(self, info):
        if len(AllFonts()) == 0 or CurrentFont() == None:
            self.clear_project_menu()

    def clear_project_menu(self):
        newItemArray = AppKit.NSMutableArray.alloc().init()
        blank = AppKit.NSArray.alloc().initWithArray_(newItemArray)
        self.project_menu_item.submenu().setItemArray_(blank)



registerCurrentFontSubscriber(project_ufo_scripts)



