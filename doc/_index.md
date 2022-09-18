# Zakhar Brain Service

[![view - Documentation](https://img.shields.io/badge/Source%20Code-GitHub-blue)](https://github.com/Zakhar-the-Robot/brain_service "Go to repository")

The Zakhar service provides access to the robot status and the CAN bus network.

The service prints information onto an ssd1306-based 128x32 OLED display connected to `/dev/i2c-1`:

<img src="screen1.jpg" width="300">
<img src="screen2.jpg" width="300">
<img src="screen3.jpg" width="300">

The service publishes status information and incoming CAN messages to [ZeroMQ](https://zeromq.org/) subscribers. It also provides a ZeroMQ service to send CAN messages to the CAN bus.

The service allows all TCP connections including connections from external machines. See [brain_pycore](https://github.com/Zakhar-the-Robot/brain_pycore) for compatible subscriber and client implementation classes.

<img src="structure.svg" width="800">

## Requirements

### OS and Hardware
The service is supposed to be run on Raspberry Pi 4 with a Debian-like Linux (e.g. Raspberry OS). The OS should be initialized with the init script:

```bash
sudo bash scripts/init/init.sh
```

The script will create a zakhar directory in the system root and prepare the robot environment.

The service expects to see an I2C 128x32 display with the ssd1306 controller. E.g. [this one](https://www.adafruit.com/product/931). The display should be connected to `/dev/i2c-1`.

### Python

The service is written in python 3, so it requires Python > 3.5

The service requires several python packages:

- [brain_pycore](https://github.com/Zakhar-the-Robot/brain_pycore)
- ifcfg
- pyzmq
- luma
- Pillow

You can install the last four packages using pip and pypi. `brain_core` should be installed from the repository:

```python
pip install git+https://github.com/Zakhar-the-Robot/brain_pycore
```

## Installation

To install the service run the installation script as root:

```bash
sudo bash scripts/service_install.sh
```

## Connections

| Type                           | Port | Topic    |
|--------------------------------|------|----------|
|Robot status **publisher**      | 5557 | `status` |
|CAN received msgs **publisher** | 5556 | `can_rcv`|
|CAN send message **server**     | 5566 | n/a      |
