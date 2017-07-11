#!/bin/bash
for repo_id in $(curl http://toolshed.ctf.galaxians.org/api/repositories | jq '.[].id' -r); do
	curl http://toolshed.ctf.galaxians.org/repository/reset_all_metadata?id=$repo_id > /dev/null
done
