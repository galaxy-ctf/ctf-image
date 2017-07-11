import requests
import os
import shutil
import time
import subprocess
import json
import glob
from bioblend import toolshed
import argparse
import yaml

def cleanup(galaxy_root):
        print("preparing setup")
        db = os.path.join(galaxy_root, "database", "community.sqlite")
        files = os.path.join(galaxy_root, "database", "community_files")
        try:
            os.remove(db)
            shutil.rmtree(files)
        except OSError:
            pass

        # edit ini file
        ini = os.path.join(galaxy_root, "config", "tool_shed.ini.sample" )
        ini2 = os.path.join(galaxy_root, "config", "tool_shed.ini" )
        shutil.copyfile(ini, ini2)
        subprocess.Popen(["sed -i 's/#admin_users = None/admin_users = "+email+"/' "+ini2], shell=True)

def start_toolshed(galaxy_root, fg=False):
        print("starting toolshed")
        ts_run_script = os.path.join(galaxy_root, 'run_tool_shed.sh ')
        proc = subprocess.Popen([ts_run_script], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        if fg:
            proc.wait()

def create_admin_user(galaxy_root, email, username, password):
        print("creating admin user")
        user_info_xml = os.path.join(galaxy_root, 'scripts/tool_shed/bootstrap_tool_shed/user_info.xml')

        with open(user_info_xml, 'w') as f:
            f.writelines([
                '<?xml version="1.0"?>',
                '<user>'
                '<email>'+email+'</email>'
                '<password>'+password+'</password>'
                '<username>'+username+'</username>'
                '</user>'
                ])

        user_create_script = os.path.join(galaxy_root, 'scripts/tool_shed/bootstrap_tool_shed/create_user_with_api_key.py')
        s = subprocess.Popen(['cd '+galaxy_root +' && ' + 'python ' + user_create_script + ' -c config/tool_shed.ini'], shell=True)
        s.wait()

def get_api_key(email, password, toolshed):
    while True:
        try:
            r = requests.get(toolshed+'/api/authenticate/baseauth', auth=(email, password))
            apikey = json.loads(r.text)['api_key']
            break
        except Exception as e:
            print(e)
            print("Waiting on API key..")
            time.sleep(1)
    return str(apikey)

def create_categories(category_list, toolshed, apikey):
    print("creating categories")
    for c in category_list:
        params={'key':apikey, 'name':c, 'description':c}
        r = requests.post(toolshed+'/api/categories', data=params)
        print(r.text)

def install_tools(directory, toolshed, apikey, username):
    print("installing tools")
    planemo_cmd = [
        'planemo', 'shed_update',
        '--force_repository_creation',
        '--shed_target', toolshed,
        '--shed_key', apikey,
    ]

    for dirname in sorted(glob.glob(directory+'/*')):
        print("processing directory: "+dirname)
        print(subprocess.check_output(['planemo', '--version']))
        print(subprocess.check_output(planemo_cmd + [dirname]))

def get_category_name_by_id(cid, ts):
    cats = ts.categories.get_categories()
    for c in cats:
        if c['id'] == cid:
            return str(c['name'])

def make_tool_yaml(toolshed_url, apikey, galaxy_url='http://localhost:8080', galaxy_apikey='admin', blacklist=[]):
    ts = toolshed.ToolShedInstance(url=toolshed_url)
    repos = ts.repositories.get_repositories()

    tool_dict = (
        {'api_key': galaxy_apikey,
        'galaxy_instance': galaxy_url,
        'tools':[{
            'name': str(repo['name']),
            'owner': str(repo['owner']),
            'revisions':
                [ str(rev) for rev in ts.repositories.get_ordered_installable_revisions(repo['name'], repo['owner']) ] ,
            'tool_shed_url': toolshed_url,
            'tool_panel_section_label': get_category_name_by_id(repo['category_ids'][0], ts),
            'install_resolver_dependencies':'true',
            'install_tool_dependencies':'true'} for repo in repos if repo['name'] not in blacklist ]})

    # manually remove first revision for use_the_source_luke_2 challenge
    for t in tool_dict['tools']:
        if t['name'] == 'use_the_source_luke_2':
            del t['revisions'][0]

    with open('ctf_tools.yml', 'w') as toolyaml:
        yaml.dump(tool_dict, toolyaml, default_flow_style=False)


def stop_shed(galaxy_root):
    print("stopping toolshed")
    ts_run_script = os.path.join(galaxy_root, 'run_tool_shed.sh')
    proc = subprocess.Popen([ts_run_script + ' --stop-daemon'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

def setup(galaxy_root, email, password, username, catagories, toolshed, galaxy_url, galaxy_admin_api_key, tool_dir):

    # start fresh, remove old toolshed database
    cleanup(galaxy_root)

    # start toolshed
    start_toolshed(galaxy_root)

    while True:
        try:
            r = requests.get('http://localhost:9009')
            print(r.status_code)
            break
        except Exception:
            print("Not available yet, sleeping...")
            time.sleep(5)

    # configure admin user
    create_admin_user(galaxy_root, email, username, password)

    # get new user's api key
    apikey = get_api_key(email, password, toolshed)

    # create categories
    create_categories(categories, toolshed, apikey)

    # install tools
    install_tools(tool_dir, toolshed, apikey, username)

    # make tool yaml with all tools for installation to galaxy
    make_tool_yaml(toolshed, apikey, galaxy_url, galaxy_admin_api_key)

    # stop shed
    stop_shed(galaxy_root)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Populate the Galaxy toolshed with challenges.')
    parser.add_argument('-c', '--command', choices=['start', 'stop', 'setup', 'make_yaml'], dest='command', required=True)
    parser.add_argument('-g', '--galaxy_root', dest='galaxy_root', required=True)
    parser.add_argument('-t', '--toolshed', dest='toolshed_url', default='http://localhost:9009')
    parser.add_argument('-u', '--galaxy_url', dest='galaxy_url', default='http://localhost:80')
    parser.add_argument('-a', '--galaxy_admin_apikey', dest='galaxy_admin_api_key', default='admin')
    parser.add_argument('-d', '--tool_dir', dest='tool_dir', default='../challenges/tools')

    args = parser.parse_args()

    email = "galaxians@galaxians.org"
    password = "password"
    username = "galaxians"

    categories = ['intro', 'tool-dev', 'admin']

    # add names of any toolshed repos not to be installed here
    blacklist=['install_me']

    if args.command == 'stop':
        stop_shed(args.galaxy_root)
    elif args.command == 'start':
        start_toolshed(args.galaxy_root)
    elif args.command == 'setup':
        setup(args.galaxy_root, email, password, username, categories, args.toolshed_url, args.galaxy_url, args.galaxy_admin_api_key, args.tool_dir)
    elif args.command == 'make_yaml':
        toolshed_apikey = get_api_key(email, password, args.toolshed_url)
        make_tool_yaml(args.toolshed_url, toolshed_apikey, args.galaxy_url, args.galaxy_admin_api_key, blacklist)
