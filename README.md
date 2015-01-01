# Dockerized Tristo Mietitore

A [dockerized](https://www.docker.com/) version of [tristo-mietitore](https://github.com/mapio/tristo-mietitore) collecting results from a set of (dockerized) instances of [Codebox](https://www.codebox.io/).

This system is based on three components: an *arbiter* that spins up the
*workers* (that are single user codebox instances) refering to the same
*tristo-mietitore* server. Every component runs in a docker container, as
described below.

## The arbiter

The arbiter is a web server that, for every distinct request, answers an
`username:token` pair. Presently are considered distinct requests coming from
different IPs (the `username` being the IP itself).

The `username:token` pair can be then used in subsequent requests to the
arbiter that will spin up a *worker* and issue an HTTP redirect to it (or just
redirect to an already running worker).

## The workers

A worker is an insance of [Codebox](https://www.codebox.io/) configured for
single user access, using the `username:token` pair as access credentials;
every worker listens on a different TCP port.

Usually the workers run on the same server that hosts the arbiter. Moreover,
every worker mounts the Codebox *workspace* as a local volume.

## Tristo mietitore

The last component is just a dockerized version of [tristo-mietitore](https://github.com/mapio/tristo-mietitore).

The only external dependency is the configuration file (that is mounted as a
single file volume); moreover, the *uploads* directory is also mounted as a
local volume.

![Analytics](https://ga-beacon.appspot.com/UA-377250-20/tm-docker?pixel)
