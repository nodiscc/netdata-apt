# netdata-apt

![](https://gitlab.com/nodiscc/toolbox/-/raw/master/DOC/SCREENSHOTS/QS3AbE3.png)

This is a `python.d` plugin for [netdata](https://my-netdata.io/). It parses output from [python3-apt](https://manpages.debian.org/bullseye/apt/apt.8.en.html) and the `/etc/debian_version` file. It provides charts/alarms for:
- Number of upgradable packages: when no package upgrades are available, the `upgradable` chart will have a value of 0. A value constantly higher than 0, for a time longer than 24 hours, will raise a netdata alarm/notification.
- The current distribution version: if the version (eg. `10`) is inferior to the configured/expected version (eg `11`), a netdata alarm/notification will be raised.


## Installation

```bash
# install requirements
sudo apt install python3-apt
# clone the repository
git clone https://gitlab.com/nodiscc/netdata-apt
# install configuration files/alarms
netdata_install_prefix="/opt/netdata" # if netdata is installed from binary/.run script
netdata_install_prefix="" # if netdata is installed from distribution packages
sudo cp -v netdata-apt/usr_libexec_netdata_python.d_apt.chart.py $netdata_install_prefix/usr/libexec/netdata/python.d/apt.chart.py
sudo cp -v netdata-apt/etc_netdata_python.d_apt.conf $netdata_install_prefix/etc/netdata/python.d/apt.conf
sudo cp -v netdata-apt/etc_netdata_health.d_apt.conf $netdata_install_prefix/etc/netdata/health.d/apt.conf
# restart netdata
sudo systemctl restart netdata
```


## Configuration

- If needed, change the expected distribution version in `etc_netdata_health.d_apt.conf` (the default is to expect Debian `11`).
- If needed, change the duration for which available upgrades can be `> 0` without trigerring an alarm in `etc_netdata_health.d_apt.conf` (`lookup:` setting). By default a warning will only be raised if the number of available upgrades is `> 0` for one day.
- The default `update every` value in `etc_netdata_python.d_apt.conf` is 600 seconds, so charts/alarms will only be created/updated after 600 seconds. Change this value if you need more accuracy.
- Common `python.d` plugin options can be changed in [`etc_netdata_python.d_apt.conf`](etc_netdata_python.d_apt.conf).

## Usage

You can get details on which packages need to be upgraded by running `apt list --upgradable` on the host.

This plugin assumes that a separate program (such as [unattended-upgrades](https://wiki.debian.org/UnattendedUpgrades)) updates the package lists (`apt update`) periodically for up-to-date information on available packages/versions. `unattended-upgrades` can fully automate security upgrades, but some packages may not be upgraded automatically (e.g. if you don't want to, or forgot to enable a repository in `Unattended-Upgrade::Origins-Pattern` in unattended-upgrades configuration).

Distribution upgrades (e.g. from Debian 10 to 11) should follow the [recommended procedure](https://debian-handbook.info/browse/stable/sect.dist-upgrade.html).



## Debug

To debug this plugin:

```bash
sudo -u netdata bash
$ $netdata_install_prefix/usr/libexec/netdata/plugins.d/python.d.plugin 1  debug trace apt
```

## License

[GNU GPLv3](LICENSE)

## Mirrors

- https://github.com/nodiscc/netdata-apt
- https://gitlab.com/nodiscc/netdata-apt

