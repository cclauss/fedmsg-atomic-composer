import subprocess
import fedmsg.consumers

class OSTreeComposer(fedmsg.consumers.FedmsgConsumer):
    topic = ['org.fedoraproject.prod.bodhi.updates.fedora.sync',
             #'org.fedoraproject.prod.compose.branched.complete',
             'org.fedoraproject.prod.compose.branched.rsync.complete',
             'org.fedoraproject.prod.compose.rawhide.rsync.complete']
    config_key = 'ostreecomposer'

    def __init__(self, *args, **kw):
        super(OSTreeComposer, self).__init__(*args, **kw)

    def consume(self, msg):
        self.log.debug(msg)
        body = msg['body']
        topic = body['topic']

        if 'rawhide' in topic:
            self.log.info('New rawhide compose ready')
            arch = body['msg']['arch']
        elif 'branched' in topic:
            self.log.info('New branched compose ready')
            arch = body['msg']['arch']
            branch = body['msg']['branch']
            log = body['msg']['log']
            if log != 'done':
                self.log.warn('Compose not done?')
                return
        elif 'updates' in topic:
            self.log.info('New updates compose ready')
            release = body['msg']['release']
            repo = body['msg']['repo']

        # ostree compose
        # extract summary
        # inject summary into repodata

    def call(self, cmd, **kwargs):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kwargs)
        out, err = p.communicate()
        return out, err, p.returncode