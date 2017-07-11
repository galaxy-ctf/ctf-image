#!/bin/bash
set -x
sed -i 's/bioblend==0.7.0.*/#bioblend==0.7.0/' lib/galaxy/dependencies/pinned-requirements.txt lib/galaxy/dependencies/pinned-hashed-requirements.txt

source $GALAXY_VIRTUAL_ENV/bin/activate;
pip install -U bioblend==0.8.0
pip install planemo==0.38.1
python /setup_toolshed.py -g $GALAXY_ROOT -c setup

echo -e "\nallow_user_creation = False" >> $GALAXY_ROOT/config/tool_shed.ini
