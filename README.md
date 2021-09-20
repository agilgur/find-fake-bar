### Description

The algorithm to determine the fake bar is a two step process.
First, nine bars are randomly split into groups of three (total of three groups).
By weighing the two groups at the same time against each other,
it's determined which group contains the fake bar. If the groups are equal in
weight, then the remaining group contains the fake bar. Second and last,
the group that has the fake bar is split into tree bars, two of which are
weighed against each other. The scales will show which one is lighter, and if they
are equal, the remaining bar is fake.

### Installation

Install python packages necessary to run the program:

```
pip3 install -r requirements.txt
```
Install chromedriver (example shown for mac):

```
brew install chromedriver
```

### Run

```
python3 fakebar.py
```

### Sample output

```
WIN !!! Fake bar is 6
Weighing [1] : [0,1,2] = [3,4,5]
Weighing [2] : [6] < [7]
```

###
