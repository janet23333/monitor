import os

import tornado.ioloop
import tornado.web
from tornado.log import app_log
from tornado.options import define
from tornado.options import options

from conf import settings
from routes import ROUTES


server_config = settings['server']


def conf_log():
    define('port', default=server_config['port'], help='running on the given port', type=int)

    options.parse_command_line(final=False)

    # log rotate by time (day), max save 30 files
    options.log_rotate_mode = 'time'
    options.log_file_num_backups = 30
    options.logging = 'debug' if settings['debug'] else 'info'
    options.log_to_stderr = settings['debug']
    options.log_file_prefix = '{}/{}.log'.format(server_config['log_path'], options.port)

    options.run_parse_callbacks()

    portal_pid = os.path.join(server_config['run_path'], 'p_{}.pid'.format(options.port))
    with open(portal_pid, 'w') as f:
        f.write('{}'.format(os.getpid()))
    app_log.info('monitor center listening:{} Started'.format(options.port))


def main():
    conf_log()

    app = tornado.web.Application(ROUTES, debug=settings['debug'])
    app.listen(options.port, address='127.0.0.1', xheaders=True, decompress_request=True)

    tornado.ioloop.IOLoop.instance().start()
    app_log.info("monitor center is starting ..")


if __name__ == '__main__':
    main()
