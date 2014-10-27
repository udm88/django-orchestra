import logging
import threading

from django import db

from orchestra.utils.python import import_class

from . import settings
from .helpers import send_report


logger = logging.getLogger(__name__)


def as_task(execute):
    def wrapper(*args, **kwargs):
        """ failures on the backend execution doesn't fuck the request transaction atomicity """
        db.transaction.set_autocommit(False)
        try:
            log = execute(*args, **kwargs)
        finally:
            db.transaction.commit()
            db.transaction.set_autocommit(True)
        if log.state != log.SUCCESS:
            send_report(execute, args, log)
        return log
    return wrapper


def close_connection(execute):
    """ Threads have their own connection pool, closing it when finishing """
    def wrapper(*args, **kwargs):
        try:
            log = execute(*args, **kwargs)
        except:
            raise
        else:
            # Using the wrapper function as threader messenger for the execute output
            wrapper.log = log
        finally:
            db.connection.close()
    return wrapper


def execute(operations):
    """ generates and executes the operations on the servers """
    router = import_class(settings.ORCHESTRATION_ROUTER)
    scripts = {}
    cache = {}
    # Generate scripts per server+backend
    for operation in operations:
        logger.debug("Queued %s" % str(operation))
        servers = router.get_servers(operation, cache=cache)
        for server in servers:
            key = (server, operation.backend)
            if key not in scripts:
                scripts[key] = (operation.backend(), [operation])
                scripts[key][0].prepare()
            else:
                scripts[key][1].append(operation)
            # Get and call backend action method
            method = getattr(scripts[key][0], operation.action)
            method(operation.instance)
    # Execute scripts on each server
    threads = []
    executions = []
    for key, value in scripts.iteritems():
        server, __ = key
        backend, operations = value
        backend.commit()
        execute = as_task(backend.execute)
        execute = close_connection(execute)
        thread = threading.Thread(target=execute, args=(server,))
        thread.start()
        threads.append(thread)
        executions.append((execute, operations))
    [ thread.join() for thread in threads ]
    logs = []
    # collect results
    for execution, operations in executions:
        for operation in operations:
            logger.info("Executed %s" % str(operation))
            operation.log = execution.log
            operation.save()
        stdout = execution.log.stdout.strip()
        stdout and logger.debug('STDOUT %s', stdout)
        stderr = execution.log.stderr.strip()
        stderr and logger.debug('STDERR %s', stderr)
        logs.append(execution.log)
    return logs
