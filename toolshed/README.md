# CTF Toolshed

This code will:

1. setup a tool shed from scratch,
2. fill it with all challenges in `../challenges/completed`
3. create a `ctf_tools.yml` with list of (all revisions of) all tools in it to use for installation to galaxy

Run the code:

```
python3 setup_toolshed.py -g <galaxy_root> -c <start|stop|setup|make_yaml>
```

WARNING: this will destroy any toolshed already present in `galaxy_root` and start fresh

stop a running toolshed from previous run:

```
# passing -s option only stops a previously started toolshed instance
python3 setup_toolshed.py -g <galaxy_root> -c stop
```

only make a `tools.yml` file from running toolshed:

```
python3 setup_toolshed.py -g <galaxy_root> -c make_yaml
```

only start the existing toolshed:

```
python3 setup_toolshed.py -g <galaxy_root> -c start
```
