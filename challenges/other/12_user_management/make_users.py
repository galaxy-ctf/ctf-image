import sys
sys.path.insert(1,'/galaxy-central')
sys.path.insert(1,'/galaxy-central/lib')

from galaxy.model import User, APIKeys
from galaxy.model.mapping import init
from galaxy.model.orm.scripts import get_config

import generate_names as makenames
import random
import string

def add_user(sa_session, security_agent, email, password, key, username):
    query = sa_session.query( User ).filter_by( email=email )
    if query.count() > 0:
        return query.first()
    else:
        User.use_pbkdf2 = False
        user = User(email)
        user.username = username
        user.set_password_cleartext(password)
        sa_session.add(user)
        sa_session.flush()

        security_agent.create_private_user_role( user )
        if not user.default_permissions:
            security_agent.user_set_default_permissions( user, history=True, dataset=True )

        if key is not None:
            api_key = APIKeys()
            api_key.user_id = user.id
            api_key.key = key
            sa_session.add(api_key)
            sa_session.flush()
        return user


if __name__ == '__main__':
    db_url = get_config(sys.argv)['db_url']
    mapping = init('/tmp/', db_url)
    sa_session = mapping.context
    security_agent = mapping.security_agent

    # make the users with flags, one in email and one in api key
    add_user(sa_session, security_agent, 'gccctf{m4n4ge_y@ur.us3rs}', 'supersecurepassword', 'noflaghere!',  'flag_thief')
    add_user(sa_session, security_agent, 'zany_galaxian@gccctf.org', 'supersecurepassword', 'gccctf{th3_k3y_t0_my_fl4g}',  'zany_galaxian')

    # make bunch of decoy users
    for _ in range(300):
        publicname = makenames.get_random_name()
        email = publicname+'@gccctf.org'
        key = ''.join(random.SystemRandom().choice(string.hexdigits).lower() for _ in range(32))
        try:
            add_user(sa_session, security_agent, email, 'supersecurepassword', key, publicname)
        except:
            pass
