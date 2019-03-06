#!/bin/bash
this_dir=$(dirname $(readlink -f $0))
echo "Install path [Press enter for default path ~/bin/hydrix] ?"
read y
y="${y/#\~/$HOME}"
if [[ "${y}" =~ ^$ ]] ; then
    hydrix_source=~/bin/hydrix
    [[ -d ~/bin ]] || mkdir ~/bin
else
    hydrix_source=${y}/hydrix
    echo "hydrix_source ${hydrix_source}"
    [[ -d ${y}/ ]] || ( echo "${y} missing" ; exit )
fi
if [[ ! -d ${hydrix_source} ]] ; then
    cp -rf ${this_dir} ${hydrix_source}
else
    cp -rf ${this_dir}/* ${hydrix_source}/
fi
echo hydrix_source=${hydrix_source}

cp ~/.bashrc ~/.bashrc.BACK
if grep -q 'source .*/hydrix_bash_bindings.sh' ~/.bashrc ; then
    sed -i "s|source .*/hydrix_bash_bindings.sh|source ${hydrix_source}/hydrix_bash_bindings.sh|g" ~/.bashrc
    echo -ne "\033[34m[NOTE]\033[00m I modified the following line to your ~/.bashrc (backup before this modification is ~/.bashrc.BACK): \"source ${hydrix_source}/hydrix_bash_bindings.sh\"\n"
else
    (echo "" ; echo "source ${hydrix_source}/hydrix_bash_bindings.sh") >> ~/.bashrc
    echo "\033[34m[NOTE]\033[00m I added the following line to your ~/.bashrc (backup before this modification is ~/.bashrc.BACK): \"source ${hydrix_source}/hydrix_bash_bindings.sh\""
fi

[[ ! -d ~/.hydrix ]] && (mkdir ~/.hydrix && echo "Created: ~/.hydrix" )
[[ ! -d ~/.hydrix/history ]] && (mkdir ~/.hydrix/history && echo "Created: ~/.hydrix/history" )
for f in hydrix_bash_aliases.sh IGNORED_COMMANDS IGNORED_PATHS SETTINGS ; do
    if [[ -f ~/.hydrix/${f} ]] ; then
        echo "overwrite ~/.hydrix/${f} ? [default:n]/y"
        read y
        [[ "${y}" =~ ^y$ ]] && cp -v ${this_dir}/default_settings/${f} ~/.hydrix/
    else
        cp -v ${this_dir}/default_settings/${f} ~/.hydrix/
    fi
done
source ${hydrix_source}/hydrix_bash_bindings.sh
