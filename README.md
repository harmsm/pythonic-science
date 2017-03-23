# pythonic-science
Materials for Scientific Programming in Python Course at the UO

## Set up the computing environment
 * Install the scientific python computing stack. If you do not have anything
   installed yet, the best starting point is [anaconda](https://www.continuum.io/downloads).  This will auto-magically install everything. See below if you want to 
   do a manual install. 
 * Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). 
 * Use `git` to clone the pythonic-science repository onto a convenient place
   on your computer:
    ```bash
        git clone https://github.com/harmsm/pythonic-science.git
    ```
 * Fire up `jupyter` in the `pythonic-science` directory. (You'll have to 
   specify the start up folder as described [here](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html)).

 * Open `Test Notebook.ipynb` by double-clicking on it in the jupyter window.
 * Follow the directions in that notebook to make sure everything is installed
   correctly.  It will print out missing packages if it cannot find them. 

#### Manual install

The instructions below will work for Mac or Linux.  If you're on Windows, I
**strongly** recommend Anaconda. 

You'll need:
 * [python3.x](https://www.python.org/downloads/)
 * [jupyter](https://jupyter.org/install.html)
 * [numpy and scipy](https://www.scipy.org/install.html)
 * [matplotlib](http://matplotlib.org/users/installing.html)
 * [pandas](http://pandas.pydata.org/pandas-docs/stable/install.html)
 * [scikit-learn](http://scikit-learn.org/stable/install.html)

After you've installed python3, you can use `pip3` to install everything with
a single command.

```bash
    pip3 --user install numpy scipy matplotlib jupyter pandas sklearn
```

## Syllabus
After you have cloned the `pythonic-science` repo, go to 
`pythonic-science/docs/build/index.html` for the syllabus and links to all 
course documents.
