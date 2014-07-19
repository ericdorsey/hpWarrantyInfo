***7/19/2014*** Of note, this is likely not even working anymore, this was code I wrote specifically for pulling out useful information from the HP site for documentation during a project, but keeping it for legacy demonstration / examples.

### mechanizeHP.py

**Description:**
Given serial and product numbers of HP devices, outputs a CSV of warranty expiration dates. Results are created in:
/output/results.csv

**Requirements:**
Python 2.7

**Directions:**
Place serial number and product number, one per line seperated by a comma with no spaces, of HP devices in a file called hpinput.txt in same directory as mechanizeHP.py, for example:

`ABC12345A0,AB012AB
ZXV12345B2,GH123ZZ`

**Limitations:**
Only tested in OSX. Changes to the HP warranty site will, of course, break the script

