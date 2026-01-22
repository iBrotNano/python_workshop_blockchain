import subprocess
import json
from constants import ELECTRUM_EXE, NETWORK


class Electrum:
    def __init__(self, network):
        self.network = network

    def open(self):
        subprocess.Popen(
            [ELECTRUM_EXE, f"--{self.network}", "gui"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def call(self, *args):
        res = subprocess.run(
            [ELECTRUM_EXE, f"--{self.network}", *args],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if res.returncode != 0:
            raise RuntimeError(res.stderr, res.stdout)

        try:
            return json.loads(res.stdout)
        except json.JSONDecodeError:
            return res.stdout.strip()


if __name__ == "__main__":
    electrum = Electrum(NETWORK)
    electrum.open()
