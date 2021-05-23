Requires python 3.6+.

You may need to [install graphviz on your system](https://pygraphviz.github.io/documentation/stable/install.html#recommended):

```
$ sudo apt-get install graphviz graphviz-dev
```

Install via

```
$ pip install -r requirements.txt
```

Edit mentor history in `sample_history.py`.

History is saved as a dictionary that maps names -> team history. Team history is a list of lists, where each element of the outer list is a "moment" in time. For example,

```
sample = {
    "Brian": [[1257], [2791], [333]],
    "Justin": [[2791], [340], [340, 5254], [5254]],
}
```

This shows that Justin was on only 2791 at one point, then only 340, then both 340 and 5254, then only 5254. It also shows that Brian was only on 1257, then only on 2791, then only on 333.

Run via

```
$ python sample_save.py
```

There will be images saved in `out/`.
