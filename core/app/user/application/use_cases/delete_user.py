
class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str) -> None:
        user = self.repository.find_by_id(user_id)
        if user is None:
            raise UserNotFound
        self.repository.delete(user)

