# MapMiddleware: A middleware for EFB

## Notice

**Middleware ID**: `jiz4oh.map`

**MapMiddleware** is a middleware of EFB for parse amap url.

## How it works

replace the parsable amap url to the `Location` message.

### before

<img width="666" height="298" alt="PixPin_2025-11-11_18-14-49" src="https://github.com/user-attachments/assets/aa0c56cf-6228-47e3-ad16-792231cfaa26" />

### after

<img width="674" height="322" alt="PixPin_2025-11-11_18-14-59" src="https://github.com/user-attachments/assets/40b48286-306c-4391-a172-b19ff19b3d62" />

## Dependense
* Python >= 3.6
* EFB >= 2.0.0

## Install and configuration

### Install

```
pip install git+https://github.com/jiz4oh/efb-map-middleware.git
```

### Enable

Register to EFB
Following [this document](https://ehforwarderbot.readthedocs.io/en/latest/getting-started.html) to edit the config file. The config file by default is `$HOME/.ehforwarderbot/profiles/default`. It should look like:

```yaml
master_channel: foo.demo_master
slave_channels:
- foo.demo_slave
- bar.dummy
middlewares:
- foo.other_middlewares
- jiz4oh.map
```

You only need to add the last line to your config file.

### Restart EFB.

