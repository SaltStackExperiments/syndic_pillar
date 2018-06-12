# RSS Beacons

This repo contains a custom external pillar for use with [SaltStack](https://saltstack.com/). 

Syndics [See docs here](https://docs.saltstack.com/en/latest/topics/topology/syndic.html) will have at least one "master of masters" with multiple "syndic masters" reporting to it. The Syndic masters may have salt-minion processes running on them. These salt-minion processes may or may not have the syndic master in their list masters. Rather, they may report up to the "Master of Masters" and get all states, pillar data, etc from there.

Question: What happens when you need the syndic master to run an orchestration state, reactor, runner, or other action using pillar data assigned to the minion running on that same system?  The syndic master will not see that data by default.

This external pillar module loads this data and makes it available to the syndic master, and optionally any minion the reports to it.

## Requirements


## How to Use it

- Add gitfs to Salt see [this link](https://docs.saltstack.com/en/develop/topics/tutorials/gitfs.html) for a walkthrough on doing this

```
# /etc/salt/master.d/fileserver.conf
fileserver_backend:
  - roots
  - git
```

- Add this repo to your gitfs repos

```
# /etc/salt/master.d/gitfs.conf
gitfs_remotes:
  - https://github.com/SaltStackExperiments/syndic_pillar.git
```

- Add a configuration for this pillar to /etc/salt/minion.d/ext_pillar.conf
- _Note_: masters have a special <master_id>_master minion that can be used to target pillar data.

```
ext_pillar:
  #- cmd_yaml:
  #  - if [ "%s" == "sm0_master" ]; then salt-call pillar.items --out=json | jq ".local" ; fi
  - syndic_pillar:
      target_minions:
        - syndic_master*
      pillar_path: syndic:name
      key: boom
```
