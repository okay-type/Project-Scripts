# Project Scripts

A [RoboFont] extension that adds a menu item with scripts from the current .ufo’s folder

To use:
- Open your project folder
- Create a folder named “scripts” next to your .ufos
- Fill that scripts folder with all your messy project-specific scripts
- The “Project Scripts” menu will automatically update when you open your .ufos
- Subfolders in your scripts folder will be put into submenus
- Supports Robofont's [menu title and keyboard shortcut] syntax

Preferences:
- You can edit the relative path to the project root and scripts folders. These paths are relative to the open .ufos, e.g.: '../production/scripts'


Requires for [RoboFont 4.0].

- - -

Questions and tasks that need to be done:
- Is there better a menu title than 'Project Scripts'?
- Are there any optimizations to make?
- Are there any events missing?
- Would this be better as a submenu in the regular Scripts folder?
    - eg: Scripts -> Project Folder Name -> [project scripts]

- - -

Version 1.0.2
- added preference ui
- added preferences to set relative paths for project root and script folders

Version 1.0.1
- fixed a bug with ufos in the same folder

Version 1.0.0
- initial release

jackson@[okaytype.com]


[okaytype.com]: https://okaytype.com
[RoboFont]: https://robofont.com
[RoboFont 4.0]: https://forum.robofont.com/topic/804/robofont-four
[Menu title and keyboard shortcut]: https://www.robofont.com/documentation/reference/workspace/scripting-window/?highlight=menuTitle#menu-title-and-keyboard-shortcut
