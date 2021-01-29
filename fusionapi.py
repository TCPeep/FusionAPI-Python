import requests
import json


url = "https://fusionapi.dev/"


def client_ip():
    """Fetches and returns the current public IP address."""
    r = requests.get(f"{url}api/ip")
    return json.loads(r.content)["ip"]


class FusionApp:

    def __init__(self, appid):
        self.appid = appid
        self.session = "NOT_LOGGED_IN"
        self.username = ""
        self.app_cache = ""
        self.user_cache = ""

    def login(self, username, password):
        """Login to FusionAPI app and initialize session. Caches session and username."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"username": username,
                                "password": password,
                                "action": "login"})
        response = json.loads(r.content)
        if not response["error"]:
            self.session = response["session"]
            self.username = username
        return json.loads(r.content)

    def check_2fa(self, username):
        """No example, self explanatory. Checks if a user has 2 Factor Authentication enabled."""
        r = requests.post(f"{url}app/{self.appid}/api", data={"username": username, "action": "has2fa"})
        return json.loads(r.content)

    def register(self, username, password, token):
        """Register, no example. May update to automatically login after successful registration."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"username": username,
                                "password": password,
                                "token": token,
                                "action": "register"})
        return json.loads(r.content)

    def app_blob(self):
        """Fetches the application blob. Caches as app_cache."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "action": "appblob"})
        response = json.loads(r.content)
        if not response["error"]:
            self.app_cache = response["blob"]
        return response

    def execute_api(self, id, data):
        """Executes an unauthenticated and non time-based API."""
        r = requests.post(f"{url}executeapi/{id}",
                          data={"data": data})
        return json.loads(r.content)

    def execute_auth_api(self, id, data):
        """Executes an authenticated, but not time-based API."""
        r = requests.post(f"{url}executeapi/{id}",
                          data={"data": data,
                                "session": self.session})
        return json.loads(r.content)

    def execute_time_api(self, id, data, time):
        """Executes an unauthenticated time-based API."""
        r = requests.post(f"{url}executeapi/{id}",
                          data={"data": data,
                                "time": time})
        return json.loads(r.content)

    def execute_full_api(self, id, data, time):
        """Executes an API with authentication and time-based enabled."""
        r = requests.post(f"{url}executeapi/{id}",
                          data={"data": data,
                                "time": time,
                                "session": self.session})
        return json.loads(r.content)

    def get_user_vars(self):
        """Fetches all user variables."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "action": "myvars"})
        return json.loads(r.content)

    def get_app_vars(self):
        """Fetches all app variables."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "action": "get-app-vars"})
        return json.loads(r.content)

    def get_app_var(self, var):
        """Fetches a singular app variable."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "action": "get-app-vars"})
        try:
            return json.loads(r.content)["vars"][var]
        except KeyError:
            return "Invalid Variable."

    def set_user_var(self, key, value):
        """Sets a user variable."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "key": key,
                                "value": value,
                                "action": "set-user-vars"})
        return json.loads(r.content)

    def get_user_var(self, var):
        """Fetches a singular user variable."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "action": "myvars"})
        try:
            return json.loads(r.content)["vars"][var]
        except KeyError:
            return "Invalid Variable."

    def change_password(self, old, new):
        """Used to update a user password. Olf password is required."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "oldpassword": old,
                                "newpassword": new,
                                "action": "change-pass"})
        return json.loads(r.content)

    def user_blob(self):
        """Fetches user blob. Cached as user_cache"""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "action": "myblob"})
        response = json.loads(r.content)
        if not response["error"]:
            self.user_cache = response["blob"]
        return response

    def get_app_chat(self):
        """Fetches entire application chat."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "action": "get-app-chat"})
        return json.loads(r.content)

    def delete_app_message(self, messageid):
        """Used to delete messages in the application chat."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "mid": messageid,
                                "action": "del-app-msg"})
        return json.loads(r.content)

    def edit_app_message(self, messageid):
        """Used to edit messages in the application chat."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "mid": messageid,
                                "action": "edit-app-msg"})
        return json.loads(r.content)

    def send_app_message(self, content):
        """Used to send messages in the application chat."""
        r = requests.post(f"{url}app/{self.appid}/api",
                          data={"session": self.session,
                                "message": content,
                                "action": "send-app-msg"})
        return json.loads(r.content)
