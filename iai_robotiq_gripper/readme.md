# udev Rules for Robotiq Grippers (Dual Setup)

## Using udev Rules (Recommended)


Open a new rules file:

```bash
sudo nano /etc/udev/rules.d/99-robotiq.rules
```

Paste the following lines into the file:

```bash
KERNEL=="ttyACM*", MODE="0666", GROUP="dialout"
KERNEL=="ttyUSB*", MODE="0666", GROUP="dialout"
```
Apply the changes:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```


