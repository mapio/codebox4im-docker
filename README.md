# Dockerized Tristo Mietitore

A [dockerized](https://www.docker.com/) version of [tristo-mietitore](https://github.com/mapio/tristo-mietitore) collecting results from a set of (dockerized) instances of [Codebox](https://www.codebox.io/).

This system is based on three components: a *arbiter* that spins up the
*workers* (that are single user codebox instances) refering to the same
*tristo-mietitore* server. Every component runs in a docker container, as
described below.

## The arbiter

The arbiter is a web server that, for every distinct request, answers an
`username:token` pair. Presently are considered distinct requests coming from
different IPs (the `username` being the IP itself). The `token` can be used in
a subsequent request to have the arbiter spin up a *worker*.

## The workers

A worker is an insance of [Codebox](https://www.codebox.io/) configured for
single user access, using the `username:token` pair as access credentials.
Every worker runs on a different TCP port.

## Tristo mietitore

The last component is just a dockerized version of [tristo-mietitore](https://github.com/mapio/tristo-mietitore).
