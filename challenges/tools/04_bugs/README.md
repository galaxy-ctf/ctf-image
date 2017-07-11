---
title: Bugs
category: Introductory Problems, Tool Development
shed: true

---

Have them look at the bug report / stack trace for the flag

```xml
<?xml version="1.0"?>
<tool id="gccctf.04" name="Bugs" version="1.0">
  <command detect_errors="aggressive">
  python tool.py
  </command>
  <inputs>
  </inputs>
  <outputs>
  </outputs>
  <help>
  </help>
  <citations/>
</tool>
```

```python
#!/usr/bin/env python
import argparse
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

def e():
    raise Exception("")

def d(a):
    return e()

def c(arg=1):
    return d("gccctf{bugs_everywhere}")

def b(z, q=43):
    return c()

def a():
    return b(3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    args = parser.parse_args()

    a()
```
