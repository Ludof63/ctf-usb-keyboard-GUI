# ctf-usb-keyboard-gui
A GUI for ctf-usb-keyboard-parser https://github.com/TeamRocketIst/ctf-usb-keyboard-parser

It launches a GUI that allows you to browse in time the sequence of keyboard input.

### Usage

Arguments can be passed to the command line as shown in the following example:

- -f <path to the file> (instruction to generate the file required from the pcap in the following section) [mandatory]
- -o <path to output file> where to save a sequential history of the keys pressed [optional]

```bash
$ python usbkeyboard.py -f <file> -o <output file>
```

### Extract file from pcap (might not work for every pcap)
```bash
$ tshark -r ./usb.pcap -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata > usbPcapData
```

Some versions of tshark don't add ":" between each byte like this:

```bash
$ tshark -r ./usb.pcap -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata
0000240000000000
0000000000000000
...
```

If this happens you can use sed to add them like this:

```bash
$ tshark -r ./usb.pcap -Y 'usb.capdata && usb.data_len == 8' -T fields -e usb.capdata | sed 's/../:&/g2'
00:00:24:00:00:00:00:00
00:00:00:00:00:00:00:00
...
```

### Hid usage tables
The key mapping is based on https://usb.org/sites/default/files/documents/hut1_12v2.pdf (table 12, page 53)
if for some reason the link is dead you may find a new one at https://www.usb.org/document-library/hid-usage-tables-112
