class User(object):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def from_dict(source):
        user = User(source["id"], source["username"], source["email"], source["password"])
        return user

    def to_dict(self):
        user = {}
        user["id"] = self.id
        user["username"] = self.username
        user["email"] = self.email
        user["password"] = self.password
        return user

    def __repr__(self):
        return (
            f"User(id={self.id}, username={self.username}, email={self.email}, password={self.password})"
        )

@staticmethod
def add_user(db, user, update = False):
    if update:
        if get_user_by_id(db, user.id) == None:
            return False
    else:
        if get_user_by_id(db, user.id) != None:
            return False
    user_dict = user.to_dict()
    doc_ref = db.collection(u"users").document(user_dict["id"])
    del user_dict["id"]
    doc_ref.set(user_dict)
    return True

@staticmethod
def update_user(db, user):
    return add_user(db, user, update = True)

@staticmethod
def authenticate_user(db, id, password):
    user = get_user_by_id(db, id)
    if user == None:
        return False
    if user.password != password:
        return False
    return True

@staticmethod
def get_user_by_id(db, id):
    users_ref = db.collection(u"users")
    doc_ref = users_ref.document(id)
    doc = doc_ref.get()
    if doc.exists:
        user_dict = { "id": id,
                     "username": doc.get("username"),
                     "email": doc.get("email"),
                     "password": doc.get("password")}
        return User.from_dict(user_dict)
    else:
        return None

@staticmethod
def get_user_by_username(db, username):
    users_ref = db.collection(u"users")
    query_ref = users_ref.where(u"username", u"==", username)
    docs = query_ref.stream()
    for doc in docs:
        user_dict = doc.to_dict()
        user_dict["id"] = doc.id
        return User.from_dict(user_dict)
    return None

@staticmethod
def get_user_by_email(db, email):
    users_ref = db.collection(u"users")
    query_ref = users_ref.where(u"email", u"==", email)
    docs = query_ref.stream()
    for doc in docs:
        user_dict = doc.to_dict()
        user_dict["id"] = doc.id
        return User.from_dict(user_dict)
    return None
