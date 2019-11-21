from Core.DataLoaders.DataLoader import get_checkpoints
from gmplot import gmplot

if __name__ == '__main__':
    gmap = gmplot.GoogleMapPlotter(30.3164945,
                                   78.03219179999999, 13)
    gmap.draw('test.html')
