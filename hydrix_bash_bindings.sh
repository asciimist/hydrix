#!/bin/bash
unset hyTime
unset hyGrep
unset hySessionClear
unset hyReverse
unset hystOff
unset hystOn
unset hydrix
unset hyAll
unset hyWidth
unset hyLines
unset hyEllipsis
unset hyRoot_no_h
unset hyRoot
unset hyCut
unset hyBud
unset hyBlossom
unset hyName
unset hunload
unset h_filter_pwd
unset hyff
unset hyLoadEntries
unset _hyhead
unset hyHead
unset hyFocus
unset hySaveAllSessions
unset hyLoadAllSessions
unset hyClearCurrentSession
unset hyEdit
unset hyClipboardCopy
unset hdummy
unset get_icell_tree_args
unset echoprev
unset hyBlob
unset hycd
unset hySpawnFreshSessionNumber
unset hyCscope
unset hy_env


this_dir=$(dirname $(readlink -f ${BASH_SOURCE[0]}))
export _TTY_=$(/usr/bin/tty | gawk -F "/" '{print $4}');
export HY_TREE_NB=${_TTY_}
HISTFILE=~/.hydrix/history/history.${HY_TREE_NB}
HISTFILESIZE=4096
HISTSIZE=4096

source ~/.hydrix/SETTINGS

export HY_CLUSTER_TTY=0
export HY_ROOT=""
export HY_COMPACT=0
export HY_ELLIPSIS=1
export HY_SHIFT=0
export HY_TIME_FILTER=''
export HY_GREP=''
export HY_COLLAPSED=''
export HY_REVERSE=1
export HY_FREEZE=0
export HY_ON=true
export HY_ELLIPSIS=0
export HY_CD=''

touch ~/.hydrix/history/ttys_to_trees
[[ -z "${HY_LINES}" ]] && export HY_LINES=10
[[ -z "${HY_FOCUS}" ]] && export HY_FOCUS=-1
sed -i "$((${_TTY_}+1))s/.*/${_TTY_}/" ~/.hydrix/history/ttys_to_trees

function hySpawnFreshSessionNumber {
    touch ~/.hydrix/history/history.
    [[ ! -f ~/.hydrix/history/pwd.${1} ]] && touch ~/.hydrix/history/pwd.${1}
    [[ ! -f ~/.hydrix/history/cwd.${1} ]] && touch ~/.hydrix/history/cwd.${1}
    [[ ! -f ~/.hydrix/history/head.${1} ]] && touch ~/.hydrix/history/head.${1}
    [[ ! -f ~/.hydrix/history/root.${1} ]] && ( > ~/.hydrix/history/root.${1} )
    [[ ! -s ~/.hydrix/history/hywidth.${1} ]] && ( echo "-1" >~/.hydrix/history/hywidth.${1} )
}

hySpawnFreshSessionNumber ${HY_TREE_NB}

export HY_CSCOPE=0
function hyCscope { export HY_CSCOPE=1 ; }

function hyTime {
    if [ "$1" == "-h" ]; then
        echo "Set a permanent age filter to the entries of the current session.
This is a permanent version of optional the age filter in hydrix command.
The format is the same : [0-9]*[smhj]~[0-9]*[smhj].
Examples : hyTime 1j~ : sets minimum age to 1 day
           hyTime ~20h : sets maximum age to 20 hours
           hyTime 30s~40m : sets age from 30 seconds to 40 minutes.
If a unicode capable terminal is used, the icon '🕛' is used to remind the value of this filter.
The filter is suppressed by calling 'hyTime' without argument."
        return
    fi
    if [[ $# -eq 0 ]] ; then
        export HY_TIME_FILTER=''
    else
        export HY_TIME_FILTER=$1
    fi
}

function hyGrep {
    if [ "$1" == "-h" ]; then
        echo "Set a permanent pattern filter to the entries of the current session.
This is a permanent version of optional the pattern filter in hydrix command.
If the pattern contains a '/', then only file paths are looked for match. 
Otherwise, all history entries are looked for match
Examples : hyGrep /home : filter history tree branches on paths containing '/home'
           hyGrep ls : filter history entries containing the string 'ls'
If a unicode capable terminal is used, the icon '🔎' is used to remind the value of this filter.
The filter is suppressed by calling 'hyGrep' without argument."
        return
    fi
    if [[ $# -eq 0 ]] ; then
        export HY_GREP=''
    else
        export HY_GREP=$1
    fi
}

function hySessionsClear {
    if [ "$1" == "-h" ]; then
        echo ""
        return
    fi
    > ~/.hydrix/history/ttys_to_trees
    for i in $(seq 1 1000)
        do
        echo "" >> ~/.hydrix/history/ttys_to_trees
    done
}


function hyClearCurrentSession {
    if [ "$1" == "-h" ]; then
        echo "Clear all the history tree entries of the current session. 
This has no effect on the shell's own history system."
        return
    fi
    > ~/.hydrix/history/pwd.${HY_TREE_NB}
    > ~/.hydrix/history/cwd.${HY_TREE_NB}
    > ~/.hydrix/history/head.${HY_TREE_NB}
    > ~/.hydrix/history/history.${HY_TREE_NB}
    > ~/.hydrix/history/pwd_filtered.${HY_TREE_NB}
    ( echo "-1" > ~/.hydrix/history/hywidth.${HY_TREE_NB} )
    > ~/.hydrix/history/root.${HY_TREE_NB}
}

function hyCompact {
    if [ "$1" == "-h" ]; then
        echo ""
        return
    fi
    if [[ $# -eq 0 ]] ; then
        export HY_COMPACT=0
    else
        export HY_COMPACT=$1
    fi
}



function hyShift {
    if [ "$1" == "-h" ]; then
        echo "When displaying a tree exceed the terminal's width (COL), 'hyShift' allows to display it from the right end.
        Examples :
        hshift -1 : display tree from the right end
        hshift 0 : display tree from the left end
        hshift n : display tree from the left shifted by n*COL cells
        hshift -n : display tree from the right shifted by n*COL cells
        etc ...
        "
        return
    fi
    if [[ $# -eq 0 ]] ; then
        export HY_SHIFT=0
    else
        export HY_SHIFT=$1
    fi
    hydrix
}


function hyArchiveCurrentSession {
    if [ "$1" == "-h" ]; then
        echo "Archive current session in ~/.hydrix/history/ with a datestamp."
        return
    fi
    datestamp=$(date +"s%W-%a%H:%M:%S")
    cp ~/.hydrix/history/pwd.${HY_TREE_NB}   ~/.hydrix/history/pwd.${HY_TREE_NB}_${datestamp}
    cp ~/.hydrix/history/cwd.${HY_TREE_NB}   ~/.hydrix/history/cwd.${HY_TREE_NB}_${datestamp}
    cp ~/.hydrix/history/head.${HY_TREE_NB}  ~/.hydrix/history/head.${HY_TREE_NB}_${datestamp}
    cp ~/.hydrix/history/hywidth.${HY_TREE_NB}  ~/.hydrix/history/hywidth.${HY_TREE_NB}_${datestamp}
    cp ~/.hydrix/history/root.${HY_TREE_NB}  ~/.hydrix/history/root.${HY_TREE_NB}_${datestamp}
    ls ~/.hydrix/history/*.${HY_TREE_NB}_${datestamp}
}


function hyChange {
    if [ "$1" == "-h" ]; then
        echo "Change to the specified session number. Otherwise, when opening a new tty, the default attributed session number is the tty's number.
Called without argument, it displays a list of session names."
        return
    fi
    if [[ $# -eq 0 ]] ; then
        for i in $(seq 1 99)
            do
            if [ -f ~/.hydrix/history/pwd.${i} ] ; then
                res=$(gawk 'NR==1&&$1~/#/{print $0}' ~/.hydrix/history/pwd.${i})
                echo "($i) ${res}"
            fi
        done
    elif [[ "$1" =~ ^[0-9]*$ ]] ; then
        export HY_TREE_NB=$1
        hySpawnFreshSessionNumber ${HY_TREE_NB}
        sed -i "$((${_TTY_}+1))s/.*/${HY_TREE_NB}/" ~/.hydrix/history/ttys_to_trees
        hyName
        hyHead
    else
        for i in $(seq 1 99)
            do
            if [ -f ~/.hydrix/history/pwd.${i} ] ; then
                res=$(gawk 'NR==1 && $1~/#/ {print $0}' ~/.hydrix/history/pwd.${i} | grep -i $1)
                [[ ! -z "${res}" ]] && break
            fi
        done
        export HY_TREE_NB=$i
        unset HISTFILE
        export HISTFILE=~/.hydrix/history/history.${HY_TREE_NB}
        sed -i "$((${_TTY_}+1))s/.*/${HY_TREE_NB}/" ~/.hydrix/history/ttys_to_trees
        hyName
        hyHead
    fi
}

function number_color_tty {
# declare -a colors=('209' '215' '178' '022' '023' '036' '059' '060' '065' '070' '075' '072')
declare -a colors=( '179,107,0' '38,115,77' '0,128,43' '115,77,38' '181,137,0' '0,41,102' '179,100,100' '0,150,150' '38,139,210' '133,53,0' )
if [[ ${HY_CLUSTER_TTY} -eq 0 ]]
then
    if [[ $# -lt 1 ]]
        then
        mod_TTY=$((${HY_TREE_NB}%${#colors[*]} ))
        mod_TTY=$((${HY_TREE_NB}%${#colors[*]} ))
    else
        mod_TTY=$((${1}%${#colors[*]} ))
    fi
    printf "${colors[mod_TTY]}"
else
    printf '179,107,0'
fi
}

export HY_ini_color_tty=$(number_color_tty)


function color_tty {
res=$(number_color_tty)
printf "\x1b[48;2;${HY_ini_color_tty//,/;}m ⎚ ${_TTY_}\x1b[48;2;${res//,/;}m ℋ${HY_TREE_NB} "
}


function hyReverse {
    if [ "$1" == "-h" ]; then
        echo "Revert the display order of the lines of tree."
        return
    fi
    if [[ ${HY_REVERSE} -eq 0 ]]
        then
        export HY_REVERSE=1
    else
        export HY_REVERSE=0
    fi
    echo HY_REVERSE=${HY_REVERSE}
}

function hyFreezeSwitch {
    if [ "$1" == "-h" ]; then
        echo "Switch on/off the freezing of cell numbers."
        return
    fi
    if [[ ${HY_FREEZE} -eq 0 ]]
        then
        export HY_FREEZE=1
    else
        export HY_FREEZE=0
    fi
    echo HY_FREEZE=${HY_FREEZE}
}

export HY_FREEZE=0

function hystOff {
    if [ "$1" == "-h" ]; then
        echo "Turn off history recording, including shell HISTFILE."
        return
    fi
    unset HISTFILE
    export HY_ON=false
    export PROMPT_COMMAND=""
}

function hystOn {
    if [ "$1" == "-h" ]; then
        echo "Turn on history recording, including shell HISTFILE."
        return
    fi
    export HISTFILE=~/.hydrix/history/history.${HY_TREE_NB}
    export HY_ON=true
    export PROMPT_COMMAND="echoprev"
}

hystOn ;

export HISTCONTROL=ignorespace:ignoredups #: Effective when bypassed by the "history -a" of echoprev ?

function echoprev {
    #this was adapted from: https://blog.dhampir.no/content/avoiding-invalid-commands-in-bash-history
    local exit_status=$?
    local number=$(history | tail -n 1 | gawk '{print $1}')
    number=${number%% *}
    if [[ ${HY_ON} == true && ${HY_CSCOPE} == 0 ]] ; then
        history -a  ~/.hydrix/history/history.${HY_TREE_NB}
        if [ -n "$number" ]; then
            if [ ${exit_status} -eq 0 ] ; then
                cmd=$(tail -n 1 ~/.hydrix/history/history.${HY_TREE_NB})
                i_h=$(wc -l ~/.hydrix/history/history.${HY_TREE_NB}| gawk '{print $1}')
                ppwd=$(pwd)
                prev_i_h=$(tail -n 1 ~/.hydrix/history/pwd.${HY_TREE_NB} | gawk '{print $1}')
                dt=$(date +"%s")
                [[ ! "${i_h}" =~ ^0$ ]] && [[ ! "${i_h}" =~ ^${prev_i_h}$ ]] && (echo "${i_h}-${dt} : $ppwd : $cmd" >> ~/.hydrix/history/pwd.${HY_TREE_NB})
            fi
        fi
    fi
}

# TEST : python ${hydrix_source}/hydrix.py $(/usr/bin/tty) $(cat ~/.hydrix/history/hywidth.${HY_TREE_NB}) $(number_color_tty) 1 0

function get_icell_tree_args {
    read -a args <<< "$@"
    icell=""
    tree_nb=${HY_TREE_NB}
    if [[ ${args[0]} =~ ^-c[0-9]*$ ]] ; then icell=${args[0]:2} ; unset args[0] ; fi
    if [[ ${args[0]} =~ ^-t[0-9]*$ ]] ; then tree_nb=${args[0]:2} ; unset args[0] ; fi
    if [[ ${args[1]} =~ ^-c[0-9]*$ ]] ; then icell=${args[1]:2} ; unset args[1] ; fi
    if [[ ${args[1]} =~ ^-t[0-9]*$ ]] ; then tree_nb=${args[1]:2} ; unset args[1] ; fi
    read -a args <<< "${args[@]}"
    if [ -z ${icell} ] ; then
        icell=$(gawk -v v=$(pwd) '$0==v{print NR}' ~/.hydrix/history/cwd.${tree_nb})
    fi
    export args
    export icell
    export tree_nb
}


function hydrix {
    if [ "$1" == "-h" ]; then
        echo "hydrix : displays the history tree of current session.
Can be combined with a pattern filter and an age filter.
Examples : hydrix
          hydrix 1j~ : filter entries and cells with minimum age 1 day
          hydrix ~20h : filter entries and cells maximum age 20 hours
          hydrix 30s~40m : filter with age from 30 seconds to 40 minutes
          hydrix /a_path : filter with history tree branches on paths containing \"/a_path\"
          hydrix a_string_in_an_entry : filter history entries containing the string \"a_string_in_an_entry\" in entries


EXPLANATION OF THE HYDRIX SYSTEM:
In hydrix you can navigate quickly through a history tree recorded in a \"session\".
A session may correspond to an on-going project or any typical use you will make of terminal if you will need to go through the same series of directories and invoke similar command lines.
The \"hydrix\" command display current session's tree.
Successfull commands (returning code 0) history are automatically recorded just as the shell's own history system.
The main difference with shell's usual history tools is that hydrix's history entries are organised according to the working directory where they were executed within a session.

One can move to a another recorded session calling \"hyChange N\" with its session number or its given name (done using the \"hyName\" command, \"hyChange\" displays the list all sessions names, \"hall\" displays all trees of all sessions).
Otherwise, by default, when opening a new tty (as done when opening a new tab in a virtual terminal manager) one opens the session corresponding to the tty's number.
Same sessions can be shared and modified on different ttys at the same time.


...┐    ┌────────────────────CELL────────────────────────────────────────────┐    ┌...
...│────│ /folder1/folder2                                                   │────│...
...│    │ [cellIndex] (oldestEntryAge~freshestEntryAge)  (numberOfEntries!)  │    │...
...│    │ EntryAge1:EntryIndex1 historyEntry1                                │    │...
...│    │ EntryAge2:EntryIndex2 historyEntry2                                │    │...
...┘    └────────────────────────────────────────────────────────────────────┘    └...
Fig. 1: Trees' cell format

                                  ┌───────────────────┐
                               ┌──│ BB/               │
                               │  │ [3] (2m~2m) (2!)  │
                               │  │2m:1 cmd1          │
                               │  └───────────────────┘
                               │                               ┌──────────────────┐
                               │                              ┌│/DD/              │
                               │                              ││ [1] (1s~1h) (2!) │
                               │                              ││1s:1 cmd1         │
                               │                              ││1h:2 cmd2         │
                               │                              │└──────sideCell────┘
                               │                              │
                               │                              │
┌───────────────────────────┐  │  ┌─────────────────┐     ┌───│───────────────┐
│ /A/                       │──┴──│ B/              │─────│ /C/D              │
│ [5] (4m~1h)  (3!)         │     │ [4] (3m~3m) (1!)│     │ [2] (1m~2h)  (2!) │
│4m:1 cmd1                  │     │3m:1 cmd1        │     │1m:1 cmd1          │
│1h:2 cmd2                  │     └─────────────────┘     │2h:2 cmd2          │
│1h:3 cmd3                  │                             └───────────────────┘
└───────────────────────────┘
Fig. 2: A tree for browsed paths \"/A\", \"/A/B\", \"/A/BB\", \"/A/B/C/D\" and \"/A/B/C/DD\".

An hydrix tree is made of branches wearing leaves (called cells).

Cells are small output block in which successfull history (\"history entries\") commands that were executed in the corresponding work directory are displayed.
If a \"TrueColors\" capable terminal (virtual terminal managers such as konsole, xterm, gnome-term and other libvte-based terms if libvte>0.36, see https://askubuntu.com/questions/512525/how-to-enable-24bit-true-color-support-in-gnome-terminal) is used, the cells are colored according to a color gradient palette that goes from a fresh color (the color is associated with to the session's index) to dark grey.
Cells with the most recent entries get the freshest colors and those with the oldest entries get the darker ones. This helps focusing on your freshest inputs.

Entries displayed in cells have a basic syntax highlighting and they are numbered in given cells to ease their loading (see hyLoad). Entries' age in seconds (s), minutes (m), hours (h) or days (j) is displayed with the most relevant unit.
This age information is also colored to highlight which commands were executed around the same period. The two top lines of a cell contain the cell index \"[N]\" (just as cell colors gradient, cell indexes are crescent with the age of their last entry).

TREE SPAN MODIFICATION
Cell index \"[N]\" may be used to :
- navigate to associated working directory (\"hycd N\" is an alternative to \"cd path\")
- permanently suppress the cell and children cells (\"hyCut N\") and all their entries
- collapse the cells' children cells (\"hyBud N\")
- expand them back (\"hyBlossom N\")
- zoom on a part of the tree by starting on that cell (\"hyRoot N\")

The last line of the cell contains relative path associated to the cell.

The straight branch at the bottom of the output (or top depending on hyReverse command) is called the trunk.

If the shell's current working directory corresponds to a cell from current session, then the 'path line' is underlined and highlighted in sky blue.

FILTERING WITH PATTERNS
One may also apply age filters (time spent since command was entered), path filters and pattern to filter the entries.
These filters may only once upon display or they can be persistent (applying on all subsequent tree display, until the filter is suppressed).
The \"hyGrep\" and \"hyTime\" commands set persistent path/pattern filters and age filters respectively, while commands \"hydrix\" and \"hyAll\" can take simultaneously age filter arguments (with the \"x~y\", \"x~\" or \"~y\" syntax) and pattern arguments (\"x\" is a pattern for entries while any pattern containing \"/\" will be interpreted as a path search pattern).

Some cell display parameters may be changed through dedicated commands:
 - the number of displayed entry lines : hyLines
 - the cell's width in columns : hyWidth
 - to shorten the displayed length of cell's relative path : hyEllipsis
 - for trees with too many levels which exceeding the terminal's width, \"hyShiftView\" allows to visualize portions of the tree.
One may also \"zoom\" one cell only using \"hyFocus\" (or \"hyff\" to fully display long entry lines with line breaks).

The \"hystOn\" and \"hystOff\" turn on and off the history.

This is full list of hydrix commands (all of them have a \"-h\" for help string printing):
hyAll
hyArchiveCurrentSession
hyBlob
hyBlossom
hyBud
hycd
hyChange
hyClearCurrentSession
hyClipboardCopy
hyCompact
hyCut
hydrix
hyEdit
hyEllipsis
hyff
hyFocus
hyGrep
hyHead
hyLines
hyLoad
hyLoadAllSessions
hyName
hyReverse
hyRoot
hyRoot_no_h
hySaveAllSessions
hySessionsClear
hyShift
hystOff
hystOn
hyTime
hyWidth

"
        return
    fi
#     echoprev
    get_icell_tree_args $@
    force=1
    head_var=0
    python ${this_dir}/hydrix.py ${tree_nb} $(cat ~/.hydrix/history/hywidth.${tree_nb}) $(number_color_tty ${tree_nb}) ${force} ${head_var} ${args[@]} ;
    if [[ $# -eq 0 ]]
        then
        h_filter_pwd ;
    fi
} ;

function hyAll {
    if [ "$1" == "-h" ]; then
        echo "Display all session's history trees. Can be combined with a pattern filter and an age filter.
Examples : hyAll
          hyAll 1j~ : filter entries and cells with minimum age 1 day
          hyAll ~20h : filter entries and cells maximum age 20 hours
          hyAll 30s~40m : filter with age from 30 seconds to 40 minutes
          hyAll /a_path : filter with history tree branches on paths containing '/a_path'
          hyAll a_string_in_an_entry : filter history entries containing the string 'a_string_in_an_entry' in entries"
        return
    fi

    for i in $(ls -1 ~/.hydrix/history/history.* | gawk -F "." '{print $3}' | sort -g)
        do
        force=1
        head_var=0
        [[ -s ~/.hydrix/history/hywidth.${i} ]] && python ${this_dir}/hydrix.py "/dev/pts/${i}" $(cat ~/.hydrix/history/hywidth.${i}) "$(number_color_tty ${i})" ${force} ${head_var} $* ;
    done
}



function hyWidth {
    if [ "$1" == "-h" ]; then
        echo "Set current tree's cell width to the specified value. Value '0', set to the minimum width, value '-1' make a tentative 'best fit' to terminal width (experimental). "
        return
    fi
    if [[ $# -eq 0 ]] ; then
        echo "missing value"
        return
    fi
    echo "$1" >~/.hydrix/history/hywidth.${HY_TREE_NB} ;
    hydrix ;
}

function hyLines {
    if [ "$1" == "-h" ]; then
        echo "Sets the cell's number of history entry lines to the specified value."
        return
    fi
    export HY_LINES=$1 ;
    hydrix ;
}


function hyEllipsis {
    if [ "$1" == "-h" ]; then
        echo "When dealing with very long path associated to cells, this commands makes the displayed path shorter."
        return
    fi
    if [[ ${HY_ELLIPSIS} -eq 0 ]]
        then
        export HY_ELLIPSIS=1 ;
    else
        export HY_ELLIPSIS=0 ;
    fi
    hydrix ;
}

function hyRoot_no_h {
    echo "${1}" >~/.hydrix/history/root.${HY_TREE_NB} ;
}

function hyRoot {
    if [ "$1" == "-h" ]; then
        echo 'Set session '"'"'s tree root path: tree branches not starting with this setting will not be displayed.
Note: Calling without argument resets this permanent filter.
Examples: hyRoot /a_given/path : the root path will be set to /a_given/path
          hyRoot . : the root path will always be set to the current working directy
          hyRoot $(pwd) : the root path will be set to the working directy at the execution
'
        return
    fi
    hyRoot_no_h ${1} ;
    hydrix ;
}


function hhroot {
    if [[ $i =~ ^pwd+ ]] ; then
        export HY_ROOT=$(pwd)
    else
        export HY_ROOT=$1
    fi
    hydrix ;
}


function hyCut {
    if [ "$1" == "-h" ]; then
        echo "hyCut N : Permanently suppress branch starting from cell N and all depending branches. Accepts multiple arguments."
        return
    fi
    if [[ $# -eq 0 ]] ; then
        echo "number missing"
    else
        for i in $@
        do
            target="$(gawk -v v=$i 'NR==v{print $0}' ~/.hydrix/history/cwd.${HY_TREE_NB})"
            cp ~/.hydrix/history/pwd.${HY_TREE_NB} ~/.hydrix/history/pwd.${HY_TREE_NB}~
            echo "SUPPRESSING ${target}"
            gawk -v v="${target}" -F' : ' '$2 !~ ("^" v "$"){print $0}' ~/.hydrix/history/pwd.${HY_TREE_NB} > ~/.hydrix/history/~pwd.${HY_TREE_NB}~
            mv  ~/.hydrix/history/~pwd.${HY_TREE_NB}~ ~/.hydrix/history/pwd.${HY_TREE_NB}
        done
    fi
}


function hyBud {
    if [ "$1" == "-h" ]; then
        echo "Hides all child branches of branches number N. Accepts multiple arguments. (opposite of hyBlossom)"
        return
    fi
    if [[ $# -eq 0 ]] ; then
        echo "number missing"
    else
        for i in $@
        do
            if [[ $i =~ ^[0-9]+ ]]
                then
                end=""
                [[ $i =~ .*/\.\.$ ]] && i=${i:0:$#-4} && end="/.."
                target="$(gawk -v v=$i 'NR==v{print $0}' ~/.hydrix/history/cwd.${HY_TREE_NB})""${end}"
                echo "HIDDING ${target}"
                export HY_COLLAPSED=${HY_COLLAPSED}:${target}
            else
                export HY_COLLAPSED=${HY_COLLAPSED}:${i}
            fi
        done
    fi
}

function hyBlossom {
    if [ "$1" == "-h" ]; then
        echo "Shown all child branches of branches number N. Accepts multiple arguments. (opposite of HyBud)"
        return
    fi
    if [[ $# -eq 0 ]] ; then
        echo "number missing"
    else
        for i in $@
        do
            target="$(gawk -v v=$i 'NR==v{print $0}' ~/.hydrix/history/cwd.${HY_TREE_NB})"
            echo "SHOWING ${target}"
            export HY_COLLAPSED=$(python -c "rr='${HY_COLLAPSED}' ; rr=rr.split(':') ; print ':'.join([ e for e in rr if e!='$target']) ")
        done
    fi
}

function hyName {
    if [ "$1" == "-h" ]; then
        echo "Sets a name for current session. Called without arguments it sets the session name to the tab (should work at least for Konsole)."
        return
    fi
    if [[ $# -eq 0 ]] ; then
        export htitle=$(gawk 'NR==1&&$1~/#/{print $0}' ~/.hydrix/history/pwd.${HY_TREE_NB})
        echo -ne "\033]30;${HY_TREE_NB}$htitle\007"
    else
        if [[ -z "$(gawk 'NR==1&&/^#/{print $0}' ~/.hydrix/history/pwd.${HY_TREE_NB})" ]] ; then
            (echo "#$1" ; cat ~/.hydrix/history/pwd.${HY_TREE_NB} ) > ~/.hydrix/history/~pwd.${HY_TREE_NB}~
        else
            (echo "#$1" ; sed -n -e "2,$ p" ~/.hydrix/history/pwd.${HY_TREE_NB} ) > ~/.hydrix/history/~pwd.${HY_TREE_NB}~
        fi
        mv ~/.hydrix/history/~pwd.${HY_TREE_NB}~ ~/.hydrix/history/pwd.${HY_TREE_NB}
    fi
}

function hunload {
        if [ "$1" == "-h" ]; then
        echo ""
        return
    fi
    if [[ ${prev_hyload_stop} -ne 0 ]] ; then
        for il in $(seq 1 $((${nlines_loaded})) ) ;
            do
            echo "deleting :"$(sed -n "$(( ${prev_hyload_start_index} +1))p " ~/.hydrix/history/history.${HY_TREE_NB}) ; history -d $(( ${prev_hyload_start_index} + 1 )) ; history -w
        done
        echo "UNLOAD ${prev_hyload_start} ${prev_hyload_stop}"
        export prev_hyload_start=0
        export prev_hyload_stop=0
    fi
}


function h_filter_pwd {
    cell_path=$(gawk -v v=${icell} 'NR==v{print $0}' ~/.hydrix/history/cwd.${tree_nb})
    (tac ~/.hydrix/history/pwd_filtered.${tree_nb} | gawk -F ' : ' -v v="${cell_path}" '($1==v){print $2}') > ~/.hydrix/history/load.${tree_nb} ;
}

function hyFocus {
    if [ "$1" == "-h" ]; then
        echo "Displays only the entries of the cell N (or current cell if none specified). Similar to hyff but with syntax highlighting but no long lines handling ."
        return
    fi
    get_icell_tree_args $@
    export HROOT_PREV=$(cat ~/.hydrix/history/root.${tree_nb})
    hyRoot_no_h
    _hyhead -t${tree_nb} -c${icell}
    export HY_FOCUS=${hwd} ;
    export HY_LINES_OLD=${HY_LINES}
    export HY_LINES=$((${COLUMNS}-5))
    H_REV_prev=${HY_REVERSE}
    H_REVERSE=0
    echo 'hydrix ${@}='${@}
    hydrix ${@} ; #-> potential hgrep arguments
    export HY_REVERSE=${H_REV_prev}
    export HY_LINES=${HY_LINES_OLD}
    export HY_FOCUS=-1 ;
    hyRoot_no_h $(echo $HROOT_PREV)
}



function hyff {
    if [ "$1" == "-h" ]; then
        echo "Displays only the entries of the cell N (or current cell if none specified). Similar to hyFocus but without syntax highlighting and with long lines handling."
        return
    fi
    get_icell_tree_args $*
    OLDIFS=${IFS}
    IFS=$'\n'
    h_filter_pwd -t${tree_nb} -c${icell} ;
    i=$(($(wc -l ~/.hydrix/history/load.${tree_nb} | gawk '{print $1}')))
    for l in $(cat ~/.hydrix/history/load.${tree_nb}) ; do echo "$i : $l"; i=$((i-1)) ; echo ; done
    IFS=${OLDIFS}
}

function hyLoad {
    if [ "$1" == "-h" ]; then
        echo "hyLoad N1 N2
Loads entries from N1 to N2 of the current cell.
When called with a single argument, it load one entry.
When called without arguments, it load all the listed entries."
        return
    fi
    get_icell_tree_args $*
    if [[ ${#args[*]} -eq 0 ]] ; then
        hunload ;
        h_filter_pwd -t${tree_nb} -c${icell}  ;
        export prev_hyload_start=$(wc -l ~/.hydrix/history/history.${tree_nb}| gawk '{print $1}') ;
        export prev_hyload_start_index=$(($(history|tail -n 1 | gawk '{print $1}')))
        export nlines_loaded=$(wc -l ~/.hydrix/history/load.${tree_nb}| gawk '{print $1}')
        lines_start="1"
        lines_stop=$((${lines_start}+${nlines_loaded}))
    else
        h_filter_pwd -t${tree_nb} -c${icell} ;
        lines_start=$((${args[0]}))
        [[ ${#args[*]} -eq 1 ]] && lines_stop=$((${args[0]})) || lines_stop=$((${args[1]}))
        export nlines_loaded=$((${lines_stop}-${lines_start}+1)) ;
    fi
    if [[ ${HY_REVERSE} -eq 1 ]] ; then
        tac ~/.hydrix/history/load.${tree_nb} > ~/.hydrix/history/load.${tree_nb}_rev
        mv ~/.hydrix/history/load.${tree_nb}_rev ~/.hydrix/history/load.${tree_nb}
    fi
    cp ~/.hydrix/history/load.${tree_nb} ~/.hydrix/history/load.${tree_nb}.old
    ( gawk -v i="${lines_start}" -v j="${lines_stop}" 'NR>=i&&NR<=j {print $0}' ~/.hydrix/history/load.${tree_nb} ) > ~/.hydrix/history/load.${tree_nb}_tmp
    mv ~/.hydrix/history/load.${tree_nb}_tmp ~/.hydrix/history/load.${tree_nb}
    if [[ ${HY_REVERSE} -eq 1 ]] ; then
        tac ~/.hydrix/history/load.${tree_nb} > ~/.hydrix/history/load.${tree_nb}_rev
        mv ~/.hydrix/history/load.${tree_nb}_rev ~/.hydrix/history/load.${tree_nb}
    fi
    history -r ~/.hydrix/history/load.${tree_nb} ;
    history -a  ~/.hydrix/history/history.${tree_nb} ;
    export prev_hyload_stop=$((${prev_hyload_start}+${nlines_loaded})) ;
    echo "LOAD ${prev_hyload_start} ${prev_hyload_stop}" ;
    cat ~/.hydrix/history/load.${tree_nb}
}


function _hyhead {
    get_icell_tree_args $@
    [[ "${HY_DEBUG}" -eq 1 ]] && echo "@_hyhead icell=${icell}"
    [[ "${HY_DEBUG}" -eq 1 ]] && echo "@_hyhead tree_nb=${tree_nb}"
    if [ -z ${icell} ] ; then
        hwd=${PWD}
    else
        hwd=$(gawk -v v=${icell} 'NR==v{print $0}' ~/.hydrix/history/cwd.${tree_nb})
    fi
    [[ "${HY_DEBUG}" -eq 1 ]] && echo "@_hyhead ${hwd} >~/.hydrix/history/head.${tree_nb}"
    [[ "${HY_DEBUG}" -eq 1 ]] && echo ${hwd} >~/.hydrix/history/head.${tree_nb}
    export hwd
}


function hyHead {
    if [ "$1" == "-h" ]; then
        echo "Forces change of trunk to contain the current cell."
        return
    fi
    _hyhead $*
    hydrix ;
}

function hySaveAllSessions {
    if [ "$1" == "-h" ]; then
        echo "Stores the list of all the opened session. They can then be opened again with hyLoadAllSessions (currently Konsole only)."
        return
    fi
    > ~/.hydrix/history/hydrix_sessions_saved
    for i in $(seq 1 1000) ; do echo "" >> ~/.hydrix/history/hydrix_sessions_saved ; done
    for p in $(pgrep '^(k|c|ba|tc|z|)sh$')
        do
        a_tty=$( ps -o tname $p | sed -n 's|pts/\([0-9]*\)|\1|p')
        a_pid=$( ps -eaf $p | sed -n 's|pts/\([0-9]*\)|\1|p')
        tty_to_tree_index=$(gawk -v v=${a_tty} 'NR-1==v{print $1}' ~/.hydrix/history/ttys_to_trees)
        if [[ -n "${tty_to_tree_index}" && ${tty_to_tree_index} -ne ${a_tty} ]] ; then
            sed -i "$((${a_tty}+1))s/.*/${tty_to_tree_index} ${tty_to_dir_index}/" ~/.hydrix/history/hydrix_sessions_saved
        fi
        done
}

function hyLoadAllSessions {
    if [ "$1" == "-h" ]; then
        echo "Load all the sessions saved by hySaveAllSessions (Konsole only)."
        return
    fi
    [[ -f ~/bin/shrist_tabs_saved ]] && mv ~/bin/shrist_tabs_saved ~/.hydrix/history/hydrix_sessions_saved
    for t in $(cat ~/.hydrix/history/hydrix_sessions_saved)
        do
        echo "hch ${t}"
        [[ ! -s ~/.hydrix/history/hywidth.${t} ]] && echo "-1" > ~/.hydrix/history/hywidth.${t}
        ( cat ~/.bashrc ; echo " " ; echo "hch ${t} ; hyName ; hcd 1 ; echo 'sleep 1'" ; ) > ~/.hydrix/tmp_bashrc.sh
        [[ -n "${t}" ]] && ( konsole --new-tab -e /bin/bash --rcfile ~/.hydrix/tmp_bashrc.sh ; wait ; sleep 1 )
        #mate-terminal --tab-with-profile=Default -e  "/bin/bash --rcfile ~/.hydrix/tmp_bashrc.sh"
        rm ~/.hydrix/tmp_bashrc.sh
    done
}

function hyEdit {
    if [ "$1" == "-h" ]; then
        echo "Edit manually the list of entries from current session."
        return
    fi
    eval "${HY_EDITOR} ~/.hydrix/history/pwd.${HY_TREE_NB} 2>/dev/null"
}


function hyClipboardCopy  {
    if [ "$1" == "-h" ]; then
        echo "Copy to the path of cell selected by its number to clipboard (requires xclip). Pasting normally accessible through Ctrl+V or Ctrl+Maj+V"
        return
    fi
    HY_CD=$(gawk -v v=$1 'NR==v{print $0}' ~/.hydrix/history/cwd.${HY_TREE_NB})  ; echo '<<<'${HY_CD} ; echo -ne ${HY_CD} | xclip -i -selection clipboard ;
}


function hdummy  {
sleep 0
}

alias .h="hdummy"

function hyBlob  {
    if [[ $# -ne 2  || "$1" == "-h" ]]; then
        echo "hyBlob N1 N2 : Splits a cell (numbered N1) when it has a branch (numbered N2) in the middle of its path."
        return
    fi
    target1="$(gawk -v v=$1 'NR==v{print $0}' ~/.hydrix/history/cwd.${HY_TREE_NB})"
    target2="$(gawk -v v=$2 'NR==v{print $0}' ~/.hydrix/history/cwd.${HY_TREE_NB})"
    common=$(python -c "r1='${target1}' ; r2='${target2}'  ; import itertools as it ; print (''.join(el[0] for el in it.takewhile(lambda t: t[0] == t[1], zip(r1, r2)))).rstrip('/')  ") ;
    num1=$(($(tail -n 1 ~/.hydrix/history/pwd.${HY_TREE_NB} | gawk -F':' '{print $1}'| gawk -F'-' '{print $1}')+1))
    num2=$(($(tail -n 1 ~/.hydrix/history/pwd.${HY_TREE_NB} | gawk -F':' '{print $1}'| gawk -F'-' '{print $2}')+1))
    echo "${num1}-${num2} : ${common} : .h " >> ~/.hydrix/history/pwd.${HY_TREE_NB}
}



function hycd  {
    if [ "$1" == "-h" ]; then
        echo "hycd N : Perform a shell 'cd' to the path of cell numbered N. Note that cd1, cd2 ... cd20 are aliases of hycd 1, hycd 2 etc."
        return
    fi
    HY_CD=$(gawk -v v=$1 'NR==v{print $0}' ~/.hydrix/history/cwd.${HY_TREE_NB})  ; echo "'"${HY_CD}"'" ; [[ ${HY_CSCOPE} -eq 0 ]] && cd "${HY_CD//\\ / }" ;
    export HY_CD
    echo "HY_CD" ${HY_CD}
    hydrix
}


function hy_env  {
    echo _TTY_="${_TTY_}"
    echo HY_ON="${HY_ON}"
    echo HY_TREE_NB="${HY_TREE_NB}"
    echo HY_CLUSTER_TTY="${HY_CLUSTER_TTY}"
    echo HISTFILE="${HISTFILE}"
    echo HISTCONTROL="${HISTCONTROL}"
    echo HY_GHLANDER="${HY_GHLANDER}"
    echo HY_COMPACT="${HY_COMPACT}"
    echo HY_ELLIPSIS="${HY_ELLIPSIS}"
    echo HY_SHIFT="${HY_SHIFT}"
    echo HY_TIME_FILTER="${HY_TIME_FILTER}"
    echo HY_GREP="${HY_GREP}"
    echo HY_COLLAPSED="${HY_COLLAPSED}"
    echo HY_REVERSE="${HY_REVERSE}"
    echo HY_FREEZE="${HY_FREEZE}"
    echo HY_ELLIPSIS="${HY_ELLIPSIS}"
    echo HY_CD="${HY_CD}"
    echo HY_LINES="${HY_LINES}"
    echo HY_FOCUS="${HY_FOCUS}"
    echo HY_CSCOPE="${HY_CSCOPE}"
    echo HY_EDITOR="${HY_EDITOR}"
    echo HY_CONSOLE="${HY_CONSOLE}"
    echo HY_TRUE_COLORS="${HY_TRUE_COLORS}"
    echo HY_UNICODE="${HY_UNICODE}"
    echo HY_DEBUG="${HY_DEBUG}"
}

source ~/.hydrix/hydrix_bash_aliases.sh
