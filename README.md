# Small Color Work (a luminance and WCAG demonstration)

This repository contains a python script to check the luminance of a color ( `luminance.py` ) and an interactive HTML page to check the WCAG compliance of a color ( `index.html` ).


## Context

I was curious about the number of colors that are compliant with the WCAG 2.0 (Web Content Accessibility Guidelines) given a background color and a set a foreground color.

I did it in a few hours, so it's not perfect, there are probably some errors, but it gave me information that I was looking for.

I'm likely to improve it in the future. Feel free to contribute or request any feature or information.

## Usage

### Bash

```bash
./run.sh
```

Will run the python script with different values for the step and the colors to test.

### Python

```bash
python luminance.py [-h] [-s STEP] [-c COLORS]
```

```plain

optional arguments:
  -h, --help          show this help message and exit
  -s, --step          Step (default: 8)
  -c, --colors        Foreground colors tested (default: base)
  (Allowed values: base (black,white) , primary (red,green,blue), secondary (yellow,cyan,magenta), tertiary (orange,green,blue), all (red,green,blue,yellow,cyan,magenta,orange,green,blue))
```

## Results

Running the script `luminance.py` with the default values:
(checking each color from 0 to 255, with a step of 1 as background color and white or black as foreground color)

```plain
Min contrast: 4.5825758149421025
Max contrast: 21.0
Number of colors that are compliant with level AAA: 10294771
Number of colors that are compliant with level AA: 6482445
Number of colors that are not compliant: 0
Number of colors with the best color being white: 5966007
Number of colors with the best color being black: 10811209
Number of colors tested: 16777216 / 16777216
```
