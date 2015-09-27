import logging

from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import define,options,parse_command_line

from sccs.settings import PROJECT_NAME,settings
from sccs.urls import urls

define("port",default=8000,help="run on this port",type=int)
define("create_tables",help="create tables")


def make_app():
    return Application(urls,**settings)

def main():
    parse_command_line()
    if options.create_tables:
        #print "creating tables"
        from sccs.base.models import db
        from sccs.user.models import User
        from sccs.task.models import Task,TaskWorker
        from sccs.mid_credit.models import MidCredit,CreditLog
        from sccs.comment.models import Comment
        db.create_tables([User,Task,TaskWorker,MidCredit,CreditLog,Comment])
        return True
    else:
        logging.info("Application listen on port %s" % options.port)
        app=make_app()
        app.listen(options.port)
        IOLoop.current().start()

if __name__=='__main__':
    main()
