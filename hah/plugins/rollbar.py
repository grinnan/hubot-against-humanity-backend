from flask import Request, got_request_exception
import hah
import os

import werkzeug.exceptions

def init_rollbar(app):
    if 'ROLLBAR_ACCESS_TOKEN' in app.config:
        import rollbar.contrib.flask
        import rollbar

        rollbar.init(
            app.config['ROLLBAR_ACCESS_TOKEN'],
            app.config['ENV'],
            root=os.path.dirname(os.path.realpath(hah.__file__)),
            allow_logging_basic_config=False,
            exception_level_filters=[
                (werkzeug.exceptions.HTTPException, 'warning'),
            ]
        )

        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

        app.logger.info('[rollbar.init_rollbar] Rollbar enabled')
    else:
        app.logger.info('[rollbar.init_rollbar] Rollbar disabled')
