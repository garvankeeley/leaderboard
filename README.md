Install the package!

```
pip install stumbler_leaderboard
```

Edit the JSON example in example_db.json and copy it to one of these
locations.

```
~/.stumbler_leaderboard/db.json
/etc/mozilla/stumbler_leaderboard/db.json
```

The db.json file in the home directory will be loaded in order and
short circuit after a configuration file is found.


Run the tests!

```
cd leaderboard_backend
nosetests
```


