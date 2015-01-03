from subprocess import Popen, PIPE
from servers.emailers import send_failure


class Ping(object):
    hostname = ''
    status_code = 0
    is_online = False
    has_checked = False

    def __init__(self, hostname):
        self.hostname = hostname

    def run_ping(self):
        if self.has_checked:
            return

        ping_response = Popen("ping -c 1 " + self.hostname, stdout=PIPE, stderr=PIPE, shell=True)
        out, error = ping_response.communicate()

        ping6_response = Popen("ping6 -c 1 " + self.hostname, stdout=PIPE, stderr=PIPE, shell=True)
        out6, error6 = ping6_response.communicate()

        self.status_code = ping_response.returncode | ping6_response.returncode
        self.out = out + out6
        self.error = error + error6

        self.has_checked = True

        # ping returns 0 on success, 1 when it didn't receive a reply, and 2
        # for all other error (name resolution failed, network unreachable,
        # etc.)
        # This allows us to check if a host is actually offline (ping or ping6
        # returned 1), while excluding the errors represented by exit code 2
        # (which could be caused by a local or remote lack of IPv6
        # connectivity).
        if self.status_code & 1 == 1:
            self.is_online = False
        else:
            self.is_online = True

        return self

