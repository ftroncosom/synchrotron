#!/usr/bin/env python
import json
import sys

f = file("image.boot.html")
template = f.read()
f.close()

mods = {}
defs = []

def loadModspec(name):
    f = file(name + ".modspec.js")
    metadata = json.load(f)
    f.close()
    f = file(name + ".js")
    body = f.read()
    f.close()
    metadata["bodyText"] = body

    mods[metadata["name"]] = metadata

    d = dict(metadata)
    d["bodyText"] = d["bodyText"] \
        .replace('</script>', '</scr"+"ipt>') # skode. Should deal with this case-insensitively
    d["objectType"] = "moduleDefinition"
    defs.append(d)

def split(what, marker):
    (prefix, suffix) = what.split(marker, 1)
    return (prefix + marker, suffix)

def replaceMarker(marker, value):
    global template
    (prefix, template) = split(template, marker)
    print prefix + '\n' + value

goal = sys.argv[1]
for name in sys.argv[2:]:
    loadModspec(name)
replaceMarker('__$__exported_repo__$__', '(' + json.dumps({}, indent = 2) + ')')
replaceMarker('__$__new_instances__$__', '(' + json.dumps(defs, indent = 2) + ')')
replaceMarker('__$__goal__$__', '(' + json.dumps(goal, indent = 2) + ')')
replaceMarker('__$__boot_script__$__', mods['net.lshift.synchrotron.boot']['bodyText'])
print template