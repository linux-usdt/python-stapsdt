__ALL__ = ['Provider', 'Probe', 'ArgTypes']

from enum import IntEnum
from ctypes import cdll, c_char_p, c_void_p, c_int

stapsdt_lib = cdll.LoadLibrary("libstapsdt.so")

# SDTProvider_t *providerInit(const char *name);
providerInit = stapsdt_lib.providerInit
providerInit.argtypes = [c_char_p]
providerInit.restype = c_void_p

# SDTProbe_t *providerAddProbe(SDTProvider_t *provider, const char *name,
#                              int argCount, ...);
providerAddProbe = stapsdt_lib.providerAddProbe
providerAddProbe.argtypes = [c_void_p, c_char_p]
providerAddProbe.restype = c_void_p

# int providerLoad(SDTProvider_t *provider);
providerLoad = stapsdt_lib.providerLoad
providerLoad.argtypes = [c_void_p]
providerLoad.restype = c_int

# int providerUnload(SDTProvider_t *provider);
providerUnload = stapsdt_lib.providerUnload
providerUnload.argtypes = [c_void_p]
providerUnload.restype = c_int

# void providerDestroy(SDTProvider_t *provider);
providerDestroy = stapsdt_lib.providerDestroy
providerDestroy.argtypes = [c_void_p]
providerDestroy.restype = c_int

# void probeFire(SDTProbe_t *probe, ...);
probeFire = stapsdt_lib.probeFire
probeFire.argtypes = [c_void_p]
probeFire.restype = c_void_p

# int probeIsEnabled(SDTProbe_t *probe);
probeIsEnabled = stapsdt_lib.probeIsEnabled
probeIsEnabled.argtypes = [c_void_p]
probeIsEnabled.restype = c_int


class Provider(object):
    def __init__(self, name):
        self._name = name
        self._provider = providerInit(c_char_p(name.encode('ascii')))
        self._probes = []

    def __str__(self):
        return self.name

    def add_probe(self, name, *args):
        probe = Probe(self, name, *args)
        self._probes.append(probe)
        return probe

    def load(self):
        return bool(providerLoad(self._provider))

    def unload(self):
        return bool(providerUnload(self._provider))

    def __del__(self):
        providerDestroy(self._provider)
        for probe in self._probes:
            probe._provider = None
            probe._probe = None


class Probe(object):
    def __init__(self, provider, name, *args):
        self._provider = provider
        self._name = name
        self._argc = len(args)
        self._args = args
        self._probe = providerAddProbe(
            provider._provider,
            c_char_p(name.encode('ascii')),
            len(args), *args)

    def fire(self, *args):
        if not self._probe:
            return False
        if not self.is_enabled:
            return False

        args = list(args)
        for i, arg in enumerate(args):
            if isinstance(arg, str):
                args[i] = c_char_p(arg.encode("utf-8"))
        args = tuple(args)
        probeFire(self._probe, *args)
        return True

    @property
    def is_enabled(self):
        if not self._probe:
            return False
        return bool(probeIsEnabled(self._probe))


class ArgTypes(IntEnum):
    noarg = 0
    uint8 = 1
    int8 = -1
    uint16 = 2
    int16 = -2
    uint32 = 4
    int32 = -4
    uint64 = 8
    int64 = -8
