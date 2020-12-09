from pyartnet import ArtNetNode
import asyncio
import time

#dit stukje is om de dmx nodes aan te geven 
node0 = ArtNetNode('2.0.0.2')
node1= ArtNetNode('2.0.0.2')
node2= ArtNetNode('2.0.0.2')
node3= ArtNetNode('2.0.0.2')
universe0 = node0.add_universe(0)
universe1 = node1.add_universe(1)
universe2 = node2.add_universe(2)
universe3 = node3.add_universe(3)

#hier zorgen we dat alle leds een naam krijgen en geadreseerd zijn binnen hun eigen universe.

#strip a 
fixturea1 = universe0.add_channel(start=1, width=6)
fixturea2 = universe0.add_channel(start=7, width=6)
fixturea3 = universe0.add_channel(start=13, width=6)
fixturea4 = universe0.add_channel(start=19, width=6)
fixturea5 = universe0.add_channel(start=25, width=6)
fixturea6 = universe0.add_channel(start=31, width=6)
fixturea7 = universe0.add_channel(start=37, width=6)
fixturea8 = universe0.add_channel(start=43, width=6)
fixturea9 = universe0.add_channel(start=49, width=6)
fixturea10 = universe0.add_channel(start=55, width=6)
fixturea11 = universe0.add_channel(start=61, width=6)
fixturea12 = universe0.add_channel(start=67, width=6)
fixturea13 = universe0.add_channel(start=73, width=6)
fixturea14 = universe0.add_channel(start=79, width=6)
fixturea15 = universe0.add_channel(start=85, width=6)
fixturea16 = universe0.add_channel(start=91, width=6)
fixturea17 = universe0.add_channel(start=97, width=6)
fixturea18 = universe0.add_channel(start=103, width=6)
fixturea19 = universe0.add_channel(start=109, width=6)
fixturea20 = universe0.add_channel(start=115, width=6)
fixturea21 = universe0.add_channel(start=121, width=6)
fixturea22 = universe0.add_channel(start=127, width=6)
fixturea23 = universe0.add_channel(start=133, width=6)
fixturea24 = universe0.add_channel(start=139, width=6)
fixturea25 = universe0.add_channel(start=145, width=6)
fixturea26 = universe0.add_channel(start=151, width=6)
fixturea27 = universe0.add_channel(start=157, width=6)
fixturea28 = universe0.add_channel(start=163  width=6)
fixturea29 = universe0.add_channel(start=169, width=6)
fixturea30 = universe0.add_channel(start=175, width=6)
fixturea31 = universe0.add_channel(start=181, width=6)
fixturea32 = universe0.add_channel(start=187, width=6)
fixturea33 = universe0.add_channel(start=193, width=6)
fixturea34 = universe0.add_channel(start=199, width=6)
fixturea35 = universe0.add_channel(start=205, width=6)
fixturea36 = universe0.add_channel(start=211, width=6)
fixturea37 = universe0.add_channel(start=217, width=6)
fixturea38 = universe0.add_channel(start=223, width=6)
fixturea39 = universe0.add_channel(start=229, width=6)
fixturea40 = universe0.add_channel(start=235, width=6)
fixturea41 = universe0.add_channel(start=241, width=6)
fixturea42 = universe0.add_channel(start=247, width=6)
fixturea43 = universe0.add_channel(start=253, width=6)
fixturea44 = universe0.add_channel(start=259, width=6)
fixturea45 = universe0.add_channel(start=265, width=6)
fixturea46 = universe0.add_channel(start=271, width=6)
fixturea47 = universe0.add_channel(start=277, width=6)
fixturea48 = universe0.add_channel(start=283, width=6)

# strip b
fixtureb1 = universe1.add_channel(start=61, width=6)
fixtureb2 = universe1.add_channel(start=55, width=6)
fixtureb3 = universe1.add_channel(start=49, width=6)
fixtureb4 = universe1.add_channel(start=43, width=6)
fixtureb5 = universe1.add_channel(start=37, width=6)
fixtureb6 = universe1.add_channel(start=31, width=6)
fixtureb7 = universe1.add_channel(start=25, width=6)
fixtureb8 = universe1.add_channel(start=19, width=6)
fixtureb9 = universe1.add_channel(start=13, width=6)
fixtureb10 = universe1.add_channel(start=7, width=6)
fixtureb11 = universe1.add_channel(start=1, width=6)
fixtureb12 = universe0.add_channel(start=505, width=6)
fixtureb13 = universe0.add_channel(start=499, width=6)
fixtureb14 = universe0.add_channel(start=493, width=6)
fixtureb15 = universe0.add_channel(start=487, width=6)
fixtureb16 = universe0.add_channel(start=481, width=6)
fixtureb17 = universe0.add_channel(start=475, width=6)
fixtureb18 = universe0.add_channel(start=469, width=6)
fixtureb19 = universe0.add_channel(start=463, width=6)
fixtureb20 = universe0.add_channel(start=457, width=6)
fixtureb21 = universe0.add_channel(start=451, width=6)
fixtureb22 = universe0.add_channel(start=445, width=6)
fixtureb23 = universe0.add_channel(start=439, width=6)
fixtureb24 = universe0.add_channel(start=433, width=6)
fixtureb25 = universe0.add_channel(start=427, width=6)
fixtureb26 = universe0.add_channel(start=421, width=6)
fixtureb27 = universe0.add_channel(start=415, width=6)
fixtureb28 = universe0.add_channel(start=409  width=6)
fixtureb29 = universe0.add_channel(start=403, width=6)
fixtureb30 = universe0.add_channel(start=397, width=6)
fixtureb31 = universe0.add_channel(start=391, width=6)
fixtureb32 = universe0.add_channel(start=385, width=6)
fixtureb33 = universe0.add_channel(start=379, width=6)
fixtureb34 = universe0.add_channel(start=373, width=6)
fixtureb35 = universe0.add_channel(start=367, width=6)
fixtureb36 = universe0.add_channel(start=361, width=6)
fixtureb37 = universe0.add_channel(start=355, width=6)
fixtureb38 = universe0.add_channel(start=349, width=6)
fixtureb39 = universe0.add_channel(start=343, width=6)
fixtureb40 = universe0.add_channel(start=337, width=6)
fixtureb41 = universe0.add_channel(start=331, width=6)
fixtureb42 = universe0.add_channel(start=325, width=6)
fixtureb43 = universe0.add_channel(start=319, width=6)
fixtureb44 = universe0.add_channel(start=313, width=6)
fixtureb45 = universe0.add_channel(start=307, width=6)
fixtureb46 = universe0.add_channel(start=301, width=6)
fixtureb47 = universe0.add_channel(start=295, width=6)
fixtureb48 = universe0.add_channel(start=289, width=6)

#strip c
fixturec1 = universe1.add_channel(start=67, width=6)
fixturec2 = universe1.add_channel(start=73, width=6)
fixturec3 = universe1.add_channel(start=79, width=6)
fixturec4 = universe1.add_channel(start=85, width=6)
fixturec5 = universe1.add_channel(start=91, width=6)
fixturec6 = universe1.add_channel(start=97, width=6)
fixturec7 = universe1.add_channel(start=103, width=6)
fixturec8 = universe1.add_channel(start=109, width=6)
fixturec9 = universe1.add_channel(start=115, width=6)
fixturec10 = universe1.add_channel(start=121, width=6)
fixturec11 = universe1.add_channel(start=127, width=6)
fixturec12 = universe1.add_channel(start=133, width=6)
fixturec13 = universe1.add_channel(start=139, width=6)
fixturec14 = universe1.add_channel(start=145, width=6)
fixturec15 = universe1.add_channel(start=151, width=6)
fixturec16 = universe1.add_channel(start=157, width=6)
fixturec17 = universe1.add_channel(start=163, width=6)
fixturec18 = universe1.add_channel(start=169, width=6)
fixturec19 = universe1.add_channel(start=175, width=6)
fixturec20 = universe1.add_channel(start=181, width=6)
fixturec21 = universe1.add_channel(start=187, width=6)
fixturec22 = universe1.add_channel(start=193, width=6)
fixturec23 = universe1.add_channel(start=199, width=6)
fixturec24 = universe1.add_channel(start=205, width=6)
fixturec25 = universe1.add_channel(start=211, width=6)
fixturec26 = universe1.add_channel(start=217, width=6)
fixturec27 = universe1.add_channel(start=223, width=6)
fixturec28 = universe1.add_channel(start=229  width=6)
fixturec29 = universe1.add_channel(start=235, width=6)
fixturec30 = universe1.add_channel(start=241, width=6)
fixturec31 = universe1.add_channel(start=247, width=6)
fixturec32 = universe1.add_channel(start=253, width=6)
fixturec33 = universe1.add_channel(start=259, width=6)
fixturec34 = universe1.add_channel(start=265, width=6)
fixturec35 = universe1.add_channel(start=271, width=6)
fixturec36 = universe1.add_channel(start=277, width=6)
fixturec37 = universe1.add_channel(start=283, width=6)
fixturec38 = universe1.add_channel(start=289, width=6)
fixturec39 = universe1.add_channel(start=295, width=6)
fixturec40 = universe1.add_channel(start=301, width=6)
fixturec41 = universe1.add_channel(start=307, width=6)
fixturec42 = universe1.add_channel(start=313, width=6)
fixturec43 = universe1.add_channel(start=319, width=6)
fixturec44 = universe1.add_channel(start=325, width=6)
fixturec45 = universe1.add_channel(start=331, width=6)
fixturec46 = universe1.add_channel(start=337, width=6)
fixturec47 = universe1.add_channel(start=343, width=6)
fixturec48 = universe1.add_channel(start=349, width=6)

#strip d 
fixtured1 = universe2.add_channel(start=1, width=6)
fixtured2 = universe2.add_channel(start=7, width=6)
fixtured3 = universe2.add_channel(start=13, width=6)
fixtured4 = universe2.add_channel(start=19, width=6)
fixtured5 = universe2.add_channel(start=25, width=6)
fixtured6 = universe2.add_channel(start=31, width=6)
fixtured7 = universe2.add_channel(start=37, width=6)
fixtured8 = universe2.add_channel(start=43, width=6)
fixtured9 = universe2.add_channel(start=49, width=6)
fixtured10 = universe2.add_channel(start=55, width=6)
fixtured11 = universe2.add_channel(start=61, width=6)
fixtured12 = universe2.add_channel(start=67, width=6)
fixtured13 = universe2.add_channel(start=73, width=6)
fixtured14 = universe2.add_channel(start=79, width=6)
fixtured15 = universe2.add_channel(start=85, width=6)
fixtured16 = universe2.add_channel(start=91, width=6)
fixtured17 = universe2.add_channel(start=97, width=6)
fixtured18 = universe2.add_channel(start=103, width=6)
fixtured19 = universe2.add_channel(start=109, width=6)
fixtured20 = universe2.add_channel(start=115, width=6)
fixtured21 = universe2.add_channel(start=121, width=6)
fixtured22 = universe2.add_channel(start=127, width=6)
fixtured23 = universe2.add_channel(start=133, width=6)
fixtured24 = universe2.add_channel(start=139, width=6)
fixtured25 = universe2.add_channel(start=145, width=6)
fixtured26 = universe2.add_channel(start=151, width=6)
fixtured27 = universe2.add_channel(start=157, width=6)
fixtured28 = universe2.add_channel(start=163  width=6)
fixtured29 = universe2.add_channel(start=169, width=6)
fixtured30 = universe2.add_channel(start=175, width=6)
fixtured31 = universe2.add_channel(start=181, width=6)
fixtured32 = universe2.add_channel(start=187, width=6)
fixtured33 = universe2.add_channel(start=193, width=6)
fixtured34 = universe2.add_channel(start=199, width=6)
fixtured35 = universe2.add_channel(start=205, width=6)
fixtured36 = universe2.add_channel(start=211, width=6)
fixtured37 = universe2.add_channel(start=217, width=6)
fixtured38 = universe2.add_channel(start=223, width=6)
fixtured39 = universe2.add_channel(start=229, width=6)
fixtured40 = universe2.add_channel(start=235, width=6)
fixtured41 = universe2.add_channel(start=241, width=6)
fixtured42 = universe2.add_channel(start=247, width=6)
fixtured43 = universe2.add_channel(start=253, width=6)
fixtured44 = universe2.add_channel(start=259, width=6)
fixtured45 = universe2.add_channel(start=265, width=6)
fixtured46 = universe2.add_channel(start=271, width=6)
fixtured47 = universe2.add_channel(start=277, width=6)
fixtured48 = universe2.add_channel(start=283, width=6)

# strip e
fixturee1 = universe3.add_channel(start=61, width=6)
fixturee2 = universe3.add_channel(start=55, width=6)
fixturee3 = universe3.add_channel(start=49, width=6)
fixturee4 = universe3.add_channel(start=43, width=6)
fixturee5 = universe3.add_channel(start=37, width=6)
fixturee6 = universe3.add_channel(start=31, width=6)
fixturee7 = universe3.add_channel(start=25, width=6)
fixturee8 = universe3.add_channel(start=19, width=6)
fixturee9 = universe3.add_channel(start=13, width=6)
fixturee10 = universe3.add_channel(start=7, width=6)
fixturee11 = universe3.add_channel(start=1, width=6)
fixturee12 = universe2.add_channel(start=505, width=6)
fixturee13 = universe2.add_channel(start=499, width=6)
fixturee14 = universe2.add_channel(start=493, width=6)
fixturee15 = universe2.add_channel(start=487, width=6)
fixturee16 = universe2.add_channel(start=481, width=6)
fixturee17 = universe2.add_channel(start=475, width=6)
fixturee18 = universe2.add_channel(start=469, width=6)
fixturee19 = universe2.add_channel(start=463, width=6)
fixturee20 = universe2.add_channel(start=457, width=6)
fixturee21 = universe2.add_channel(start=451, width=6)
fixturee22 = universe2.add_channel(start=445, width=6)
fixturee23 = universe2.add_channel(start=439, width=6)
fixturee24 = universe2.add_channel(start=433, width=6)
fixturee25 = universe2.add_channel(start=427, width=6)
fixturee26 = universe2.add_channel(start=421, width=6)
fixturee27 = universe2.add_channel(start=415, width=6)
fixturee28 = universe2.add_channel(start=409  width=6)
fixturee29 = universe2.add_channel(start=403, width=6)
fixturee30 = universe2.add_channel(start=397, width=6)
fixturee31 = universe2.add_channel(start=391, width=6)
fixturee32 = universe2.add_channel(start=385, width=6)
fixturee33 = universe2.add_channel(start=379, width=6)
fixturee34 = universe2.add_channel(start=373, width=6)
fixturee35 = universe2.add_channel(start=367, width=6)
fixturee36 = universe2.add_channel(start=361, width=6)
fixturee37 = universe2.add_channel(start=355, width=6)
fixturee38 = universe2.add_channel(start=349, width=6)
fixturee39 = universe2.add_channel(start=343, width=6)
fixturee40 = universe2.add_channel(start=337, width=6)
fixturee41 = universe2.add_channel(start=331, width=6)
fixturee42 = universe2.add_channel(start=325, width=6)
fixturee43 = universe2.add_channel(start=319, width=6)
fixturee44 = universe2.add_channel(start=313, width=6)
fixturee45 = universe2.add_channel(start=307, width=6)
fixturee46 = universe2.add_channel(start=301, width=6)
fixturee47 = universe2.add_channel(start=295, width=6)
fixturee48 = universe2.add_channel(start=289, width=6)

#strip f
fixturef1 = universe3.add_channel(start=67, width=6)
fixturef2 = universe3.add_channel(start=73, width=6)
fixturef3 = universe3.add_channel(start=79, width=6)
fixturef4 = universe3.add_channel(start=85, width=6)
fixturef5 = universe3.add_channel(start=91, width=6)
fixturef6 = universe3.add_channel(start=97, width=6)
fixturef7 = universe3.add_channel(start=103, width=6)
fixturef8 = universe3.add_channel(start=109, width=6)
fixturef9 = universe3.add_channel(start=115, width=6)
fixturef10 = universe3.add_channel(start=121, width=6)
fixturef11 = universe3.add_channel(start=127, width=6)
fixturef12 = universe3.add_channel(start=133, width=6)
fixturef13 = universe3.add_channel(start=139, width=6)
fixturef14 = universe3.add_channel(start=145, width=6)
fixturef15 = universe3.add_channel(start=151, width=6)
fixturef16 = universe3.add_channel(start=157, width=6)
fixturef17 = universe3.add_channel(start=163, width=6)
fixturef18 = universe3.add_channel(start=169, width=6)
fixturef19 = universe3.add_channel(start=175, width=6)
fixturef20 = universe3.add_channel(start=181, width=6)
fixturef21 = universe3.add_channel(start=187, width=6)
fixturef22 = universe3.add_channel(start=193, width=6)
fixturef23 = universe3.add_channel(start=199, width=6)
fixturef24 = universe3.add_channel(start=205, width=6)
fixturef25 = universe3.add_channel(start=211, width=6)
fixturef26 = universe3.add_channel(start=217, width=6)
fixturef27 = universe3.add_channel(start=223, width=6)
fixturef28 = universe3.add_channel(start=229  width=6)
fixturef29 = universe3.add_channel(start=235, width=6)
fixturef30 = universe3.add_channel(start=241, width=6)
fixturef31 = universe3.add_channel(start=247, width=6)
fixturef32 = universe3.add_channel(start=253, width=6)
fixturef33 = universe3.add_channel(start=259, width=6)
fixturef34 = universe3.add_channel(start=265, width=6)
fixturef35 = universe3.add_channel(start=271, width=6)
fixturef36 = universe3.add_channel(start=277, width=6)
fixturef37 = universe3.add_channel(start=283, width=6)
fixturef38 = universe3.add_channel(start=289, width=6)
fixturef39 = universe3.add_channel(start=295, width=6)
fixturef40 = universe3.add_channel(start=301, width=6)
fixturef41 = universe3.add_channel(start=307, width=6)
fixturef42 = universe3.add_channel(start=313, width=6)
fixturef43 = universe3.add_channel(start=319, width=6)
fixturef44 = universe3.add_channel(start=325, width=6)
fixturef45 = universe3.add_channel(start=331, width=6)
fixturef46 = universe3.add_channel(start=337, width=6)
fixturef47 = universe3.add_channel(start=343, width=6)
fixturef48 = universe3.add_channel(start=349, width=6)

async def functie():

    #hier starten we de 4 nodes 
    await node0.start()
    await node1.start()
    await node2.start()
    await node3.start()

#    universe0 = node.add_universe(2,1)
 #GG   universe1 = node.add_universe(0)
    # dit zou een range van channels kunnen requesten
    # channel = universe.get_channel('1/3')  
#    cnr = 1
#    StartOfChannel = 1
#    for x in range(170):
#    channel


# output van de leds 
# Fade channel to 255,0,0 in 5s
# The fade will automatically run in the background
#stap 1
    fixturea1.add_fade([255,0,0,255,0,0], 1000)
    fixtureb1.add_fade([255,0,0,255,0,0], 1000)
    fixturec1.add_fade([255,0,0,255,0,0], 1000)
    fixtured1.add_fade([255,0,0,255,0,0], 1000)
    fixturee1.add_fade([255,0,0,255,0,0], 1000)
    fixturef1.add_fade([255,0,0,255,0,0], 1000)
    
 # this can be used to wait till the fade is complete
    await fixturea1.wait_till_fade_complete()
    await fixtureb1.wait_till_fade_complete()
    await fixtureb1.wait_till_fade_complete()
    await fixtureb1.wait_till_fade_complete()
    await fixtureb1.wait_till_fade_complete()
    await fixtureb1.wait_till_fade_complete()
 
#stap2
    fixturea1.add_fade([0,0,0,0,0,0], 1000)
    fixtureb1.add_fade([0,0,0,0,0,0], 1000)
    fixturec1.add_fade([0,0,0,0,0,0], 1000)
    fixtured1.add_fade([0,0,0,0,0,0], 1000)
    fixturee1.add_fade([0,0,0,0,0,0], 1000)
    fixturef1.add_fade([0,0,0,0,0,0], 1000)
    
    fixturea2.add_fade([255,0,0,255,0,0], 1000)
    fixtureb2.add_fade([255,0,0,255,0,0], 1000)
    fixturec2.add_fade([255,0,0,255,0,0], 1000)
    fixtured2.add_fade([255,0,0,255,0,0], 1000)
    fixturee2.add_fade([255,0,0,255,0,0], 1000)
    fixturef2.add_fade([255,0,0,255,0,0], 1000)
  
    await fixturea1.wait_till_fade_complete()
    await fixtureb1.wait_till_fade_complete()
    await fixturec1.wait_till_fade_complete()
    await fixtured1.wait_till_fade_complete()
    await fixturee1.wait_till_fade_complete()
    await fixturef1.wait_till_fade_complete()

    await fixturea2.wait_till_fade_complete()
    await fixtureb2.wait_till_fade_complete()
    await fixturec2.wait_till_fade_complete()
    await fixtured2.wait_till_fade_complete()
    await fixturee2.wait_till_fade_complete()
    await fixturef2.wait_till_fade_complete()
    
    #stap3
    fixturea2.add_fade([0,0,0,0,0,0], 1000)
    fixtureb2.add_fade([0,0,0,0,0,0], 1000)
    fixturec2.add_fade([0,0,0,0,0,0], 1000)
    fixtured2.add_fade([0,0,0,0,0,0], 1000)
    fixturee2.add_fade([0,0,0,0,0,0], 1000)
    fixturef2.add_fade([0,0,0,0,0,0], 1000)
    
    fixturea3.add_fade([255,0,0,255,0,0], 1000)
    fixtureb3.add_fade([255,0,0,255,0,0], 1000)
    fixturec3.add_fade([255,0,0,255,0,0], 1000)
    fixtured3.add_fade([255,0,0,255,0,0], 1000)
    fixturee3.add_fade([255,0,0,255,0,0], 1000)
    fixturef3.add_fade([255,0,0,255,0,0], 1000)
  
    await fixturea2.wait_till_fade_complete()
    await fixtureb2.wait_till_fade_complete()
    await fixturec2.wait_till_fade_complete()
    await fixtured2.wait_till_fade_complete()
    await fixturee2.wait_till_fade_complete()
    await fixturef2.wait_till_fade_complete()

    await fixturea3.wait_till_fade_complete()
    await fixtureb3.wait_till_fade_complete()
    await fixturec3.wait_till_fade_complete()
    await fixtured3.wait_till_fade_complete()
    await fixturee3.wait_till_fade_complete()
    await fixturef3.wait_till_fade_complete()
    
    #stap4
    fixturea3.add_fade([0,0,0,0,0,0], 1000)
    fixtureb3.add_fade([0,0,0,0,0,0], 1000)
    fixturec3.add_fade([0,0,0,0,0,0], 1000)
    fixtured3.add_fade([0,0,0,0,0,0], 1000)
    fixturee3.add_fade([0,0,0,0,0,0], 1000)
    fixturef3.add_fade([0,0,0,0,0,0], 1000)
    
    fixturea4.add_fade([255,0,0,255,0,0], 1000)
    fixtureb4.add_fade([255,0,0,255,0,0], 1000)
    fixturec4.add_fade([255,0,0,255,0,0], 1000)
    fixtured4.add_fade([255,0,0,255,0,0], 1000)
    fixturee4.add_fade([255,0,0,255,0,0], 1000)
    fixturef4.add_fade([255,0,0,255,0,0], 1000)
  
    await fixturea3.wait_till_fade_complete()
    await fixtureb3.wait_till_fade_complete()
    await fixturec3.wait_till_fade_complete()
    await fixtured3.wait_till_fade_complete()
    await fixturee3.wait_till_fade_complete()
    await fixturef3.wait_till_fade_complete()

    await fixturea4.wait_till_fade_complete()
    await fixtureb4.wait_till_fade_complete()
    await fixturec4.wait_till_fade_complete()
    await fixtured4.wait_till_fade_complete()
    await fixturee4.wait_till_fade_complete()
    await fixturef4.wait_till_fade_complete()
    
    #stap 5 
    fixturea4.add_fade([0,0,0,0,0,0], 1000)
    fixtureb4.add_fade([0,0,0,0,0,0], 1000)
    fixturec4.add_fade([0,0,0,0,0,0], 1000)
    fixtured4.add_fade([0,0,0,0,0,0], 1000)
    fixturee4.add_fade([0,0,0,0,0,0], 1000)
    fixturef4.add_fade([0,0,0,0,0,0], 1000)
    
    await fixturea4.wait_till_fade_complete()
    await fixtureb4.wait_till_fade_complete()
    await fixturec4.wait_till_fade_complete()
    await fixtured4.wait_till_fade_complete()
    await fixturee4.wait_till_fade_complete()
    await fixturef4.wait_till_fade_complete()
    

asyncio.run(functie())

