# pycobaltstrike

A pure python, Cobalt Strike External C2 client library.

This library provides convenience methods for interacting with a Cobalt Strike teamserver via its [External C2](https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/listener-infrastructure_external-c2.htm) mechanism. It implemenents the specification as defined [here](https://hstechdocs.helpsystems.com/kbfiles/cobaltstrike/attachments/externalc2spec.pdf).

## installation

```bash
pip install pycobaltstrike
```

## overview

This project provides two classes for working with Cobalt Strike via its external c2 mechanism.

- `CobaltStrike()` - This class handles connections to a teamserver and is responsible for sending and receiving frames between a teamserver and an implementor.
- `Frame()` - This class is a representation of the raw bytes that is sent to and from a teamserver via the `CobaltStrike` class. It contains various convenience methods for working with data.

## usage example

Once installed, import the library (and the `Frame` class if you need it).

```python
from pycobaltstrike import CobaltStrike, Frame
```

Next, instantiate a new instance of `CobaltStrike` and then connect to an external c2 server.

```python
cs = CobaltStrike()
cs.connect('remote.host', 2222)
```

With the `cs` object connected to a Cobalt Strike teamserver, we can now request a stager.

```python
stager = cs.get_stage(arch='x64', pipename='tutorial')
```

Getting the result of `stager` to run is out of the scope of this library, however, once that is running and you are able to relay frames, you can do so by sending and receiving `Frame` objects.

```python
# assuming data here is the raw frame bytes you want to send to the teamserver
data = b'00'
frame = Frame(data)

cs.send(frame=frame)

# response from the teamserver will also return a Frame
response = cs.recv()
```

Thats it!

## the `Frame` object

Data sent up and down using `send()` and `recv()` are instances of the `Frame` class. `Frame`'s have some convenience methods as shown below.

The specification states that data frames sent to and from the teamserver via external c2's must have the format of `[size][payload]`. When instantiating a new `Frame` using the class constructor, note that this should purely be data and not include the length prefix as indicated by the [specification](https://hstechdocs.helpsystems.com/kbfiles/cobaltstrike/attachments/externalc2spec.pdf). If you have a payload that includes the length prefix, use `Frame.from_bytes()`.

```python
# init a frame from data that does not include length prefix
frame = Frame(b'00')

# init a frame from data that *does* include the length prefix
frame = Frame.from_bytes(b'00')

# init a frame from base64 encoded data that *does* include the length prefix
frame = Frame.from_base64('bXVoYWhhCg==')

# return the raw bytes of a frame that includes the size prefix
frame_bytes = frame.as_bytes()
```

