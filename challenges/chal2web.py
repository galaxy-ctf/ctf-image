#!/usr/bin/env python
import re
import uuid
import yaml
data = yaml.load(open('challenge_list.yml', 'r'))

cats = {}
for chal in data['challenges']:
    cat = chal['category']
    if cat not in cats:
        cats[cat] = []

    cats[cat].append(chal)

def cleanup(data):
    desc = re.sub(r'([^\s])\n([^\s])', r'\1 \2', data).strip()
    desc = re.sub(r'\n\n', r'\n', desc)
    return desc


cat_order = data['category_order']

newdata = {'chals': []}
for cat in cat_order:
    cat_chals = []
    for chal in cats[cat]:
        if isinstance(chal['flag'], dict):
            flags = [{
                'flag': chal['flag']['flag'],
                'regex': chal['flag']['regex'],
            }]
        else:
            flags = [{
                'flag': chal['flag'],
                'regex': False,
            }]

        cat_chals.append({
            'id': uuid.uuid4(),
            'name': chal['title'],
            'desc': cleanup(chal['description']),
            'value': chal['points'],
            'category': cat,
            'hints': chal.get('hints', []),
            'lesson': cleanup(chal.get('lesson', '')),
            'flags': flags
        })

    newdata['chals'].append({
        'name': cat,
        'desc': data['categories'][cat],
        'chals': cat_chals,
    })

print(yaml.dump(newdata, default_flow_style=False))
