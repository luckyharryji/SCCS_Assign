
from .utils import union_urls

urls = union_urls([
    (r'/api/task','task.urls'),
    (r'/api/login','login.urls'),
    (r'/api/user','user.urls'),
    (r'/api/comment','comment.urls'),
    (r'/api/rank','rank.urls'),

])
