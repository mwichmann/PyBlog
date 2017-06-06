import yaml
import os

blankapp = """
    %s:
        url: ''
        sha256: ''
        releasedate: ''
        version: ''
        name: ''
"""

y = yaml.load(blankapp % "test")

#with open(os.path.expanduser('~' + '/.version_cache.yml'), 'w') as f:
with open('.version_cache.yml', 'w') as f:
    f.write(yaml.dump(y, default_flow_style=False))



#with open("config.yml", 'r') as ymlfile:
#    cfg = yaml.safe_load(ymlfile)
#
#for section in cfg:
#    print(section)
#    print(cfg[section])
#print(cfg['mysql'])
#print(cfg['other'])
