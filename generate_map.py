"""
Spotswood Historic Homes Map Generator
=======================================
Usage:
  python generate_map.py           # generates index.html

Or paste the code into a Jupyter notebook cell.

To add a new property, add an entry to the 'properties' list below and re-run.
See ADD_NEW_PROPERTY.md for details.
"""

import folium
from folium import IFrame, Popup, Marker, Icon, TileLayer, LayerControl
from folium.plugins import MarkerCluster, Fullscreen

# ── Image base URL ──────────────────────────────────────────────────────────
IMAGE_BASE = "https://raw.githubusercontent.com/MikeHistory/Spotswood-Historic-Homes/refs/heads/main/images"

# ── Map centre & zoom ──────────────────────────────────────────────────────
MAP_CENTER = [40.391565230621474, -74.3903805208576]
ZOOM_START = 15

# ── Era definitions (colour coding) ────────────────────────────────────────
ERAS = {
    "1700s":     "orange",
    "1800s":     "red",
    "1900-1909": "green",
    "1910-1919": "blue",
    "1920-1929": "black",
    "1930-1939": "pink",
    "1940-1949": "purple",
    "1950-1959": "darkred",
}

# ── Property data ──────────────────────────────────────────────────────────
# Format: [lat, lon, name, year, era, description, image, icon, color]
#
# icon types: "home", "church", "industry", "store"
# color must match the era colour in the ERAS dict above
#
# To add a new home, just append a new row here and re-run the script.
# ───────────────────────────────────────────────────────────────────────────
properties = [
    # ── 1700s (Orange) ─────────────────────────────────────────────────────
    [40.391119167853574, -74.38927290757084, "St. Peter's Church", "1899", "1700s",
     "Although there has been record of a chruch here since the 1740's, the current structure was rebuilt in the 1800's after a fire.",
     "stpeters.jpeg", "church", "orange"],

    [40.37404720357879, -74.41629291824485, "Ten Eyks Forge", "1700s", "1700s",
     "One of the earliest forges in the county, established before the Revolution. Some stonework is still visible",
     "oldforge.jpeg", "industry", "orange"],

    # ── 1800s (Red) ────────────────────────────────────────────────────────
    [40.37576344900822, -74.41134856125089, "37 S. Shore Blvd", "1893", "1800s",
     "Predates Physical Culture City",
     "37Shore.jpeg", "home", "red"],

    [40.38533844328248, -74.39040014355436, "26 Lakeview Dr", "1869", "1800s",
     "Very old pine trees and water facing structures on property.",
     "26lakeview.jpeg", "home", "red"],

    [40.35452738643187, -74.4418346184206, "15 Stockton Ave", "1835", "1800s",
     "Marryott House",
     "MarryottHouse.jpeg", "home", "red"],

    [40.37775887887239, -74.42493778094678, "Helmetta Snuff Mill", "1880", "1800s",
     "Now the 'Lofts at Helmetta' Condominiums",
     "Snuffmill.jpeg", "industry", "red"],

    [40.39327262044848, -74.38676971846652, "Spotswood Reformed Church", "1821", "1800s",
     "Over two centuries of history and many of the town's early leaders laid to rest here.",
     "reformed.jpeg", "church", "red"],

    [40.39069588735334, -74.39220009049912, "Immaculate Convent", "Circa 1875", "1800s",
     "Originally constructed by a former Confederate Officer in the 1870s. The land was purchased by the Church in 1909.",
     "Convent.jpeg", "church", "red"],

    [40.391773299634096, -74.38930951482584, "505 Main Street.", "1872", "1800s",
     "St. Peter's Rectory, constructed in 1872.",
     "505main.jpeg", "church", "red"],

    # ── 1900-1909 (Green) ──────────────────────────────────────────────────
    [40.385888760121915, -74.40217742646804, "300 Manalapan Ave", "1905", "1900-1909",
     "Constructed during Physical Culture era.",
     "300Manalapan.jpeg", "home", "green"],

    [40.385249232439946, -74.38854921936806, "222 Devoe Ave", "1900", "1900-1909",
     "Devoe Mansion.",
     "222devoe.jpeg", "home", "green"],

    [40.3741229106213, -74.42815593006208, "92 Main St", "1907", "1900-1909",
     "Main Street, Helmetta",
     "92mainstreet.jpeg", "home", "green"],

    [40.39402914768797, -74.38645461845664, "421 Main St", "1905", "1900-1909",
     "Three years before Spotswood became its own boro.",
     "421main.jpeg", "home", "green"],

    [40.37959501397669, -74.40771826802995, "22 Avenue C", "1906", "1900-1909",
     "Constructed during Physical Culture City era.",
     "22AveC.jpeg", "home", "green"],

    [40.35616867884141, -74.44309178323445, "33 Stockton Ave.", "1900", "1900-1909",
     "Jamesburg Turn of 20th Century.",
     "33stockton.jpeg", "home", "green"],

    [40.38664472038314, -74.39896231749604, "219 Manalapan Rd.", "1955", "1900-1909",
     "Second house from corner.",
     "219manalapan.jpeg", "home", "green"],

    [40.38718583361005, -74.39795347164319, "191 Manalapan Rd.", "1905", "1900-1909",
     "At the intersection of River Street, itself a very old street.",
     "191manalapan.jpeg", "home", "green"],

    [40.38408589764912, -74.39010246063746, "57 Lettau Drive", "1905", "1900-1909",
     "Structure seems to hint at possible earlier origins.",
     "57lettau.jpeg", "home", "green"],

    [40.407325932962934, -74.37493078837302, "24 Main Street.", "1905", "1900-1909",
     "Near intersection with Old Stage.",
     "24main.jpeg", "home", "green"],

    [40.39329121141645, -74.38776959315489, "452 Main Street.", "1905", "1900-1909",
     "Blue house with elaborate lattice work..",
     "452main.jpeg", "home", "green"],

    # ── 1910-1919 (Blue) ──────────────────────────────────────────────────
    [40.38238830813217, -74.42103717710137, "45 Lake Ave.", "1910", "1910-1919",
     "Tucked Away Behind Pines",
     "45lake.jpeg", "home", "blue"],

    [40.38906129788272, -74.3870385015316, "15 Mundy Ave.", "1910", "1910-1919",
     "Across From Playground",
     "15mundy.jpeg", "home", "blue"],

    [40.396603154880175, -74.38420067197023, "321 Main St.", "1918", "1910-1919",
     "Past Summerhill On Right",
     "321main.jpeg", "home", "blue"],

    # ── 1920-1929 (Black) ─────────────────────────────────────────────────
    [40.38930441527162, -74.38259221121461, "116 Mundy Ave", "1926", "1920-1929",
     "Possible older mill structures on property.",
     "116mundy.jpeg", "home", "black"],

    [40.38573789455148, -74.3834434656437, "114 Fernhead", "1926", "1920-1929",
     "Mary's House",
     "114fernhead.jpeg", "home", "black"],

    [40.38948683884871, -74.38836835144457, "79 Devoe Ave", "1929", "1920-1929",
     "Long, old stone lined driveway in front.",
     "79devoe.jpeg", "home", "black"],

    [40.39246682175453, -74.38909948774666, "490 Main Street", "1920", "1920-1929",
     "Once the site of a gubernaterial debate in the 1930's, it was also home to Spotswood's local doctor for several decades",
     "490main.jpeg", "home", "black"],

    [40.38807651064285, -74.39333229613035, "50 South Street.", "1928", "1920-1929",
     "One of several houses with same construction style.",
     "50south.jpeg", "home", "black"],

    [40.38815669703339, -74.39344696056672, "46 South Street.", "1928", "1920-1929",
     "One of several houses with same construction style.",
     "46south.jpeg", "home", "black"],

    [40.388278764033096, -74.39351535689677, "44 South Street.", "1928", "1920-1929",
     "One of several houses with same construction style.",
     "44south.jpeg", "home", "black"],

    # ── 1930-1939 (Pink) ──────────────────────────────────────────────────
    [40.38915852582279, -74.38640937262706, "29 Mundy Ave.", "1938", "1930-1939",
     "Home is built on elevated ground with retaining wall.",
     "29mundy.jpeg", "home", "pink"],

    [40.393361065518725, -74.38765823096863, "448 Main Street.", "1930", "1930-1939",
     "Near post office. Closely tucked near another house.",
     "448main.jpeg", "home", "pink"],

    # ── 1940-1949 (Purple) ────────────────────────────────────────────────
    [40.39259716480967, -74.3888259050029, "482 Main Street", "Circa 1945", "1940-1949",
     "Over two centuries of history and many of the town's early leaders laid to rest here.",
     "482main.jpeg", "store", "purple"],

    [40.40076624942257, -74.38094939227055, "186 Main Street.", "1945", "1940-1949",
     "Small home, several structures on property near railroad.",
     "186main.jpeg", "home", "purple"],

    # ── 1950-1959 (Darkred) ───────────────────────────────────────────────
    [40.38910038876435, -74.3866540686125, "23 Mundy Ave.", "1955", "1950-1959",
     "Across From Playground",
     "23mundy.jpeg", "home", "darkred"],

    [40.38934397177625, -74.38810031732679, "87 Devoe Ave.", "1954", "1950-1959",
     "The infamous H*tler House.",
     "87devoe.jpeg", "home", "darkred"],

    [40.38920998245602, -74.38787572498619, "93 Devoe Ave.", "1953", "1950-1959",
     "Black and White Awnings.",
     "93devoe.jpeg", "home", "darkred"],

    [40.38906407823472, -74.38763267439222, "97 Devoe Ave.", "1955", "1950-1959",
     "Red house on corner of Mundy and Devoe.",
     "97devoe.jpeg", "home", "darkred"],
]


# ── Helper: popup HTML ────────────────────────────────────────────────────
def popup_html(name, year, era, description, image):
    return f"""
    <style>
        .popup-content {{
            font-family: Arial;
            font-size: 10px;
            line-height: 1.5;
            width: 250px;
        }}
        .popup-content h4 {{ margin: 8px 0; }}
        .popup-content p {{ margin: 0 0 4px 0; }}
        @media (max-width: 600px) {{
            .popup-content {{ width: 90vw; font-size: 14px; }}
            .popup-content img {{ width: 100%; max-width: none; }}
        }}
    </style>
    <div class="popup-content">
        <h4>{name} ({year})</h4>
        <p><b>Era:</b> {era}</p>
        <p>{description}</p>
        <div style="text-align:center;margin:8px 0;">
            <img src="{IMAGE_BASE}/{image}"
                 style="width: 100%; max-width: 200px; height: auto;">
        </div>
    </div>
    """


# ── Build the map ─────────────────────────────────────────────────────────
def build_map():
    m = folium.Map(
        location=MAP_CENTER,
        zoom_start=ZOOM_START,
        tiles="OpenStreetMap",
        prefer_canvas=False,
        zoom_control=False,
    )

    # Google Satellite hybrid layer
    TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="Google Satellite",
        name="Google Satellite",
        max_zoom=22,
        max_native_zoom=22,
    ).add_to(m)

    # One MarkerCluster per era
    clusters = {}
    for era, color in ERAS.items():
        cluster = MarkerCluster(
            name=f'<span style="color: {color}; font-family: Arial, sans-serif; font-size: 12px;">{era}</span>',
            show=True,
            options={
                "showCoverageOnHover": False,
                "spiderfyOnMaxZoom": True,
                "disableClusteringAtZoom": 16,
            },
        )
        clusters[era] = cluster

    # Add markers
    for lat, lon, name, year, era, desc, img, icon_type, color in properties:
        html = popup_html(name, year, era, desc, img)
        iframe = IFrame(html, width=350, height=250)
        popup = Popup(iframe, max_width=500)

        Marker(
            location=[lat, lon],
            popup=popup,
            icon=Icon(
                color=color,
                icon_color="white",
                icon=icon_type,
                prefix="fa",
            ),
            tooltip=folium.Tooltip(
                year,
                permanent=True,
                direction="top",
                className="year-tooltip",
                offset=[0, -10],
            ),
        ).add_to(clusters[era])

    # Add clusters to map
    for cluster in clusters.values():
        cluster.add_to(m)

    # Layer control (era toggle / "time slider")
    LayerControl(position="bottomright", collapsed=True).add_to(m)

    # Fullscreen button
    Fullscreen(position="topleft").add_to(m)

    return m


def render_html(m):
    """Render the map to an HTML string with custom CSS injected."""
    html = m._repr_html_() if hasattr(m, "_repr_html_") else m.get_root().render()

    # ── Tooltip CSS ────────────────────────────────────────────────────
    tooltip_css = """
    <style>
        .year-tooltip {
            background-color: rgba(0, 0, 0, 0.75) !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 2px 6px !important;
            font-size: 11px !important;
            font-weight: bold !important;
            font-family: Arial, sans-serif !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
            white-space: nowrap !important;
        }
        .year-tooltip:before {
            border-top-color: rgba(0, 0, 0, 0.75) !important;
        }
        @media (max-width: 600px) {
            .year-tooltip {
                font-size: 10px !important;
                padding: 2px 5px !important;
            }
        }
    </style>
    </head>"""

    html = html.replace("</head>", tooltip_css)

    # ── Title banner ──────────────────────────────────────────────────
    title_banner = """
    <style>
        .title-banner {
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 9999;
            background: blue;
            color: yellow;
            padding: 16px;
            font-family: Arial, sans-serif;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            border-bottom: 3px solid #ddd;
            text-align: center;
        }
        @media (max-width: 600px) {
            .title-banner { padding: 10px; font-size: 16px; }
        }
    </style>
    <div class="title-banner">Spotswood Historic Homes</div>
    </body>"""

    html = html.replace("</body>", title_banner)

    # Fix FontAwesome version for Awesome Markers compatibility
    html = html.replace("fontawesome-free@6.2.0", "fontawesome-free@5.15.4")

    return html


# ── Main ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    m = build_map()
    html = render_html(m)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Map saved to index.html  ({len(properties)} properties)")
