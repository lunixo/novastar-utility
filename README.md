# Brightness control and test utility for Novastar MCTRL300

With this command line tool you can test a Novastar MCTRL300 and control the brightness.

### Requirements 
- python3
- pyserial 

### Installation
```console
./install.sh
```

## Features

### Set the brightness (0-255)
```console
novastar --brightness 120
```

### Turn off
```console
novastar --brightness 0
```

### Show test patterns (red,green,blue,white,slash,vertical,horizontal,grayscale)
```console
novastar --test horizontal
novastar --test slash
novastar --test grayscale
```

### Hide test pattern
```console
novastar --test normal
```

## License

- This project is licensed under the [GNU General Public License v3.0](LICENSE)
- This project uses GPL 3 licensed code from https://github.com/dietervansteenwegen/Novastar_MCTRL300_basic_controller 

## Acknowledgments
- Thanks to Dieter Vansteenwegen https://github.com/dietervansteenwegen and Bitfocus AS https://github.com/bitfocus for their Github contributions. Their code has been incredibly helpful in the development of this utility.
