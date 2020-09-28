import pandas
import folium


def mapmake():
    data = pandas.read_csv("uploads/uploaded-sample.csv")
    infos=[]
    norows = len(data.index)    
    for i in range(norows):
        infos.append(dict(data.iloc[i]))
    
    lat = list(data["Latitude"])
    lon = list(data["Longitude"])

    map = folium.Map(location=[0,0], tiles="openstreetmap",zoom_start=2)
    fgi=folium.FeatureGroup(name="Info")

    for info, lt, ln in zip(infos,lat,lon):
        fgi.add_child(folium.CircleMarker(location=[lt,ln],tooltip="click me to see my loc info", fill_color="green", fill_opacity=0.7, radius = 6,popup=str(info).replace(":"," =").replace("{","").replace("}","").replace("'","").replace("nan","info not available")))

    map.add_child(fgi)

    folium.TileLayer('Stamen Terrain').add_to(map)
    folium.TileLayer('stamentoner').add_to(map)
    folium.TileLayer('stamenwatercolor').add_to(map)
    folium.TileLayer('cartodbpositron').add_to(map)
    folium.TileLayer('cartodbdark_matter').add_to(map)

    folium.LayerControl().add_to(map)
    map.save("uploads/map.html")
    pass
