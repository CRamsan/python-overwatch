from overwatch import Overwatch

# List of lists containing battle tags and their respective platform
# players = [['Seagull-1894'], ['empathy_awaits', 'psn'], ['Seagull-1894', 'pc'], ['Dark Desert Fox', 'xbl']]
players = [['empathy_awaits', 'psn']]

for player in players:
    print (player)
    if len(player) == 2:
        OW = Overwatch(battletag=player[0], platform=player[1])
    else:
        OW = Overwatch(battletag=player[0])
    for mode in OW.modes:
        print (OW.comparisons)
        for selection in OW.comparisons:
            print (selection + ' for ' + str(mode) + ' - ' + str(OW.comparison(mode=mode, stat=selection)))
        for heroe in OW.heroes:
            for filt in OW.stats:
                if filt == 'Hero Specific' and heroe == 'all':
                    continue
                if filt == 'Miscellaneous' and heroe != 'all':
                    continue
                #print (mode + '-' + filt + '-' + heroe + '-' + str(OW.get_stats(mode=mode, hero=heroe, stat=filt)))
'''
        for achievement in OW.achievementTypes:
            print (achievement + ' for ' + str(mode) + ' - ' + str(OW.achiements(mode=mode, achivementType=achievement)))
'''
