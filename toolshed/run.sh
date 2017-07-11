#!/bin/bash

sed -i 's|host = 127.0.0.1|host = 0.0.0.0|g' $GALAXY_ROOT/config/tool_shed.ini
#python /setup_toolshed.py -g $GALAXY_ROOT -c start
source $GALAXY_VIRTUAL_ENV/bin/activate
# Launch nginx to deal with static files + pass to uWSGI
nginx &
# Launch uWSGI
uwsgi \
	--virtualenv /galaxy_venv \
	--ini-paste $GALAXY_ROOT/config/tool_shed.ini \
	-s 127.0.0.1:4001 \
	--pythonpath $GALAXY_ROOT/lib/
