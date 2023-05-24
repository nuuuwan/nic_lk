import os

from utils import JSONFile, Log

from nic_lk.core.NIC import NIC
from tests.EXAMPLE_NIC_NO_LIST import EXAMPLE_NIC_NO_LIST

EXAMPLE_PATH = os.path.join('tests', 'EXAMPLE_NICS.json')
EXAMPLE_FILE = JSONFile(EXAMPLE_PATH)

log = Log('examples')


def generate_examples():
    d_list = []
    for nic_no in EXAMPLE_NIC_NO_LIST:
        nic = NIC(nic_no)
        if not nic.is_valid:
            raise ValueError(f'Invalid NIC: {nic_no}')
        d = nic.to_dict()
        d_list.append(d)
    EXAMPLE_FILE.write(d_list)
    log.debug(f'Wrote {len(EXAMPLE_NIC_NO_LIST)} examples to {EXAMPLE_PATH}')


EXMPLE_LIST = None
if EXAMPLE_FILE.exists:
    EXMPLE_LIST = EXAMPLE_FILE.read()

if __name__ == '__main__':
    generate_examples()
