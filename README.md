# localshop-webhook

GitHub webhook for Localshop PyPI server.


## Installation

On a newly provisioned Debian/Jessie EC2 server, run

```
$ bin/bootstrap_debian
```

While the script is running, you will be prompted by the Localshop
installer to create username and password for an admin account.

After the script finishes running, open and edit
`/home/localshop/.pypirc`, replacing `<ACCESS_KEY>` and `<SECRET_KEY>`
with the Localshop admin credentials just created.

In `/etc/supervisor/conf.d/localshop.conf`, edit the `environment`
item of the section `[program:localshop-webhook]`:

```
environment=WEBHOOK_SECRET="mysecret",WEBHOOK_MATCHER_SPECS_FILE="/path/to/matcher.conf"
```

where `WEBHOOK_SECRET` is the key used by GitHub to sign commit
message body that the webhook receives, and
`WEBHOOK_MATCHER_SPECS_FILE` provides a path to a text file with each
line containing a tab-delimited pair of Git branch name and Python
version string regex used to decide whether the commit should trigger
package update in Localshop.

If necessary, create RSA keys as `localshop` user:

```
$ sudo su localshop
localshop$ ssh-keygen
(... follow instruction ...)
```

The public key needs to be associated with a GitHub account (e.g., a
machine user) so that the service can fetch GitHub repos.

Place SSL certificate and key at `/etc/ssl/certs/localshop.pem` and
`/etc/ssl/private/localshop.key` so that the web service communicates
over HTTPS.

Restart `nginx`:

```
$ sudo /etc/init.d/nginx restart
```

Restart `supervisor`:

```
$ sudo supervisorctl reload
```

The services need the following ports open:

```
Type             Protocol Port  Range
-----------------------------------------
SSH              TCP      22    0.0.0.0/0
HTTP             TCP      80    0.0.0.0/0
HTTPS            TCP      443   0.0.0.0/0
```


Visit `https://localshop.mydomain.io` with a browser as a Localshop
admin.

1. Go to Permissions -> CIDRs -> Create, and add `0.0.0.0/0` (i.e., open
to everyone) as CIDR.

2. Go to Permissions -> CIDRs -> Credentials, and create access key
and secret key.


## Usage

To install a package registered at Localshop,

```
$ pip install \
      -i https://<access key>:<secret key>@localshop.mydomain.io/simple/ \
      python-package-name [another-package ...]
```

where `<access key>` and `<secret key>` are the ones generated on the
Localshop admin panel.
