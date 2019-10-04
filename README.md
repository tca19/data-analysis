# data-analysis

## Installation
Update the `pip3` tool :
```
sudo pip3 install --upgrade pip --proxy=https://cache.univ-st-etienne.fr:3128
```

Install the required Python3 packages :
```
sudo pip3 install --upgrade ipython numpy pandas matplotlib scipy scikit-learn jupyter --proxy=https://cache.univ-st-etienne.fr:3128
```

Install TK for Python 3 (used by Matplotlib) :
```
sudo apt install python3-tk
```

If you had installed the packages with something else than pip3 (like Anaconda),
make sure your packages meet these requirements :

  * ipython (7.8+)
  * numpy (1.17+)
  * pandas (0.25+)
  * matplotlib (3.1+)
  * scipy (1.3.1+)
  * scikit-learn (0.21+)
  * jupyter

## Instructions

In a terminal, type:

```bash
$ git clone https://github.com/tca19/data-analysis.git
$ cd data-analysis/
$ jupyter notebook
```

Your web browser should open. Select the corresponding session folder and
complete the .ipynb file.
