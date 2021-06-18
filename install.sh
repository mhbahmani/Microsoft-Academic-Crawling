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

curl_inst=0
[ $(curl --version | grep -Eci 'release-date') = 0 ] && curl_inst=1

if [ $curl_inst = 1 ]; then
    if [ -z $package_manager ]; then
        echo "unknown linux distro".
        echo "try installing curl with your package manager"
        echo "then run the installation command again"
        echo "exiting."
        exit
    fi
    [ curl_intst = 1 ] && $package_manager curl python3-pip git -y
fi


main_destination=/usr/local/bin/mir_phase3

rm -rf $HOME/.local/share/mir_phase3
cd $HOME/.local/share
git clone https://github.com/mhbahmani/Microsoft-Academic-Crawling mir_phase3
cd mir_phase3

sudo rm -rf $main_destination 
sudo mv mir_phase3 $main_destination
sudo chmod +x $main_destination

pip3 install -r requirements.txt
rm -rf MIR_Phase3.pdf example.json README.md

echo "mir_phase3 successfully installed."
echo "enjoy!"
echo

