from data.users import users
from schemas.user_schemas import NewUser, UpdateUser
from exceptions import EmailLinkedError, EmailRegisteredError

class UserService:
    def __init__(self):
        self.users = users

    def check_duplicate_user(self,new_user: NewUser):
        if any(user.email == new_user.email for user in self.users.values()):
            raise EmailLinkedError()

    def check_duplicate_user_during_update(self,  current_user_id: str, update_user: UpdateUser):
        if any(user.email == update_user.email
               and user.id != current_user_id
               for user in self.users.values()):
            raise EmailRegisteredError()






