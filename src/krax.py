# This is project entry point.
from pyplc.config import *
from concrete import Motor,Lock,Container,Dosator,Weight,Readiness,Loaded,Manager,MSGate,Mixer,Factory,Accelerator
from concrete.vibrator import UnloadHelper,Vibrator
from concrete.imitation import iMOTOR,iGATE,iVALVE,iWEIGHT
from board import version,name

print(f'Starting up {name} {version}')
instances = [] #here should be listed user defined programs

factory_1 = Factory()

cement_m_1 = Weight(mmax=1500, raw=plc.CEMENT_M_1)
silage_1 = Container(m=lambda: cement_m_1.m, out = plc.CEMENT_OPEN_1, closed = plc.CEMENT_CLOSED_1, lock = Lock( key = ~plc.DCEMENT_CLOSED_1) ) 
dcement_1 = Dosator(m=lambda: cement_m_1.m, closed=plc.DCEMENT_CLOSED_1, out=plc.DCEMENT_OPEN_1,
                    containers=[silage_1], lock=Lock(key=lambda: not hw.CEMENT_CLOSED_1 or not hw.MIXER_ISON_1), unloadT=0)
dc_vibrator_1 = UnloadHelper( dosator=dcement_1, weight=cement_m_1,point = 100,q = plc.DC_VIBRATOR_ON_1 )
silage_1.bind( 'busy', plc.AERATOR_ON_1 )

water_m_1 = Weight(mmax=500, raw=plc.WATER_M_1)
water_1 = Container(m=lambda: water_m_1.m, out = plc.WATER_OPEN_1, closed = plc.WATER_CLOSED_1, lock = Lock( key = ~plc.DWATER_CLOSED_1) ) 
dwater_1 = Dosator(m=lambda: water_m_1.m, closed=plc.DWATER_CLOSED_1, out=plc.DWATER_OPEN_1,
                    containers=[water_1], lock=Lock(key=~plc.WATER_CLOSED_1), unloadT=0)

additions_m_1 = Weight(mmax=100, raw=plc.ADDITIONS_M_1)
addition_1 = Container(m=lambda: additions_m_1.m, out = plc.APUMP_ON_1, closed = ~plc.APUMP_ON_1, lock = Lock( key = lambda: hw.APUMP_ON_2 or not hw.DADDITIONS_CLOSED_1) ) 
addition_2 = Container(m=lambda: additions_m_1.m, out = plc.APUMP_ON_2, closed = ~plc.APUMP_ON_2, lock = Lock( key = lambda: hw.APUMP_ON_1 or not hw.DADDITIONS_CLOSED_1) ) 
dadditions_1 = Dosator(m=lambda: additions_m_1.m, closed=plc.DADDITIONS_CLOSED_1, out=plc.DADDITIONS_OPEN_1,containers=[addition_1,addition_2], lock=Lock(key=lambda: hw.APUMP_ON_1 or hw.APUMP_ON_2), unloadT=0)

fillers_m_1  = Weight(mmax=2000, raw=plc.FILLERS_M_1)
accel_1 = Accelerator(outs=[plc.FILLER_OPEN_1, plc.FILLER_OPEN_2], sts=[
                      plc.FILLER_CLOSED_1, plc.FILLER_CLOSED_2] )
filler_1 = Container(m=lambda: fillers_m_1.m, lock=Lock(key=lambda: not hw.DFILLERS_CLOSED_1),
                     closed=lambda: accel_1.closed, max_sp = 2000)
accel_1.link(filler_1)
filler_2 = Container(m=lambda: fillers_m_1.m, lock=Lock(key=lambda: not hw.DFILLERS_CLOSED_1 or not hw.FILLER_CLOSED_1),
                    max_sp = 2000)
dfillers_1 = Dosator(m=lambda: fillers_m_1.m, out = plc.DFILLERS_OPEN_1, closed = plc.DFILLERS_CLOSED_1, 
                     containers=[filler_1,filler_2], lock = Lock( key = lambda: not hw.FILLER_CLOSED_1 or not hw.FILLER_CLOSED_2 or not hw.MIXER_ISON_1 ) ) 
vibrator_1 = Vibrator( containers=[plc.FILLER_OPEN_1], weight=fillers_m_1, q = plc.VIBRATOR_ON_1 )
vibrator_2 = Vibrator( containers=[plc.FILLER_OPEN_2], weight=fillers_m_1, q = plc.VIBRATOR_ON_2 )
df_vibrator_1 = UnloadHelper( dosator=dfillers_1, weight=fillers_m_1,point = 100,q = plc.DF_VIBRATOR_ON_1 )

fillers_m_2  = Weight(mmax=2000, raw=plc.FILLERS_M_2)
filler_3 = Container(m=lambda: fillers_m_2.m, out = plc.FILLER_OPEN_3, closed = plc.FILLER_CLOSED_3, lock = Lock( key = ~plc.DFILLERS_CLOSED_2) ) 
dfillers_2 = Dosator(m=lambda: fillers_m_2.m, out = plc.DFILLERS_OPEN_2, closed = plc.DFILLERS_CLOSED_2, 
                     containers=[filler_3],lock = Lock( key = lambda: not hw.FILLER_CLOSED_3 or not hw.MIXER_ISON_1) ) 
vibrator_3 = Vibrator( containers=[plc.FILLER_OPEN_3], weight=fillers_m_2, q = plc.VIBRATOR_ON_3 )
df_vibrator_2 = UnloadHelper( dosator=dfillers_2, weight=fillers_m_2,point = 100,q = plc.DF_VIBRATOR_ON_2 )

fillers_m_3  = Weight(mmax=2000, raw=plc.FILLERS_M_3)
filler_4 = Container(m=lambda: fillers_m_3.m, out = plc.FILLER_OPEN_4, closed = plc.FILLER_CLOSED_4, lock = Lock( key = ~plc.DFILLERS_CLOSED_3) ) 
dfillers_3 = Dosator(m=lambda: fillers_m_3.m, out = plc.DFILLERS_OPEN_3, closed = plc.DFILLERS_CLOSED_3, 
                     containers=[filler_4], lock = Lock( key = lambda: not hw.FILLER_CLOSED_4 or not hw.MIXER_ISON_1 ) ) 
vibrator_4 = Vibrator( containers=[plc.FILLER_OPEN_4], weight=fillers_m_3, q = plc.VIBRATOR_ON_4 )
df_vibrator_3 = UnloadHelper( dosator=dfillers_3, weight=fillers_m_3,point = 100,q = plc.DF_VIBRATOR_ON_3 )

# смеситель №1
motor_1 = Motor(on=plc.MIXER_ON_1, off=plc.MIXER_OFF_1, ison=plc.MIXER_ISON_1)
gate_1 = MSGate(closed=plc.MIXER_CLOSED_1, open=plc.MIXER_OPEN_1,opened=plc.MIXER_OPENED_1)
mixer_1 = Mixer(motor=motor_1, gate=gate_1,  flows=[s.q for s in [silage_1,water_1,addition_1,addition_2,filler_1,filler_2,filler_3,filler_4]],use_ack=False)

ready_1 = Readiness( [ mixer_1,dcement_1,dwater_1,dadditions_1,dfillers_1,dfillers_2,dfillers_3 ] )
loaded_1 = Loaded([dcement_1,dwater_1,dadditions_1,dfillers_1,dfillers_2,dfillers_3] )
manager_1 = Manager(collected=ready_1, loaded=loaded_1, mixer=mixer_1, dosators=[dcement_1,dwater_1,dadditions_1,dfillers_1,dfillers_2,dfillers_3])

factory_1.on_mode = [x.switch_mode for x in [dcement_1,dwater_1,dadditions_1,dfillers_1,dfillers_2,dfillers_3 ]]
factory_1.on_emergency = [x.emergency for x in [manager_1,dcement_1,dwater_1,dadditions_1,dfillers_1,dfillers_2,dfillers_3, mixer_1, gate_1]] 

def running():
    board.run = not board.run

instances+=[running,factory_1,cement_m_1,silage_1,dcement_1,dc_vibrator_1,water_m_1,water_1,dwater_1, additions_m_1, addition_1,addition_2, dadditions_1, 
            fillers_m_1, filler_1, dfillers_1, vibrator_1,vibrator_2,df_vibrator_1,
            fillers_m_2, filler_3, dfillers_2, vibrator_3,df_vibrator_2,
            fillers_m_3, filler_4, dfillers_3, vibrator_4,df_vibrator_3,
            motor_1,gate_1,mixer_1,ready_1,loaded_1,manager_1,accel_1]

igate_1 = iGATE( simple=True, open = plc.MIXER_OPEN_1, closed = plc.MIXER_CLOSED_1,opened = plc.MIXER_OPENED_1 )
imotor_1 = iMOTOR(on = plc.MIXER_ON_1,off=plc.MIXER_OFF_1,ison=plc.MIXER_ISON_1 )
icement_m_1 = iWEIGHT( speed=100, loading = ~plc.CEMENT_CLOSED_1,unloading=~plc.DCEMENT_CLOSED_1,q = plc.CEMENT_M_1)
isilage_1 = iVALVE(open=plc.CEMENT_OPEN_1, closed=plc.CEMENT_CLOSED_1 )
idcement_1 = iVALVE( open = plc.DCEMENT_OPEN_1, closed = plc.DCEMENT_CLOSED_1 )

iwater_m_1 = iWEIGHT( speed=100, loading = ~plc.WATER_CLOSED_1,unloading=~plc.DWATER_CLOSED_1,q = plc.WATER_M_1)
iwater_1 = iVALVE(open=plc.WATER_OPEN_1, closed=plc.WATER_CLOSED_1 )
idwater_1 = iVALVE( open = plc.DWATER_OPEN_1, closed = plc.DWATER_CLOSED_1 )

iadditions_m_1 = iWEIGHT( speed=100,loading = lambda: hw.APUMP_ON_1 or hw.APUMP_ON_2, unloading = plc.DADDITIONS_OPEN_1, q = plc.ADDITIONS_M_1)
iaddition_1 = iMOTOR(simple=True,on = plc.APUMP_ON_1, ison=plc.APUMP_ISON_1)
iaddition_2 = iMOTOR(simple=True,on = plc.APUMP_ON_2, ison=plc.APUMP_ISON_2)
idadditions_1 = iVALVE( open = plc.DADDITIONS_OPEN_1, closed = plc.DADDITIONS_CLOSED_1 )

ifillers_m_1 = iWEIGHT( speed=100,loading = lambda: hw.FILLER_OPEN_1 or hw.FILLER_OPEN_2, unloading = plc.DFILLERS_OPEN_1, q = plc.FILLERS_M_1 )
ifiller_1 = iVALVE( open=plc.FILLER_OPEN_1,closed = plc.FILLER_CLOSED_1 )
ifiller_2 = iVALVE( open=plc.FILLER_OPEN_2,closed = plc.FILLER_CLOSED_2 )
idfillers_1 = iVALVE(open=plc.DFILLERS_OPEN_1,closed=plc.DFILLERS_CLOSED_1)
ifillers_m_2 = iWEIGHT( speed=100,loading = lambda: hw.FILLER_OPEN_3, unloading = plc.DFILLERS_OPEN_2, q = plc.FILLERS_M_2 )
ifiller_3 = iVALVE( open=plc.FILLER_OPEN_3,closed = plc.FILLER_CLOSED_3 )
idfillers_2 = iVALVE(open=plc.DFILLERS_OPEN_2,closed=plc.DFILLERS_CLOSED_2)
ifillers_m_3 = iWEIGHT( speed=100,loading = lambda: hw.FILLER_OPEN_4, unloading = plc.DFILLERS_OPEN_3, q = plc.FILLERS_M_3 )
ifiller_4 = iVALVE( open=plc.FILLER_OPEN_4,closed = plc.FILLER_CLOSED_4 )
idfillers_3 = iVALVE(open=plc.DFILLERS_OPEN_3,closed=plc.DFILLERS_CLOSED_3)

imitations = [igate_1,imotor_1,icement_m_1,isilage_1, idcement_1, iwater_m_1,iwater_1,idwater_1,iadditions_m_1,iaddition_1,iaddition_2,idadditions_1,ifillers_m_1,ifiller_1,ifiller_2,idfillers_1,
              ifillers_m_2,ifiller_3,idfillers_2, ifillers_m_3,ifiller_4,idfillers_3]
instances += imitations 

try:
    from machine import reset_cause,WDT
    print(f'------------причина перезапуска #{reset_cause()}------------')
    with open('krax.log','a+t') as log:
        log.write(f'[{manager_1.NOW_MS}] причина перезапуска - {reset_cause()}\n')
    wdt = WDT(timeout=2000)
    instances+=[wdt.feed]
except Exception as e:
    print(e)

try:
    plc.run(instances=instances,ctx=globals())
except Exception as e:
    with open('krax.log','a+t') as log:
        log.write(f'[{mixer_1.NOW_MS}] ошибка в программе - {e}\n')