#!/bin/bash
printf '{"team": {"id": "%d", "name": "%s"}}' "$TEAM_ID" "$TEAM_NAME" > $GALAXY_ROOT/version.json;

export GALAXY_CONFIG_NGINX_X_ACCEL_REDIRECT_BASE=${PROXY_PREFIX}/_x_accel_redirect
export GALAXY_CONFIG_NGINX_X_ARCHIVE_FILES_BASE=${PROXY_PREFIX}/_x_accel_redirect
export GALAXY_CONFIG_NGINX_UPLOAD_PATH=${PROXY_PREFIX}/_upload

if [[ $(grep -c "${PROXY_PREFIX}" /etc/nginx/nginx.conf) -eq 0  ]]; then
	sed -i "s|location\s*/|location ${PROXY_PREFIX}/|g" /etc/nginx/nginx.conf
	sed -i "s|location ~ ^/plugins|location ~ ^${PROXY_PREFIX}/plugins|g" /etc/nginx/nginx.conf
	sed -i "s|upload_pass\s*/_upload_done|upload_pass ${PROXY_PREFIX}/_upload_done|g" /etc/nginx/nginx.conf
fi;


# start galaxy
/usr/bin/startup &

# wait til galaxy has started
$GALAXY_ROOT/sleep.py http://localhost:80

echo "Creating Galaxy user $TEAM_NAME@galaxy.org with password $TEAM_PASSWORD"
# Create login user
. $GALAXY_VIRTUAL_ENV/bin/activate;
export TEAM_NAME=${TEAM_NAME:-temp_name}
export TEAM_PASSWORD=${TEAM_PASSWORD:-temp_password}
export TEAM_API_KEY=key-${GALAXY_DEFAULT_ADMIN_PASSWORD}
python /usr/local/bin/create_galaxy_user.py \
	--user $TEAM_NAME@galaxy.org \
	--password $TEAM_PASSWORD \
	--key $TEAM_API_KEY \
	--username $TEAM_NAME;
deactivate;
# The admin user still exists, but with pseudo-random password.

# make yaml with all ctf tools
python /setup_toolshed.py -g $GALAXY_ROOT -c make_yaml -t ${CTF_TOOLSHED_URL} --galaxy_url "http://localhost:80"

# install ctf tools to galaxy
shed-install -a ${GALAXY_CONFIG_MASTER_API_KEY} -t ctf_tools.yml -g "http://localhost:80"

# install pages chall to regular user account
python $GALAXY_ROOT/challenges/makepage.py

tail -f /home/galaxy/logs/handler*.log
