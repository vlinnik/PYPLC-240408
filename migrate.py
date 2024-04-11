from pyplc.pou import POU
#make backup for transfering to new plc
def backup():
    from pyplc.pou import POU
    dump = { }
    for so in POU.__persistable__: 
        dump[so.id] = so.__dump__(so.__persistent__)
    with open('dump.json','w+') as f: 
        f.write(str(dump))
def restore():
    #now copy dump.json and restore state from pyplc cli
    with open('dump.json','r') as f: 
        rdump = eval(f.read())
    for so in POU.__persistable__: 
        if so.id in rdump:
            so.__restore__(rdump[so.id])
        else:
            print(so.id,' not found')