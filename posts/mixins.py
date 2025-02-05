class UsernameDisplayMixin:
    
    @property
    def get_username_display(self):
        return self.user.profile.username_display or self.user.profile.full_name
