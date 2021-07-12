#!/bin/bash

declare -A osInfo;
osInfo[/etc/debian_version]="sudo apt-get install -y"
osInfo[/etc/alpine-release]="sudo apk --update add"
osInfo[/etc/centos-release]="sudo yum install -y"
osInfo[/etc/fedora-release]="sudo dnf install -y"
osInfo[/etc/manjaro-release]="sudo pamac install -y"

for f in ${!osInfo[@]}
do
    if [[ -f $f ]];then
        package_manager=${osInfo[$f]}
    fi
done

echo "Install some packages"

curl_inst=0
[ $(curl --version | grep -Eci 'release-date') = 0 ] && curl_inst=1
git_inst=0
[ $(git --version | grep -Eci 'release-date') = 0 ] && git_inst=1
venv_inst=0
[ $(git --version | grep -Eci 'from /usr') = 0 ] && venv_inst=1

if [ $curl_inst = 1 ]; then
    if [ -z $package_manager ]; then
        echo "unknown linux distro".
        echo "try installing curl with your package manager"
        echo "then run the installation command again"
        echo "exiting."
        exit
    fi
    [ curl_intst = 1 ] && $package_manager curl python3-pip-y
    [ git_intst = 1 ] && $package_manager python3-pip git -y
    [ venv_intst = 1 ] && $package_manager python3-pip virtualenv -y
fi

echo "Install docker"
echo


main_destination=/usr/local/bin/mir_phase3

echo
echo "Download repository"
echo

rm -rf $HOME/.local/share/mir_phase3
cd $HOME/.local/share
git clone --depth=1 --branch=master https://github.com/mhbahmani/Microsoft-Academic-Crawling mir_phase3
cd mir_phase3
sudo rm -rf .git

echo
echo "Setup cli"
echo

sudo rm -rf $main_destination 
sudo mv mir_phase3 $main_destination
sudo chmod +x $main_destination

pip3 install virtualenv
virtualenv venv

source venv/bin/activate
pip3 install -r requirements.txt
rm -rf MIR_Phase3.pdf example.json README.md

echo
echo "mir_phase3 successfully installed."
echo "enjoy!"
echo

