import requests
import json
from loremipsum import get_paragraphs
import random
import os

galaxy_url = "http://localhost:80"

try:
    api_key = os.environ['TEAM_API_KEY']
except:
    api_key = 'admin'
    galaxy_url = "http://localhost:8080"

s_nouns = ["A hacker", "My mom", "Reviewer 3", "A kitten", "My supervisor", "The doctor", "The PI", "My lab partner", "This cool guy my gardener met yesterday", "The journal"]
p_nouns = ["These hackers", "Both of my moms", "The students", "My reviewers", "The PIs", "The statistician", "The monsters under my bed", "Your neighbours", "The journals"]
s_verbs = ["downloads", "sequences", "analyzes", "generates", "treats", "publishes", "meets with", "creates", "hacks", "configures", "spies on", "troubleshoots", "hides from", "tries to automate", "explodes"]
p_verbs = ["download", "sequence", "generate", "analyze", "treat", "publish", "meet with", "create", "hack", "configure", "spy on", "troubleshoot", "hide from", "try to automate", "explode"]
infinitives = ["for a laugh.", "for the manuscript", "for no apparent reason.", "because science.", "for a disease.", "to know more about biology."]

def make_sentence():
    return [random.choice(s_nouns), random.choice(s_verbs), random.choice(s_nouns).lower() or random.choice(p_nouns).lower(), random.choice(infinitives)]



# make a bunch of pages, one has the flag
'''
'slug'       = The title slug for the page URL, must be unique
'title'      = Title of the page
'content'    = HTML contents of the page
'annotation' = Annotation that will be attached to the page
'''

offset = 0
for i in range(offset, offset+25):
    content = '<br><br>'.join(get_paragraphs(5))
    if i == offset+16:
        content += '<br><br>gccctf{pages_let_you_describe_and_share_your_work}'

    payload={'slug':'page-'+str(i),
             'title': ' '.join(make_sentence()),
             'content': content,
             'annotation': 'no flags here',
             'published': True
             }
    headers={ 'Content-Type': 'application/json' }

    url = galaxy_url + '/api/pages/?key='+api_key
    r=requests.post(url, data=json.dumps(payload), headers=headers)
    print r.text
