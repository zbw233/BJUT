## README

### Introduction
gem5_utils is a single [Python3](http://www.python.org/) script to automate your daily tasks during [gem5](http://www.gem5.org/) related development and/or research, including running experiments, collecting configurations and statistics from experiment runs, and exporting experiment results as CSV files and figures.

### Prerequisites
Below is the packages required to install on Ubuntu Linux 15.10. Other environments could be configured in a similar way.

`sudo apt-get install python3-pip python3-matplotlib python3-pandas python3-seaborn`

`pip3 install objectpath pyparsing pytz` 

### Usage
`gem5_utils.py` is the only Python3 script where gem5_utils resides.

See `test_gem5_utils.py` and the `test_data` folder for example usage. You can setup parameters accordingly, then run `./test_gem5_utils.py` in the command line.

### Contact the Author
Please reports any bugs and problems of gem5_utils to min.cai.china@bjut.edu.cn.