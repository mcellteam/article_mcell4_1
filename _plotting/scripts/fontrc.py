import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

def configure_fonts():
    print('Looking for my favorite font...')
    font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
    path = font_manager.findfont("Gill Sans")
    # path = '/System/Library/Fonts/Supplemental/GillSans.ttc'
    prop = font_manager.FontProperties(fname=path)
    #prop = findfont(FontProperties(family=['sans-serif']))
    mpl.rcParams['font.family'] = prop.get_name()