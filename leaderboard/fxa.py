import requests

class FxaProfileServer(object):
    PROD_PROFILE_SERVER = "https://profile.accounts.firefox.com/v1/profile"
    DEV_PROFILE_SERVER = "https://stable.dev.lcip.org/profile/v1"

    def __init__(self):
        # TODO: this needs to be repointed to the production server in
        # a config object or something.
        self.fxa_url = self.DEV_PROFILE_SERVER


    def fetch_profile(self, bearer_token):
        '''
        Fetch a profile JSON blob from the FxA profile server and
        return a tuple of (email address, nickname)

        A typical profile response will be a JSON blob that looks
        like:
        {
          "uid": "6d940dd41e636cc156074109b8092f96",
          "email": "user@example.domain",
          "avatar": "https://secure.gravatar.com/avatar/6d940dd41e636cc156074109b8092f96"
        }
        '''
        email_address = display_name = ''

        headers = {'Authorization': 'Bearer %s' % bearer_token}

        try:
            r = requests.get(self.fxa_url, headers=headers)
            json_response = r.text
            jdata = json.loads(json_response)
            email_address = jdata.get('email', '')
            display_name = jdata.get('displayName', '')
        except:
            return ('', '')


        return (email_address, display_name)

