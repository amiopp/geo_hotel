from dataclasses import dataclass


@dataclass(frozen=True)
class HotelPhoto:
    image_url: str
    source_url: str


FALLBACK_HOTEL_IMAGES = [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=900&q=80",
]


# Real hotel photos are mapped only when the hotel identity is clear enough
# from the imported name plus official/listing sources.
REAL_HOTEL_PHOTOS: dict[int, HotelPhoto] = {
    6: HotelPhoto(
        "https://noaille-hotel.hotels-in-casablanca.com/data/Photos/1080x700w/12920/1292021/1292021332/casablanca-noaille-hotel-casablanca-photo-1.JPEG",
        "https://noaille-hotel.hotels-in-casablanca.com/en/",
    ),
    13: HotelPhoto(
        "https://du-louvre.hotels-in-casablanca.com/data/Photos/1080x700w/13100/1310011/1310011087/casablanca-hotel-du-louvre-photo-1.JPEG",
        "https://du-louvre.hotels-in-casablanca.com/en/",
    ),
    19: HotelPhoto(
        "https://rio.hotels-in-casablanca.com/data/Pics/1080x700w/11563/1156320/1156320852/rio-casablanca-pic-1.JPEG",
        "https://rio.hotels-in-casablanca.com/en/",
    ),
    26: HotelPhoto(
        "https://premiere-classe-centre-ville.hotels-in-casablanca.com/data/Pics/1080x700w/14229/1422966/1422966855/premiere-classe-casablanca-centre-ville-casablanca-pic-1.JPEG",
        "https://premiere-classe-centre-ville.hotels-in-casablanca.com/en/",
    ),
    27: HotelPhoto(
        "https://astrid.hotels-in-casablanca.com/data/Pics/1080x700w/11394/1139466/1139466730/hotel-astrid-casablanca-pic-1.JPEG",
        "https://astrid.hotels-in-casablanca.com/en/",
    ),
    29: HotelPhoto(
        "https://point-du-jour-10-rue-lieutnant-berger-ma.hotels-in-casablanca.com/data/Photos/1080x700w/17255/1725542/1725542410/casablanca-point-du-jour-photo-1.JPEG",
        "https://point-du-jour-10-rue-lieutnant-berger-ma.hotels-in-casablanca.com/en/",
    ),
    30: HotelPhoto(
        "https://colisee.hotels-in-casablanca.com/data/Photos/1080x700w/11758/1175827/1175827228/casablanca-colisee-hotel-photo-1.JPEG",
        "https://colisee.hotels-in-casablanca.com/en/",
    ),
    31: HotelPhoto(
        "https://hotel-salim-casablanca.hotels-in-casablanca.com/data/Photos/1080x700w/7884/788432/788432850/photo-hotel-salim-casablanca-1.JPEG",
        "https://hotel-salim-casablanca.hotels-in-casablanca.com/en/",
    ),
    34: HotelPhoto(
        "https://anfa-port.hotels-in-casablanca.com/data/Photos/1080x700w/764/76441/76441646/casablanca-hotel-anfa-port-photo-1.JPEG",
        "https://anfa-port.hotels-in-casablanca.com/en/",
    ),
    35: HotelPhoto(
        "https://volubilis.hotels-in-casablanca.com/data/Pics/1080x700w/16271/1627119/1627119696/hotel-volubilis-casablanca-pic-1.JPEG",
        "https://volubilis.hotels-in-casablanca.com/en/",
    ),
    36: HotelPhoto(
        "https://images.trvl-media.com/lodging/12000000/11970000/11970000/11969964/73304f12.jpg?impolicy=resizecrop&ra=fit&rw=598",
        "https://www.hotels.com/ho384038848/hotel-yto-casablanca-morocco/",
    ),
    38: HotelPhoto(
        "https://central.hotels-in-casablanca.com/data/Photos/1080x700w/5226/522609/522609921/casablanca-hotel-central-photo-1.JPEG",
        "https://central.hotels-in-casablanca.com/en/",
    ),
    39: HotelPhoto(
        "https://manzil.hotels-in-casablanca.com/data/Photos/1080x700w/6847/684711/684711942/casablanca-manzil-hotel-photo-1.JPEG",
        "https://manzil.hotels-in-casablanca.com/en/",
    ),
    40: HotelPhoto(
        "https://tropicana.hotels-in-casablanca.com/data/Pics/1080x700w/14670/1467042/1467042140/hotel-tropicana-casablanca-pic-1.JPEG",
        "https://tropicana.hotels-in-casablanca.com/en/",
    ),
    41: HotelPhoto(
        "https://al-walid.hotels-in-casablanca.com/data/Photos/1080x700w/2458/245855/245855333/casablanca-hotel-al-walid-photo-1.JPEG",
        "https://al-walid.hotels-in-casablanca.com/en/",
    ),
    42: HotelPhoto(
        "https://www.ahstatic.com/photos/7585_ho_00_p_1024x768.jpg",
        "https://all.accor.com/hotel/7585/index.en.shtml",
    ),
    44: HotelPhoto(
        "https://media.iceportal.com/107158/photos/75783428_L.jpg",
        "https://casablanca-centre-ville.campanile.com/en-us/",
    ),
    45: HotelPhoto(
        "https://relax-casa-voyageurs.hotels-in-casablanca.com/data/Photos/1080x700w/12839/1283918/1283918656/casablanca-relax-hotel-casa-voyageurs-photo-1.JPEG",
        "https://relax-casa-voyageurs.hotels-in-casablanca.com/en/",
    ),
    46: HotelPhoto(
        "https://delta-atlas.hotels-in-casablanca.com/data/Pics/1080x700w/17318/1731814/1731814183/hotel-delta-atlas-casablanca-pic-1.JPEG",
        "https://delta-atlas.hotels-in-casablanca.com/en/",
    ),
    47: HotelPhoto(
        "https://belle-rive.hotels-in-casablanca.com/data/Photos/1080x700w/11758/1175847/1175847655/photo-hotel-bellerive-casablanca-1.JPEG",
        "https://belle-rive.hotels-in-casablanca.com/en/",
    ),
    50: HotelPhoto(
        "https://washington.hotels-in-casablanca.com/data/Photos/1080x700w/16778/1677859/1677859984/casablanca-washington-hotel-photo-1.JPEG",
        "https://washington.hotels-in-casablanca.com/en/",
    ),
    51: HotelPhoto(
        "https://le-littoral.hotels-in-casablanca.com/data/Pics/1080x700w/7632/763281/763281220/le-littoral-casablanca-pic-1.JPEG",
        "https://le-littoral.hotels-in-casablanca.com/en/",
    ),
    52: HotelPhoto(
        "https://www.ahstatic.com/photos/a0g4_ho_01_p_1024x768.jpg",
        "https://all.accor.com/hotel/A0G4/index.en.shtml",
    ),
    53: HotelPhoto(
        "https://guynemer.hotels-in-casablanca.com/data/Photos/1080x700w/7474/747449/747449393/casablanca-guynemer-photo-1.JPEG",
        "https://guynemer.hotels-in-casablanca.com/en/",
    ),
    54: HotelPhoto(
        "https://de-paris.hotels-in-casablanca.com/data/Photos/1080x700w/12974/1297420/1297420546/casablanca-hotel-de-paris-photo-1.JPEG",
        "https://de-paris.hotels-in-casablanca.com/en/",
    ),
    55: HotelPhoto(
        "https://www.onomohotels.com/app/uploads/2023/04/onomo-hotel-casablanca-sidi-maarouf-superior-room-6.webp",
        "https://www.onomohotels.com/hotel/onomo-hotel-casablanca-sidi-maarouf/",
    ),
    56: HotelPhoto(
        "https://moroccan-house.hotels-in-casablanca.com/data/Photos/1080x700w/17163/1716390/1716390204/photo-hotel-moroccan-house-casablanca-casablanca-1.JPEG",
        "https://moroccan-house.hotels-in-casablanca.com/en/",
    ),
    59: HotelPhoto(
        "https://east-west.hotels-in-casablanca.com/data/Photos/1080x700w/13201/1320139/1320139426/casablanca-east-west-hotel-photo-1.JPEG",
        "https://east-west.hotels-in-casablanca.com/en/",
    ),
    60: HotelPhoto(
        "https://www.ahstatic.com/photos/6289_ho_00_p_1024x768.jpg",
        "https://all.accor.com/hotel/6289/index.en.shtml",
    ),
    61: HotelPhoto(
        "https://rania-belmadina.hotels-in-casablanca.com/data/Pics/1080x700w/17237/1723730/1723730021/rania-belmadina-hotel-casablanca-pic-1.JPEG",
        "https://rania-belmadina.hotels-in-casablanca.com/en/",
    ),
    62: HotelPhoto(
        "https://www.ahstatic.com/photos/6573_ho_01_p_1024x768.jpg",
        "https://all.accor.com/hotel/6573/index.en.shtml",
    ),
    65: HotelPhoto(
        "https://les-saisons.hotels-in-casablanca.com/data/Pics/1080x700w/17131/1713197/1713197829/hotel-les-saisons-casablanca-pic-1.JPEG",
        "https://les-saisons.hotels-in-casablanca.com/en/",
    ),
    66: HotelPhoto(
        "https://le-zenith.hotels-in-casablanca.com/data/Photos/1080x700w/13550/1355040/1355040428/casablanca-le-zenith-hotel-spa-photo-1.JPEG",
        "https://le-zenith.hotels-in-casablanca.com/en/",
    ),
    67: HotelPhoto(
        "https://www.ahstatic.com/photos/6572_ho_00_p_1024x768.jpg",
        "https://all.accor.com/hotel/6572/index.en.shtml",
    ),
    68: HotelPhoto(
        "https://images.trvl-media.com/lodging/27000000/26830000/26829100/26829054/eab141cb.jpg?h=201&impolicy=fcrop&p=1&q=medium&w=469",
        "https://www.expedia.com/Casablanca-Hotels-Odyssee-Center-Hotel.h26829054.Hotel-Information",
    ),
    69: HotelPhoto(
        "https://www.oumpalace.com/_next/image?url=%2Fimages%2FHotel%2FDSC09953.jpg&w=2048&q=75",
        "https://www.oumpalace.com/",
    ),
    70: HotelPhoto(
        "https://images.squarespace-cdn.com/content/v1/515c5af9e4b0bca14d7485fc/1607531785822-GZR1MQGM6W2BDE4PZPAQ/PHOTO-2019-12-02-13-05-36%2B30.jpg",
        "https://www.hoteldiwancasablanca.com/",
    ),
    71: HotelPhoto(
        "https://photos.smugmug.com/Maroc-Lovers/Casablanca/Hotels/Art-Palace-Suites-and-Spa-Hotel/i-4mkNCS5/0/MDDBzmXS6QfcrkfvqgMmpkTnDWdWfjqRZDHvBxJg2/L/art-palace-suites-and-spa-apartment-hotel-casablanca-L.jpg",
        "https://maroclovers.com/en/where-stay-casablanca-best-hotels-neighborhoods/",
    ),
    72: HotelPhoto(
        "https://villa-blanca-urban.hotels-in-casablanca.com/data/Images/1080x700w/17426/1742661/1742661376/casablanca-villa-blanca-urban-hotel-image-1.JPEG",
        "https://villa-blanca-urban.hotels-in-casablanca.com/en/",
    ),
    73: HotelPhoto(
        "https://photos.smugmug.com/Maroc-Lovers/Casablanca/Hotels/Idou-Anfa-Hotel/i-PpjqrgP/0/LQpNR7j5NWHDWPt9sxjFbssDKQt8nnCc7tjdZ8zn6/L/idou-anfa-hotel-casablanca-lobby-L.jpg",
        "https://maroclovers.com/en/where-stay-casablanca-best-hotels-neighborhoods/",
    ),
    74: HotelPhoto(
        "https://le-lido-thalasso-spa.hotels-in-casablanca.com/data/Pics/1080x700w/17097/1709765/1709765400/casablanca-le-lido-thalasso-spa-casablanca-pic-1.JPEG",
        "https://le-lido-thalasso-spa.hotels-in-casablanca.com/en/",
    ),
    75: HotelPhoto(
        "https://image-tc.galaxy.tf/wijpeg-ee27ah3vjod1k1mj4feden0p/front-office.jpg",
        "https://www.kenzi-hotels.com/en/kenzi-basma",
    ),
    77: HotelPhoto(
        "https://photos.smugmug.com/Maroc-Lovers/Casablanca/Hotels/Other-Hotels/i-xnRnSXC/0/MjPnN5GkQTXWkDG84qB6ZqpZfcGsw6M889JbXRp8f/L/hotel-club-val-danfa-casablanca-lobby-L.jpg",
        "https://maroclovers.com/en/where-stay-casablanca-best-hotels-neighborhoods/",
    ),
    78: HotelPhoto(
        "https://suisse.hotels-in-casablanca.com/data/Pics/1080x700w/10319/1031952/1031952763/hotel-suisse-casablanca-pic-1.JPEG",
        "https://suisse.hotels-in-casablanca.com/en/",
    ),
    79: HotelPhoto(
        "https://azur.hotels-in-casablanca.com/data/Images/1080x700w/17132/1713201/1713201229/casablanca-hotel-azur-image-1.JPEG",
        "https://azur.hotels-in-casablanca.com/en/",
    ),
    80: HotelPhoto(
        "https://golden-star.hotels-in-casablanca.com/data/Photos/1080x700w/17288/1728842/1728842363.JPEG",
        "https://golden-star.hotels-in-casablanca.com/en/",
    ),
    81: HotelPhoto(
        "https://www.onomohotels.com/app/uploads/2023/04/onomo-hotel-casablanca-city-center-facade-entrance-3-scaled.webp",
        "https://www.onomohotels.com/hotel/onomo-hotel-casablanca-city-center/",
    ),
    82: HotelPhoto(
        "https://static.barcelo.com/content/dam/bhg/master/es/hoteles/marruecos/casablanca/barcelo-casablanca/main-photos/hotel/BCAS_ROOM_59.jpg",
        "https://www.barcelo.com/fr-fr/barcelo-casablanca/",
    ),
    83: HotelPhoto(
        "https://le-135-hotel.hotels-in-casablanca.com/data/Photos/1080x700w/13422/1342283/1342283591/casablanca-le-135-appart-hotel-photo-1.JPEG",
        "https://le-135-hotel.hotels-in-casablanca.com/en/",
    ),
    84: HotelPhoto(
        "https://imperial-spa.hotels-in-casablanca.com/data/Images/1080x700w/12771/1277175/1277175670/casablanca-imperial-casablanca-hotel-image-1.JPEG",
        "https://imperial-spa.hotels-in-casablanca.com/en/",
    ),
    85: HotelPhoto(
        "https://images.trvl-media.com/lodging/15000000/14770000/14768600/14768561/12756996.jpg?h=201&impolicy=fcrop&p=1&q=medium&w=469",
        "https://www.hotels.com/",
    ),
    86: HotelPhoto(
        "https://image-tc.galaxy.tf/wijpeg-2bph59amytwyayc30s9ibo50d/facade.jpg",
        "https://www.kenzi-hotels.com/en/kenzi-sidi-maarouf",
    ),
    87: HotelPhoto(
        "https://the-seven-and-spa.hotels-in-casablanca.com/data/Pics/1080x700w/17221/1722186/1722186582/the-seven-hotel-casablanca-pic-1.JPEG",
        "https://the-seven-and-spa.hotels-in-casablanca.com/en/",
    ),
    88: HotelPhoto(
        "https://mogador-marina.hotels-in-casablanca.com/data/Photos/1080x700w/17219/1721933/1721933748/casablanca-mogador-marina-photo-1.JPEG",
        "https://mogador-marina.hotels-in-casablanca.com/en/",
    ),
    89: HotelPhoto(
        "https://d31tsesv4zrpsz.cloudfront.net/cache/img/d9cac7e5e89d50cf1b6341f5aa52869c0350d5d8-d9cac7-1200-627-crop.jpg?q=1695287291",
        "https://www.lecasablanca-hotel.com/",
    ),
    92: HotelPhoto(
        "https://cache.marriott.com/is/image/marriotts7prod/mc-cmnmc-hotel-night-entrance31967-02044%3AClassic-Hor?fit=constrain&wid=1336",
        "https://www.marriott.com/en-us/hotels/cmnmc-casablanca-marriott-hotel/photos/",
    ),
    93: HotelPhoto(
        "https://www.royalmansour.com/wp-content/uploads/2024/07/casa-g-entree.jpg",
        "https://www.royalmansour.com/royal-mansour-casablanca/",
    ),
    94: HotelPhoto(
        "https://m.ahstatic.com/is/image/accorhotels/Casablanca_xxxxxxx_i117597",
        "https://movenpick.accor.com/en/africa/morocco/casablanca/hotel-casablanca.html",
    ),
    95: HotelPhoto(
        "https://static.barcelo.com/content/dam/bhg/master/es/hoteles/marruecos/casablanca/barcelo-anfa-casablanca/main-photos/hotel/BANFACAS_ROOM_09.jpg",
        "https://www.barcelo.com/fr-fr/barcelo-anfa-casablanca/",
    ),
    96: HotelPhoto(
        "https://radisson-blu-city-center.hotels-in-casablanca.com/data/Photos/1080x700w/16323/1632314/1632314209/casablanca-radisson-blu-hotel-casablanca-city-center-photo-1.JPEG",
        "https://radisson-blu-city-center.hotels-in-casablanca.com/en/",
    ),
    97: HotelPhoto(
        "https://le-palace-danfa.hotels-in-casablanca.com/data/Photos/1080x700w/12120/1212070/1212070150/casablanca-le-palace-d-anfa-photo-1.JPEG",
        "https://le-palace-danfa.hotels-in-casablanca.com/en/",
    ),
    99: HotelPhoto(
        "https://cache.marriott.com/is/image/marriotts7prod/cy-cmncm-lobby-welcome-42675%3AFeature-Hor?fit=constrain&wid=1920",
        "https://www.marriott.com/en-us/hotels/cmncm-courtyard-casablanca-downtown/overview/",
    ),
    100: HotelPhoto(
        "https://media.booking-channel.com/api/hotels/2992/images/83.jpeg",
        "https://www.eurostarshotels.co.uk/eurostars-casa-anfa.html",
    ),
    101: HotelPhoto(
        "https://exe.hotels-in-casablanca.com/data/Photos/1080x700w/16684/1668460/1668460208.JPEG",
        "https://exe.hotels-in-casablanca.com/en/",
    ),
    102: HotelPhoto(
        "https://images.trvl-media.com/lodging/75000000/74040000/74035500/74035471/0092e515.jpg?h=201&impolicy=fcrop&p=1&q=medium&w=469",
        "https://www.hilton.com/en/hotels/casasgi-hilton-garden-inn-casablanca-sud/",
    ),
    103: HotelPhoto(
        "https://photos.smugmug.com/Maroc-Lovers/Casablanca/Hotels/Other-Hotels/i-9zs6QzS/0/NgC2N7g9NdX5XgtG2PbSbP3fvPmnZW3ZgctNcnkpb/L/jm-suites-ecofriendly-hotel-casablanca-lobby-L.jpg",
        "https://maroclovers.com/en/where-stay-casablanca-best-hotels-neighborhoods/",
    ),
    104: HotelPhoto(
        "https://images.trvl-media.com/lodging/1000000/50000/46300/46282/20479b1a.jpg?impolicy=resizecrop&ra=fit&rw=598",
        "https://www.hotels.com/ho233220/kaan-casablanca/",
    ),
    106: HotelPhoto(
        "https://images.trvl-media.com/lodging/103000000/102770000/102761800/102761796/b12c681b.jpg?h=201&impolicy=fcrop&p=1&q=medium&w=469",
        "https://www.radissonhotels.com/en-us/hotels/radisson-gauthierlacitadelle-casablanca",
    ),
    107: HotelPhoto(
        "https://silver-suitesspa.hotels-in-casablanca.com/data/Photos/1080x700w/15522/1552211/1552211644/casablanca-silver-suites-hotel-casablanca-photo-1.JPEG",
        "https://silver-suitesspa.hotels-in-casablanca.com/en/",
    ),
    108: HotelPhoto(
        "https://images.trvl-media.com/lodging/13000000/12900000/12895000/12894999/07e89db2.jpg?impolicy=resizecrop&ra=fit&rw=598",
        "https://www.hotels.com/ho560709/the-fourteen-luxury-boutique-hotel-spa-casablanca-morocco/",
    ),
    109: HotelPhoto(
        "https://best-western-toubkal.hotels-in-casablanca.com/data/Photos/1080x700w/11443/1144340/1144340331.JPEG",
        "https://best-western-toubkal.hotels-in-casablanca.com/en/",
    ),
    111: HotelPhoto(
        "https://images.trvl-media.com/lodging/12000000/11970000/11970000/11969964/73304f12.jpg?impolicy=resizecrop&ra=fit&rw=598",
        "https://www.hotels.com/ho384038848/hotel-yto-casablanca-morocco/",
    ),
    112: HotelPhoto(
        "https://www.ahstatic.com/photos/a0g3_ho_00_p_1024x768.jpg",
        "https://all.accor.com/hotel/A0G3/index.en.shtml",
    ),
    114: HotelPhoto(
        "https://olympic-inn.hotels-in-casablanca.com/data/Pics/1080x700w/16353/1635358/1635358701/olympic-inn-casablanca-casablanca-pic-1.JPEG",
        "https://olympic-inn.hotels-in-casablanca.com/en/",
    ),
    117: HotelPhoto(
        "https://images.trvl-media.com/lodging/100000000/99580000/99570200/99570111/73d0912b.jpg?impolicy=resizecrop&ra=fit&rw=598",
        "https://www.hotels.com/ho3187243552/unico-hotel-casablanca-morocco/",
    ),
}


def hotel_image_for(hotel_id: int) -> str:
    photo = REAL_HOTEL_PHOTOS.get(hotel_id)
    if photo is not None:
        return photo.image_url
    return FALLBACK_HOTEL_IMAGES[(hotel_id - 1) % len(FALLBACK_HOTEL_IMAGES)]
