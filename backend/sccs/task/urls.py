
from . import handlers

urls = [
    (r'/list', handlers.TaskListHandler), #deal with the request about taskList
    (r'/(\d+)', handlers.TaskDetailHandler),
    (r'/found/(\d+)/(\d+)', handlers.FounderHandler),
]
