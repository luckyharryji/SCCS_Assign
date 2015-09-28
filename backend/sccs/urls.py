
from .utils import union_urls

urls = union_urls([
    (r'/api/task','task.urls'),
    (r'/api/login','login.urls'),
])
