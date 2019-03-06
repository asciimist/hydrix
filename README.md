<a href="https://imgflip.com/gif/2ve3rq"><img src="https://i.imgflip.com/2ve3rq.gif" title="made at imgflip.com"/></a>
# hydrix
A command line tool to record and display as a tree the command line history for given sessions/projects. The tree is built according the visited folders. It comes with many companion commands to focus on parts on the tree filtered by time of execution, pattern of commands, path ... It also allows to reload selected history command (pushing it on top of bash history stack, accessible with keyboard arrows).


  Description
Hydrix is a system of commands to display, filter and manipulate terminal history commands gathered into tree leaves ("cells") and branches grown according to the filesystem browsing history. The goal is to help fast selection and re-use of history commands related to a specific folder.
Can be combined with a pattern filter and an "age" (time spent since commands' first use)
see MANUAL file
filter.

    Configuration instructions
Basically there should be no depencies for most users: only python and bash are needed.
More specifically, python version 2.7 is requiered. The series hydrix commands use GNU bash, and they were tested on version 4.3 and some lower and higher versions.
A "TRUECOLORS" capable terminal (virtual terminal managers such as konsole, xterm-based terminals, gnome-term, mlterm and so many more) is advised. If you use a 256 colors ("8-bit") terminal, see operating instructions.
You must choose a MONOSPACED FONT (like most terminals should propose you as default), otherwise the display will mess up.
In principle it should work with any operating system providing the forementioned environment.
Pushing history items into hydrix storing files relies on both the PROMPT_COMMAND and HISTFILE bash variables mechanisms.
It was actually tested on several Linux distribution and MacOS with terminal application.

    Installation instructions
Installation requieres only very basic operations and can be done either manually or using the "install.sh" script : "cd hydrix ; bash install.sh". This script will just copy the source folder where you want and add one line to your "~/.bashrc" : "source ${hydrix_source}/hydrix_bash_bindings.sh", et voilà !

    Operating instructions
 After installation, some settings can be tuned from the ~/.hydrix/SETTINGS file. If you terminal is only 8-bit colors capable (256 colors) then you may switch HY_TRUE_COLORS to "256" :
"export HY_TRUE_COLORS=256". If your VTE is not even 256-capable then use "export HY_TRUE_COLORS=0" to only the 14 basic colors.  Same for terminal which are not unicode capables : you may switch to "export HY_UNICODE=0". The other settings of this file may only be useful to developers.
You may also customize :
- the commands you don't want to display in hydrix (typical "ls", "cd" ...) with the ~/.hydrix/IGNORED_COMMANDS file,
- paths you want to exclude: ~/.hydrix/IGNORED_paths file,
- the aliases to hydrix commands ~/.hydrix/hydrix_bash_aliases.sh

    File manifest (list of files included) 
AUTHORS
common.py
CustomOrderedDict.py
hydrix_bash_bindings.sh
hydrix.py
install.sh
LICENSE
MANUAL
README
default_settings/hydrix_bash_aliases.sh
default_settings/IGNORED_COMMANDS
default_settings/IGNORED_PATHS
default_settings/SETTINGS

    Copyright and licensing information
GNU General Public License v3.0, see LICENCE file

    Contact information for the distributor or programmer
https://github.com/asciimist/
    
    Known bugs
Could have limited functionalities when switching between folders with same names. 
    
    Troubleshooting
If sudden undesired behaviour, try to clean the last entries of the ~/.hydrix/history/pwd.${_TTY_}, where ${_TTY_} is your tty number (accessible via $(tty | awk -F '/' '{print $4}'))
    
    Credits and acknowledgments
Many thanks to BP and Benji for support and beta testing !
