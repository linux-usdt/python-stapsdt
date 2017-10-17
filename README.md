# python-stapsdt

Create USDT probes and instrument your Python application dynamically.

# Dependencies

At the moment this package only runs on Linux and requires
[libstapsdt](https://github.com/sthima/libstapsdt) to be installed to create
runtime probes.

## Ubuntu 16.04

To install libstapsdt, run:

```bash
sudo add-apt-repository ppa:sthima/oss
sudo apt-get update
sudo apt-get install libstapsdt0 libstapsdt-dev
```

## Other

Build from [libstapsdt](https://github.com/sthima/libstapsdt).

# Install

```bash
pip install stapsdt
```

# Example

The following code will create a probe named `firstProbe`.

```python
from time import sleep

import stapsdt

provider = stapsdt.Provider("pythonapp")
probe = provider.add_probe(
    "firstProbe", stapsdt.ArgTypes.uint64, stapsdt.ArgTypes.int32)
provider.load()


while True:
    print("Firing probe...")
    if probe.fire("My little probe", 42):
        print("Probe fired!")
    sleep(1)
```

You can then trace this probe with any tool able to trace Systemtap's probes.
Here's an example with eBPF/bcc:

```bash
sudo trace -p PID 'u::firstProbe "%s - %d", arg1, arg2'
```
