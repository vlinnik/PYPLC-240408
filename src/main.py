from machine import Pin
import webrepl 

# usr = Pin(36,Pin.IN)
run = Pin(39,Pin.IN)

if run.value()==0:
    print('KRAX.MAIN: RUN switch is ON. Loading TASK module...')
    #begin of eth initialization
    # import network
    # from machine import Pin
    # try:
    #     eth = network.LAN(mdc=Pin(23),mdio=Pin(18),power=Pin(4),id=None,phy_addr=1,phy_type=network.PHY_LAN8720)
    #     eth.active(True)
    # except:
    #     pass
    #end of eth inititalization
    try:
        import task
    except Exception as e:
        from kx.config import kx_init,kx_term
        print('KRAX.MAIN: Exception in TASK. SafeMode!',e)
        kx_term( )
        plc,hw = kx_init()

webrepl.stop()
webrepl.start()