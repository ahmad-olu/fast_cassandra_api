from enum import Enum

class PostType(Enum):
    COMIC = "Comic"
    NOVEL = "Novel"

class NotificationType(Enum):
    LIKES = "Likes"
    COMMENT = "Comment"
    REIMAGINED = "Re_imagined"
    FOLLOW = "followed"


class Category(Enum):
    pass