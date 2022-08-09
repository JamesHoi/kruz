# kruz 
kruz is a command line p2p file transfer tool
```bash
> kruz share file.txt
Share server started, waiting for client...
Connected from ('::ffff:127.0.0.1', 12478, 0, 0)
file.txt: 100%|██████████████████████████████████████████████████████████████████▉| 4.27M/4.27M [00:00<00:00, 98.5MB/s]
```

receive file
```bash
> kruz recv 127.0.0.1 19302
Connected to peer 127.0.0.1:19302
file.txt: 100%|███████████████████████████████████████████████████████████████████▉| 4.27M/4.27M [00:00<00:00, 100MB/s]
File recved, cost 0.7420966625213623s
```

## Install
[![Supported Versions](https://img.shields.io/pypi/pyversions/kruz.svg)](https://pypi.org/project/kruz) Require python>=3.8
```bash
pip install kruz
```
or you can install from source
```
git clone https://github.com/JamesHoi/kruz
cd kruz & python setup.py install
```

## Run tests

```bash
pip install pytest pytest-xdist
cd kruz & pytest
```

## TODO
1. show all ipv6 address
2. ctrl+c to cancel sharing
3. accomplish communication using udp protocol
4. hole puching
5. multi-thread sharing
5. send folder
