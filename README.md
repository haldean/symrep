symrep
===
`symrep` is an attempt to make a general-purpose, hierarchical, functional
representation for media using function composition. Graphs that represent some
creative entity are constructed from nested function calls, these graphs can
then be sampled at different parameter values with varying results. `symrep` is
written to be parameter-space agnostic, allowing for it to be used for
everything from 5.1-channel audio to functional representation of 3D models.

For example, the source code for audio synthesis (using the `symrep.audio`
package) in [examples/sound.py](https://github.com/haldean/symrep/blob/master/examples/sound.py)
gives [this sound file](examples/sound.wav) from the following graph:

![](examples/sound.png)

The source code for solid modelling (using the `symrep.solids` package) in
[examples/solids.py](https://github.com/haldean/symrep/blob/master/examples/sphere.py)
gives these solid bodies (rendered by MeshLab):

![](https://raw.githubusercontent.com/haldean/symrep/master/examples/sphere.gif)

from this graph:

![](examples/sphere.png)
