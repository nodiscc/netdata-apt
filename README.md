# netdata-apt

![]()

This is a `python.d` plugin for [netdata](https://my-netdata.io/). It parses output from [apt](https://manpages.debian.org/bullseye/apt/apt.8.en.html) and the `/etc/debian_version` file. It provides charts/alarms for:
- number of upgradeable packages: when no package upgrades are available, the `upgradeable` chart will have a value of 0. Values higher than 0 will raise a netdata alarm/notification.
- current distribution version/availability of a distribution upgrade: If the detected `distribution_version` (eg. `10`) is inferior to the configured/expected version (eg `11`), a netdata alarm/notification will be raised.


## Installation

This plugin expects the output of `apt list --upgradable |wc -l` at `/var/log/netdata/netdata-apt.log`


```bash
# clone the repository
git clone https://gitlab.com/nodiscc/netdata-apt
# generate the initial file
apt list --upgradable | wc -l | sudo tee /var/log/netdata-apt.log
# configure dpkg to refresh the file after each run
sudo cp netdata-apt/etc_apt_apt.conf.d_99netdata-apt /etc/apt/apt.conf.d/99netdata-apt
# add a cron job to refresh the file periodically
sudo cp netdata-apt/etc_cron.d_netdata-apt /etc/cron.d/netdata-apt
# install configuration files/alarms
netdata_install_prefix="/opt/netdata" # if netdata is installed from binary/.run script
netdata_install_prefix="" # if netdata is installed from OS packages
sudo cp -v netdata-apt/usr_libexec_netdata_python.d_apt.chart.py $netdata_install_prefix/usr/libexec/netdata/python.d/apt.chart.py
sudo cp -v netdata-apt/etc_netdata_python.d_apt.conf $netdata_install_prefix/etc/netdata/python.d/apt.conf
sudo cp -v netdata-apt/etc_netdata_health.d_apt.conf $netdata_install_prefix/etc/netdata/health.d/apt.conf
# restart netdata
sudo systemctl restart netdata
```


## Configuration

If needed, change the expected distribution version in `health.d_apt.conf` (the default is to expect Debian `11`). Common `python.d` plugin options can be changed in [`etc_netdata_python.d_apt.conf`](etc_netdata_python.d_apt.conf). The default `update every` value is 30 seconds so the chart will only be created/updated after 30 seconds. Change this value if you need more accuracy.

You can get details on which packages need to be upgraded by running `apt list --upgradeable` on the host. It is recommended to setup [UnattendedUpgrades](https://wiki.debian.org/UnattendedUpgrades) for stable/security package repositories. Distribution upgrades should be follow the [recommended procedure](https://debian-handbook.info/browse/stable/sect.dist-upgrade.html).



## Debug

To debug this plugin:

```bash
sudo -u netdata bash
$ $netdata_install_prefix/usr/libexec/netdata/plugins.d/python.d.plugin 1  debug trace apt
```

## TODO

- Graph number of available updates
- Alert when > 0
- Graph current debian version
- Alert when < $expected

## License

[GNU GPLv3](LICENSE)

## Mirrors

- https://github.com/nodiscc/netdata-apt
- https://gitlab.com/nodiscc/netdata-apt

