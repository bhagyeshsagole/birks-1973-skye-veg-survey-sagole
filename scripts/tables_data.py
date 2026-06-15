"""Hand-read transcriptions of Birks tables 4.2-4.11 (images 2-11).

Each table: releves list (ordered, one per column) + species list whose `cells`
align to the releve order. Cell values are the printed symbols: a Domin digit,
"." (absent), "+" (low), or "x" (presence mark). The builder expands these into
long-format observation rows via the real pipeline normalization functions.

All sites are Isle of Skye, so os_grid_square is "NG" throughout.
"""

NG = "NG"


def releve(rid, ref, mapref, alt, asp, slope, cover, area, sprep):
    return {
        "releve_id": str(rid),
        "ref_code": ref,
        "map_reference": mapref,
        "os_grid_square": NG,
        "altitude_ft": str(alt),
        "aspect_deg": str(asp),
        "slope_deg": str(slope),
        "cover_pct": str(cover),
        "plot_area_m2": str(area),
        "species_reported": str(sprep),
    }


TABLE_4_2 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_2.png",
    "table_id_raw": "Table 4.2",
    "class": "THLASPIETEA ROTUNDIFOLII",
    "order": "ANDROSACETALIA ALPINAE",
    "alliance": "Androsacion alpinae",
    "association": "Koenigia islandica scree community",
    "n_releves": "4",
    "total_species": "27",
    "mean_species": "14",
    "releves": [
        releve(1, "B68-033", "499540", 1600, 90, 45, 10, 4, 13),
        releve(2, "B67-131", "456618", 1750, 90, 60, 10, 4, 14),
        releve(3, "B66-002", "500540", 1600, 90, 35, 20, 4, 12),
        releve(4, "B67-129", "456613", 1600, 90, 20, 40, 4, 17),
    ],
    "species": [
        {"name": "Agrostis canina", "cells": ["3", "4", "x", "5"]},
        {"name": "Festuca vivipara", "cells": ["5", "6", "x", "5"]},
        {"name": "Poa glauca", "cells": ["3", ".", "x", "."]},
        {"name": "Carex demissa", "cells": [".", ".", ".", "3"]},
        {"name": "Luzula spicata", "cells": [".", "3", ".", "1"]},
        {"name": "Alchemilla alpina", "cells": ["6", "4", "x", "5"]},
        {"name": "Cardaminopsis petraea", "cells": ["3", "2", "x", "5"]},
        {"name": "Cerastium holosteoides", "cells": [".", "3", "x", "."]},
        {"name": "Cherleria sedoides", "cells": [".", "2", ".", "."]},
        {"name": "Galium saxatile", "cells": [".", ".", ".", "3"]},
        {"name": "Koenigia islandica", "cells": ["7", "5", "x", "4"]},
        {"name": "Oxyria digyna", "cells": ["+", ".", ".", "."]},
        {"name": "Sagina subulata", "cells": ["3", "3", "x", "."]},
        {"name": "Saxifraga hypnoides", "cells": [".", "x", ".", "."]},
        {"name": "S. stellaris", "cells": [".", ".", ".", "2"]},
        {"name": "Sibbaldia procumbens", "cells": [".", ".", ".", "5"]},
        {"name": "Silene acaulis", "cells": [".", "2", ".", "2"]},
        {"name": "Thymus drucei", "cells": ["4", "1", "x", "5"]},
        {"name": "Viola riviniana", "cells": ["3", ".", ".", "."]},
        {"name": "Andreaea rothii", "cells": [".", ".", ".", "2"]},
        {"name": "Oligotrichum hercynicum", "cells": ["3", "3", "x", "2"]},
        {"name": "Polytrichum urnigerum", "cells": [".", "2", ".", "."]},
        {"name": "Rhacomitrium canescens", "cells": ["3", ".", "x", "."]},
        {"name": "R. ellipticum", "cells": [".", ".", ".", "1"]},
        {"name": "R. lanuginosum", "cells": [".", ".", ".", "2"]},
        {"name": "Nardia scalaris", "cells": ["+", ".", "x", "."]},
        {"name": "Stereocaulon vesuvianum", "cells": [".", ".", ".", "1"]},
    ],
}


TABLE_4_3 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_3.png",
    "table_id_raw": "Table 4.3",
    "class": "ASPLENIETEA RUPESTRIS",
    "order": "POTENTILLETALIA CAULESCENTIS",
    "alliance": "Potentillion caulescentis",
    "association": "Asplenium marinum-Grimmia maritima",
    "n_releves": "8",
    "total_species": "20",
    "mean_species": "6.7",
    "releves": [
        releve(1, "B68-147", "141477", 100, 90, 80, 60, 1, 7),
        releve(2, "B68-158", "504444", 30, 135, 90, 50, 0.5, 5),
        releve(3, "B68-211", "583189", 25, 270, 75, 60, 2, 8),
        releve(4, "B68-088", "558157", 10, 90, 80, 80, 4, 6),
        releve(5, "B68-323", "508186", 30, 90, 90, 100, 1, 6),
        releve(6, "B68-004", "410762", 50, 315, 80, 50, 1, 8),
        releve(7, "B68-200", "222613", 5, 0, 90, 40, 0.5, 6),
        releve(8, "B68-202", "323385", 20, 270, 80, 60, 2, 8),
    ],
    "species": [
        {"name": "Asplenium adiantum-nigrum", "cells": [".", ".", ".", ".", ".", ".", "3", "8"], "C": "II", "D": "1.4"},
        {"name": "A. marinum", "cells": ["9", "8", "8", "8", "9", "8", "8", "."], "C": "V", "D": "7.3"},
        {"name": "Festuca rubra", "cells": [".", "4", "4", "3", ".", "4", "3", "4"], "C": "IV", "D": "2.8"},
        {"name": "Armeria maritima", "cells": ["3", ".", "5", ".", "4", ".", "4", "4"], "C": "IV", "D": "2.5"},
        {"name": "Ligusticum scoticum", "cells": ["2", ".", "2", ".", ".", ".", ".", "."], "C": "II", "D": "0.5"},
        {"name": "Plantago maritima", "cells": [".", ".", ".", ".", "1", "2", "5", "3"], "C": "III", "D": "1.4"},
        {"name": "Tripleurospermum maritimum", "cells": ["4", ".", ".", "3", ".", "3", ".", "."], "C": "II", "D": "1.3"},
        {"name": "Grimmia maritima", "cells": ["2", "3", ".", "3", "4", "3", "3", "4"], "C": "V", "D": "2.8"},
        {"name": "*Trichostomum brachydontium", "cells": ["3", "2", "3", "4", "3", "2", ".", "3"], "C": "V", "D": "2.5"},
    ],
}


TABLE_4_5 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_5.png",
    "table_id_raw": "Table 4.5",
    "class": "PLANTAGINETEA MAJORIS",
    "order": "PLANTAGINETALIA MAJORIS",
    "alliance": "Lolio-Plantaginion",
    "association": "Lolium perenne-Plantago major",
    "n_releves": "8",
    "total_species": "49",
    "mean_species": "15.9",
    "releves": [
        releve(1, "B68-088", "518605", 300, "", "", 100, 4, 17),
        releve(2, "B68-206", "377364", 300, "", "", 100, 4, 20),
        releve(3, "B68-256", "611203", 50, "", "", 100, 4, 14),
        releve(4, "B68-287", "554166", 50, "", "", 100, 4, 12),
        releve(5, "B68-346", "532323", 50, "", "", 100, 4, 11),
        releve(6, "B68-358", "696116", 75, "", "", 90, 4, 9),
        releve(7, "B68-362", "672099", 100, "", "", 100, 4, 16),
        releve(8, "B68-052", "478388", 120, "", "", 80, 4, 28),
    ],
    "species": [
        {"name": "Agrostis stolonifera", "cells": [".", ".", ".", "1", "2", ".", ".", "4"], "C": "II", "D": "0.9"},
        {"name": "A. tenuis", "cells": ["2", ".", ".", ".", ".", ".", "2", "."], "C": "II", "D": "0.9"},
        {"name": "Anthoxanthum odoratum", "cells": [".", ".", ".", "4", ".", "2", ".", "."], "C": "II", "D": "0.8"},
        {"name": "Cynosurus cristatus", "cells": ["5", "4", "4", "3", ".", "4", ".", "2"], "C": "IV", "D": "2.3"},
        {"name": "Festuca ovina", "cells": ["3", ".", ".", ".", ".", ".", ".", "4"], "C": "II", "D": "0.9"},
        {"name": "F. rubra", "cells": ["5", ".", ".", ".", ".", ".", ".", "5"], "C": "II", "D": "1.3"},
        {"name": "Holcus lanatus", "cells": ["2", "5", ".", ".", ".", ".", "4", "."], "C": "II", "D": "1.4"},
        {"name": "Lolium perenne", "cells": ["5", "5", "5", "6", ".", "5", "6", "5"], "C": "V", "D": "5.4"},
        {"name": "Poa annua", "cells": [".", "2", "4", ".", "2", "3", ".", "7"], "C": "IV", "D": "2.3"},
        {"name": "Carex ovalis", "cells": [".", ".", ".", ".", ".", "1", ".", "+"], "C": "II", "D": "0.3"},
        {"name": "Juncus articulatus", "cells": ["2", ".", ".", ".", ".", "2", ".", "."], "C": "II", "D": "0.5"},
        {"name": "Achillea millefolium", "cells": [".", "5", "4", "3", ".", ".", ".", "."], "C": "II", "D": "1.5"},
        {"name": "Bellis perennis", "cells": ["5", "6", "3", "3", ".", "1", "4", "."], "C": "V", "D": "3.3"},
        {"name": "Cerastium holosteoides", "cells": ["2", ".", ".", ".", "1", ".", "3", "."], "C": "III", "D": "0.9"},
        {"name": "Euphrasia brevipila", "cells": [".", ".", ".", "3", ".", ".", ".", "1"], "C": "II", "D": "0.5"},
        {"name": "Plantago lanceolata", "cells": ["3", ".", "4", "1", ".", "3", "3", "+"], "C": "IV", "D": "1.9"},
        {"name": "P. major", "cells": ["6", "5", "8", "8", "6", "7", "8", "6"], "C": "V", "D": "6.8"},
        {"name": "Prunella vulgaris", "cells": ["3", "2", ".", ".", ".", ".", "3", "3"], "C": "III", "D": "1.4"},
        {"name": "Ranunculus repens", "cells": ["3", "3", "1", "2", ".", ".", ".", "2"], "C": "IV", "D": "1.4"},
        {"name": "Rumex acetosella", "cells": [".", "2", ".", "2", ".", ".", "1", "."], "C": "II", "D": "0.6"},
        {"name": "R. obtusifolius", "cells": [".", ".", ".", "3", "2", ".", ".", "."], "C": "II", "D": "0.6"},
        {"name": "Sagina procumbens", "cells": ["2", "3", ".", ".", ".", ".", "3", "."], "C": "II", "D": "1.0"},
        {"name": "Taraxacum officinale agg.", "cells": ["1", ".", "2", ".", "1", ".", ".", "3"], "C": "III", "D": "0.9"},
        {"name": "Thymus drucei", "cells": [".", ".", "2", ".", ".", ".", "3", "2"], "C": "II", "D": "0.5"},
        {"name": "Trifolium repens", "cells": [".", "4", ".", "2", "6", "4", "3", "4"], "C": "IV", "D": "2.9"},
        {"name": "Acrocladium cuspidatum", "cells": ["1", ".", ".", ".", ".", ".", ".", "1"], "C": "II", "D": "0.3"},
        {"name": "Brachythecium rutabulum", "cells": [".", ".", ".", ".", "2", ".", "1", "3"], "C": "II", "D": "0.8"},
        {"name": "Bryum bicolor", "cells": [".", ".", ".", ".", ".", ".", "1", "2"], "C": "II", "D": "0.4"},
        {"name": "Ceratodon purpureus", "cells": [".", ".", ".", ".", "1", "1", "3", "3"], "C": "III", "D": "1.0"},
    ],
}


TABLE_4_9 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_9.png",
    "table_id_raw": "Table 4.9",
    "class": "CAKILETEA MARITIMAE",
    "order": "CAKILETALIA MARITIMAE",
    "alliance": "Atriplicion littoralis",
    "association": "Atriplex glabriuscula-Rumex crispus",
    "n_releves": "9",
    "total_species": "48",
    "mean_species": "13.6",
    "releves": [
        releve(1, "B68-118", "395437", 20, "", "", 50, 16, 11),
        releve(2, "B68-153", "260566", 20, "", "", 70, 4, 18),
        releve(3, "B68-140", "415520", 15, "", "", 50, 16, 12),
        releve(4, "B68-198", "222612", 10, "", "", 100, 4, 13),
        releve(5, "B68-201", "323385", 25, "", "", 100, 4, 19),
        releve(6, "B68-038", "376663", 5, "", "", 80, 4, 13),
        releve(7, "B68-128", "596268", 10, "", "", 40, 4, 9),
        releve(8, "B68-036", "375661", 60, "", "", 60, 4, 15),
        releve(9, "B68-037", "376663", 25, "", "", 75, 4, 13),
    ],
    "species": [
        {"name": "Equisetum arvense", "cells": [".", "1", ".", ".", ".", "3", ".", ".", "+"], "C": "II", "D": "0.6"},
        {"name": "Agrostis stolonifera", "cells": [".", ".", "+", "3", "3", "2", ".", ".", "."], "C": "III", "D": "1.0"},
        {"name": "Agropyron repens", "cells": [".", "2", ".", "2", ".", ".", ".", ".", "."], "C": "II", "D": "0.4"},
        {"name": "Festuca rubra", "cells": ["2", ".", "3", "4", "3", "3", ".", ".", "."], "C": "III", "D": "1.6"},
        {"name": "Holcus lanatus", "cells": [".", "3", ".", ".", "1", ".", ".", ".", "."], "C": "II", "D": "0.4"},
        {"name": "Juncus bufonius", "cells": [".", "2", ".", ".", "+", "3", ".", "3", "."], "C": "III", "D": "1.0"},
        {"name": "J. gerardii", "cells": [".", ".", ".", ".", ".", ".", "3", "3", "3"], "C": "II", "D": "1.4"},
        {"name": "Scirpus maritimus", "cells": [".", ".", ".", ".", ".", ".", "7", "6", "."], "C": "II", "D": "0.7"},
        {"name": "Triglochin maritima", "cells": ["+", ".", ".", ".", ".", ".", "2", ".", "."], "C": "II", "D": "0.5"},
        {"name": "Armeria maritima", "cells": ["+", "3", "4", "2", "+", ".", "4", ".", "."], "C": "IV", "D": "1.7"},
        {"name": "Atriplex glabriuscula", "cells": ["8", "7", "6", "4", "6", "6", "7", "4", "3"], "C": "V", "D": "5.9"},
        {"name": "Cochlearia officinalis agg.", "cells": [".", ".", "2", ".", ".", ".", "1", ".", "."], "C": "II", "D": "0.5"},
        {"name": "Galium aparine", "cells": ["2", "3", "4", ".", "4", ".", ".", "2", "3"], "C": "V", "D": "3.1"},
        {"name": "Glaux maritima", "cells": ["3", "1", ".", "4", ".", ".", "3", ".", "."], "C": "III", "D": "1.2"},
        {"name": "Leontodon autumnalis", "cells": [".", ".", ".", ".", "2", "1", ".", ".", "."], "C": "II", "D": "0.3"},
        {"name": "Ligusticum scoticum", "cells": [".", ".", ".", "5", "1", ".", ".", ".", "."], "C": "II", "D": "0.7"},
        {"name": "Lycopus europaeus", "cells": [".", "2", ".", ".", "+", ".", ".", ".", "."], "C": "II", "D": "0.3"},
        {"name": "Plantago maritima", "cells": [".", ".", "3", ".", ".", ".", ".", "+", "."], "C": "II", "D": "0.4"},
        {"name": "Polygonum persicaria", "cells": ["1", "+", ".", ".", ".", ".", ".", ".", "."], "C": "I", "D": "0.2"},
        {"name": "Rumex crispus var. triangulatus", "cells": ["4", "5", "5", "7", ".", "3", "3", "3", "3"], "C": "V", "D": "4.3"},
        {"name": "Sonchus arvensis", "cells": [".", "5", ".", ".", ".", ".", ".", ".", "+"], "C": "II", "D": "0.7"},
        {"name": "Stellaria media", "cells": ["5", "4", "4", "5", "3", ".", "6", "+", "+"], "C": "V", "D": "2.9"},
        {"name": "Tripleurospermum maritimum", "cells": ["3", "3", "3", "1", "8", ".", ".", ".", "+"], "C": "IV", "D": "1.7"},
    ],
}


TABLE_4_10 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_10.png",
    "table_id_raw": "Table 4.10",
    "class": "LITTORELLETEA",
    "order": "LITTORELLETALIA",
    "alliance": "Littorellion uniflorae",
    "association": "Littorella uniflora-Lobelia dortmanna",
    "n_releves": "11",
    "total_species": "18",
    "mean_species": "6.6",
    "releves": [
        releve(1, "B68-354", "590106", 250, "", "", 50, 4, 4),
        releve(2, "B68-025", "472306", 300, "", "", 20, 4, 6),
        releve(3, "B68-044", "502652", 250, "", "", 40, 4, 6),
        releve(4, "B68-175", "222412", 800, "", "", 50, 4, 4),
        releve(5, "B68-225", "679205", 150, "", "", 50, 4, 7),
        releve(6, "B68-327", "685205", 200, "", "", 50, 4, 7),
        releve(7, "B68-253", "666205", 50, "", "", 50, 4, 8),
        releve(8, "B68-078", "416182", 275, "", "", 50, 4, 8),
        releve(9, "B68-291", "676105", 200, "", "", 100, 4, 9),
        releve(10, "B68-295", "696113", 350, "", "", 100, 4, 8),
        releve(11, "B68-296", "657110", 350, "", "", 100, 4, 5),
    ],
    "species": [
        {"name": "Equisetum fluviatile", "cells": [".", ".", "+", ".", ".", "5", ".", ".", ".", "+", "."], "C": "II", "D": "0.6"},
        {"name": "Isoetes lacustris", "cells": [".", "3", ".", ".", ".", ".", ".", ".", ".", ".", "."], "C": "I", "D": "0.7"},
        {"name": "Baldellia ranunculoides", "cells": [".", ".", ".", ".", ".", "4", "5", "2", ".", ".", "."], "C": "II", "D": "1.0"},
        {"name": "Carex nigra", "cells": [".", ".", ".", ".", "4", ".", ".", "2", ".", ".", "."], "C": "II", "D": "0.9"},
        {"name": "Eleocharis palustris", "cells": [".", ".", ".", ".", ".", ".", "4", "5", "4", "3", "."], "C": "III", "D": "2.1"},
        {"name": "Eleogiton fluitans", "cells": [".", ".", ".", ".", ".", ".", "3", "5", "3", ".", "."], "C": "II", "D": "1.0"},
        {"name": "Juncus articulatus", "cells": ["5", "3", "4", ".", ".", "3", "4", "4", ".", "1", "."], "C": "IV", "D": "2.3"},
        {"name": "J. bulbosus", "cells": ["1", ".", ".", "4", "6", "3", ".", ".", "2", "5", "3"], "C": "IV", "D": "2.6"},
        {"name": "J. effusus", "cells": [".", ".", ".", "2", "+", ".", ".", ".", ".", ".", "."], "C": "I", "D": "0.3"},
        {"name": "Littorella uniflora", "cells": ["9", "5", "9", "5", ".", ".", "8", "5", "7", "7", "7"], "C": "V", "D": "5.3"},
        {"name": "Lobelia dortmanna", "cells": [".", "7", "3", "8", "8", "8", ".", "5", "6", ".", "."], "C": "V", "D": "5.1"},
        {"name": "Myriophyllum alterniflorum", "cells": [".", ".", "+", ".", ".", ".", "3", ".", ".", "2", "."], "C": "II", "D": "0.6"},
        {"name": "Ranunculus flammula", "cells": [".", "3", "+", "3", "5", "4", ".", ".", "2", "+", "3"], "C": "IV", "D": "2.3"},
    ],
}


TABLE_4_11 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_11.png",
    "table_id_raw": "Table 4.11",
    "class": "POTAMETEA",
    "order": "MAGNOPOTAMETALIA",
    "alliance": "Nymphaeion albae",
    "association": "Potamogeton natans-Nymphaea alba",
    "n_releves": "6",
    "total_species": "13",
    "mean_species": "5.5",
    "notes": "Water depth (cm) by releve: 75, 90, 90, 75, 70, 52.",
    "releves": [
        releve(1, "B68-292", "676106", 200, "", "", 100, 4, 5),
        releve(2, "B68-224", "679205", 150, "", "", 90, 4, 3),
        releve(3, "B68-023", "472306", 300, "", "", 75, 4, 8),
        releve(4, "B68-043", "502652", 250, "", "", 50, 4, 5),
        releve(5, "B68-067", "494487", 450, "", "", 50, 4, 7),
        releve(6, "B68-194", "233605", 200, "", "", 90, 4, 5),
    ],
    "species": [
        {"name": "Equisetum fluviatile", "cells": ["3", "3", "3", "3", ".", "."], "C": "IV", "D": "2.0"},
        {"name": "Eleogiton fluitans", "cells": ["5", ".", ".", ".", "5", "."], "C": "II", "D": "1.7"},
        {"name": "Potamogeton natans", "cells": [".", "7", "7", "8", "8", "5"], "C": "V", "D": "5.8"},
        {"name": "P. polygonifolius", "cells": [".", ".", ".", "3", "2", "7"], "C": "III", "D": "2.0"},
        {"name": "Sparganium angustifolium", "cells": ["7", ".", ".", "5", "3", "4"], "C": "IV", "D": "3.2"},
        {"name": "Myriophyllum alterniflorum", "cells": ["3", ".", ".", "+", "4", "5"], "C": "IV", "D": "2.2"},
        {"name": "Nymphaea alba", "cells": ["6", "8", "6", ".", "3", "."], "C": "IV", "D": "3.8"},
        {"name": "Chara spp.", "cells": [".", ".", "2", ".", ".", "3"], "C": "II", "D": "0.8"},
        {"name": "Carex rostrata", "cells": [".", ".", "4", ".", ".", "."]},
        {"name": "Juncus bulbosus", "cells": [".", ".", "3", ".", ".", "."]},
        {"name": "Sparganium minimum", "cells": [".", ".", "+", ".", ".", "."]},
        {"name": "Menyanthes trifoliata", "cells": [".", ".", "4", ".", ".", "."]},
        {"name": "Callitriche stagnalis", "cells": [".", ".", ".", ".", "+", "."]},
    ],
}


# Table 4.6 holds two sub-tables (different alliances) on one page, each with a
# two-panel side-by-side species layout. Modelled as two entries, same table_id.
TABLE_4_6A = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_6.png",
    "table_id_raw": "Table 4.6",
    "class": "AMMOPHILETEA",
    "order": "ELYMO-AMMOPHILETALIA ARENARIAE",
    "alliance": "Agropyrion boreoatlanticum",
    "association": "Fore-dune communities",
    "n_releves": "2",
    "total_species": "",
    "releves": [
        releve(1, "B68-347", "412205", "", "", "", 90, 4, ""),
        releve(2, "B68-365", "412205", "", "", "", 80, 4, ""),
    ],
    "species": [
        {"name": "Agropyron junceiforme", "cells": ["8", "7"]},
        {"name": "Agrostis stolonifera", "cells": ["3", "3"]},
        {"name": "Ammophila arenaria", "cells": [".", "4"]},
        {"name": "Festuca rubra", "cells": ["4", "5"]},
        {"name": "Carex arenaria", "cells": ["6", "5"]},
        {"name": "Cirsium vulgare", "cells": ["2", "+"]},
        {"name": "Honkenya peploides", "cells": ["5", "4"]},
        {"name": "Lotus corniculatus", "cells": ["4", "2"]},
        {"name": "Potentilla anserina", "cells": ["5", "4"]},
        {"name": "Rumex crispus", "cells": ["+", "."]},
        {"name": "Sonchus asper", "cells": ["3", "3"]},
    ],
}

TABLE_4_6B = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_6.png",
    "table_id_raw": "Table 4.6",
    "class": "AMMOPHILETEA",
    "order": "ELYMO-AMMOPHILETALIA ARENARIAE",
    "alliance": "Ammophilion borealis",
    "association": "Grey dune Turfs",
    "n_releves": "2",
    "total_species": "",
    "releves": [
        releve(3, "B68-349", "412222", "", "", "", 60, 4, ""),
        releve(4, "B68-366", "412220", "", "", "", 80, 4, ""),
    ],
    "species": [
        {"name": "Festuca rubra", "cells": ["7", "8"]},
        {"name": "Achillea millefolium", "cells": ["5", "3"]},
        {"name": "Centaurea nigra", "cells": ["3", "3"]},
        {"name": "Galium verum", "cells": ["6", "5"]},
        {"name": "Heracleum sphondylium", "cells": ["+", "."]},
        {"name": "Leontodon autumnalis", "cells": ["2", "."]},
        {"name": "Lotus corniculatus", "cells": ["4", "5"]},
        {"name": "Plantago lanceolata", "cells": ["3", "1"]},
        {"name": "Sedum acre", "cells": ["1", "3"]},
        {"name": "Senecio jacobea", "cells": ["2", "1"]},
        {"name": "Thalictrum minus", "cells": ["4", "3"]},
        {"name": "Trifolium repens", "cells": ["3", "2"]},
        {"name": "Bryum argenteum", "cells": ["1", "."]},
        {"name": "B. capillare", "cells": ["1", "3"]},
        {"name": "Tortula ruraliformis", "cells": ["2", "2"]},
    ],
}


# Table 4.7 = Puccinellietum maritimae with two subassociations side by side,
# each with its own constancy (C) and mean (D) columns. Split by subassociation:
# 4.7A = releves 1-6 (Asplenium nodosum subass.), 4.7B = releves 7-12 (Festuca rubra subass.).
TABLE_4_7A = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_7.png",
    "table_id_raw": "Table 4.7",
    "class": "ASTERETEA TRIPOLIUM",
    "order": "GLAUCETO-PUCCINELLIETALIA",
    "alliance": "Puccinellion maritimae",
    "association": "Puccinellietum maritimae (Puccinellia-Asplenium nodosum subass.)",
    "n_releves": "6",
    "total_species": "20",
    "mean_species": "5.8",
    "releves": [
        releve(1, "B68-133", "540273", "", "", "", 100, 4, 5),
        releve(2, "B68-134", "540273", "", "", "", 100, 4, 5),
        releve(3, "B68-289", "565222", "", "", "", 100, 4, 5),
        releve(4, "B68-277", "703158", "", "", "", 100, 4, 6),
        releve(5, "B68-357", "699116", "", "", "", 100, 4, 6),
        releve(6, "B68-205", "323385", "", "", "", 100, 4, 8),
    ],
    "species": [
        {"name": "Festuca rubra", "cells": [".", ".", ".", ".", ".", "."], "C": "", "D": ""},
        {"name": "Puccinellia maritima", "cells": ["8", "8", "8", "7", "6", "8"], "C": "V", "D": "7.5"},
        {"name": "Armeria maritima", "cells": ["5", "4", "5", "8", "3", "7"], "C": "V", "D": "5.3"},
        {"name": "Aster tripolium", "cells": [".", ".", ".", ".", "2", "7"], "C": "II", "D": "1.5"},
        {"name": "Euphrasia officinalis agg.", "cells": [".", ".", ".", ".", ".", "."], "C": "", "D": ""},
        {"name": "Glaux maritima", "cells": ["4", "5", "5", "4", "3", "5"], "C": "V", "D": "4.3"},
        {"name": "Leontodon autumnalis", "cells": [".", ".", ".", ".", ".", "."], "C": "", "D": ""},
        {"name": "Plantago coronopus", "cells": [".", ".", ".", ".", ".", "."], "C": "", "D": ""},
        {"name": "P. lanceolata", "cells": [".", ".", ".", ".", ".", "."], "C": "", "D": ""},
        {"name": "P. maritima", "cells": ["6", "6", "5", "5", "7", "3"], "C": "V", "D": "5.3"},
        {"name": "Spergularia media", "cells": [".", ".", ".", "3", ".", "4"], "C": "II", "D": "1.2"},
        {"name": "Trichostomum brachydontium", "cells": [".", ".", ".", ".", ".", "."], "C": "", "D": ""},
        {"name": "Ascophyllum nodosum", "cells": ["7", "5", "6", "5", "3", "."], "C": "V", "D": "4.3"},
    ],
}

TABLE_4_7B = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_7.png",
    "table_id_raw": "Table 4.7",
    "class": "ASTERETEA TRIPOLIUM",
    "order": "GLAUCETO-PUCCINELLIETALIA",
    "alliance": "Puccinellion maritimae",
    "association": "Puccinellietum maritimae (Puccinellia-Festuca rubra subass.)",
    "n_releves": "6",
    "total_species": "20",
    "mean_species": "7.3",
    "releves": [
        releve(7, "B68-058", "495305", "", "", "", 90, 4, 5),
        releve(8, "B68-142", "416519", "", "", "", 100, 4, 5),
        releve(9, "B68-141", "415520", "", "", "", 100, 4, 7),
        releve(10, "B68-057", "495305", "", "", "", 95, 4, 7),
        releve(11, "B68-092", "527627", 75, "", "", 75, 4, 10),
        releve(12, "B68-093", "527627", 60, "", "", 100, 4, 10),
    ],
    "species": [
        {"name": "Festuca rubra", "cells": ["3", "6", "5", "5", "4", "5"], "C": "V", "D": "4.6"},
        {"name": "Puccinellia maritima", "cells": ["6", "8", "7", "5", "9", "7"], "C": "V", "D": "7.0"},
        {"name": "Armeria maritima", "cells": ["8", "5", "4", "3", "5", "3"], "C": "V", "D": "4.7"},
        {"name": "Aster tripolium", "cells": [".", ".", ".", ".", ".", "."], "C": "", "D": ""},
        {"name": "Euphrasia officinalis agg.", "cells": [".", ".", ".", "+", "2", "3"], "C": "II", "D": "0.8"},
        {"name": "Glaux maritima", "cells": ["5", "5", "3", "+", ".", "."], "C": "IV", "D": "2.3"},
        {"name": "Leontodon autumnalis", "cells": [".", ".", ".", "+", "+", "."], "C": "II", "D": "0.3"},
        {"name": "Plantago coronopus", "cells": [".", ".", ".", ".", "4", "4"], "C": "II", "D": "1.3"},
        {"name": "P. lanceolata", "cells": [".", ".", ".", ".", "2", "4"], "C": "II", "D": "1.0"},
        {"name": "P. maritima", "cells": ["4", "5", "4", "9", "6", "4"], "C": "V", "D": "5.3"},
        {"name": "Spergularia media", "cells": [".", ".", "4", ".", ".", "."], "C": "I", "D": "0.7"},
        {"name": "Trichostomum brachydontium", "cells": [".", ".", ".", ".", "3", "3"], "C": "II", "D": "1.0"},
        {"name": "Ascophyllum nodosum", "cells": [".", ".", ".", ".", ".", "."], "C": "", "D": ""},
    ],
}


TABLE_4_4 = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_4.png",
    "table_id_raw": "Table 4.4",
    "class": "ASPLENIETEA RUPESTRIS",
    "order": "POTENTILLETALIA CAULESCENTIS",
    "alliance": "Potentillion caulescentis",
    "association": "Asplenium trichomanes-Fissidens cristatus",
    "n_releves": "14",
    "total_species": "86",
    "mean_species": "16.8",
    "releves": [
        releve(1, "B68-152", "272531", 50, 90, 90, 100, 0.5, 11),
        releve(2, "B68-191", "317507", 200, 45, 75, 80, 2, 15),
        releve(3, "B68-207", "377364", 300, 45, 80, 80, 4, 12),
        releve(4, "B68-208", "377364", 300, 90, 90, 100, 4, 21),
        releve(5, "B68-159", "504444", 150, 180, 90, 50, 2, 8),
        releve(6, "B68-154", "154446", 250, 90, 50, 50, 4, 18),
        releve(7, "B68-217", "584187", 75, 270, 80, 100, 2, 15),
        releve(8, "B68-304", "618195", 100, 315, 80, 100, 1, 21),
        releve(9, "B68-257", "611200", 75, 90, 75, 100, 2, 16),
        releve(10, "B68-301", "615120", 300, 0, 80, 100, 1, 15),
        releve(11, "B68-231", "558217", 120, 0, 90, 100, 2, 22),
        releve(12, "B68-230", "560217", 100, 315, 90, 100, 2, 15),
        releve(13, "B68-236", "539216", 1500, 315, 80, 100, 2, 22),
        releve(14, "B68-238", "537213", 1600, "", 75, 100, 2, 24),
    ],
    "species": [
        {"name": "Asplenium ruta-muraria", "cells": [".", ".", ".", ".", "7", "5", "4", "5", "7", "3", ".", ".", ".", "."], "C": "III", "D": "2.2"},
        {"name": "A. trichomanes", "cells": ["8", "7", "8", "8", "6", "6", "7", "7", "5", "7", "7", "3", "3", "6"], "C": "V", "D": "6.6"},
        {"name": "A. viride", "cells": [".", ".", ".", ".", ".", ".", "5", "6", "2", "3", "6", "8", "7", "7"], "C": "III", "D": "2.8"},
        {"name": "Cystopteris fragilis", "cells": [".", ".", ".", ".", ".", ".", "3", "+", "4", "5", "+", "4", "3", "."], "C": "III", "D": "1.5"},
        {"name": "Phyllitis scolopendrium", "cells": [".", ".", ".", ".", ".", ".", "1", "2", ".", "2", "4", ".", ".", "."], "C": "II", "D": "0.6"},
        {"name": "Polystichum aculeatum", "cells": [".", "3", ".", ".", "1", ".", "3", "1", ".", "1", ".", ".", ".", "."], "C": "II", "D": "0.6"},
        {"name": "P. lonchitis", "cells": [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "3", "4", "1"], "C": "II", "D": "0.5"},
        {"name": "Selaginella selaginoides", "cells": [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "3", "1", "3"], "C": "I", "D": "0.3"},
        {"name": "Arrhenatherum elatius", "cells": [".", ".", ".", ".", "3", "3", "3", ".", ".", ".", ".", ".", ".", "."], "C": "II", "D": "0.6"},
        {"name": "Festuca ovina", "cells": ["2", "3", "3", "3", "5", "5", "2", "3", ".", "2", "1", ".", "4", "2"], "C": "V", "D": "2.5"},
        {"name": "Allium ursinum", "cells": [".", ".", ".", ".", ".", ".", ".", "2", ".", ".", ".", ".", ".", "."], "C": "I", "D": "0.4"},
        {"name": "Carex pulicaris", "cells": ["2", ".", ".", ".", ".", ".", "2", ".", ".", ".", ".", ".", ".", "."], "C": "I", "D": "0.1"},
        {"name": "Chrysosplenium oppositifolium", "cells": [".", ".", "4", "3", ".", ".", ".", ".", ".", "2", ".", ".", "1", "."], "C": "II", "D": "0.7"},
        {"name": "Geranium robertianum", "cells": [".", ".", "4", "2", "4", "3", "4", "3", ".", "3", ".", ".", ".", "."], "C": "III", "D": "1.4"},
        {"name": "Epilobium montanum", "cells": [".", "2", ".", "2", ".", ".", ".", "1", ".", "1", ".", ".", ".", "."], "C": "II", "D": "0.4"},
        {"name": "Fragaria vesca", "cells": [".", "3", ".", "4", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "C": "I", "D": "0.5"},
        {"name": "Linum catharticum", "cells": [".", ".", ".", ".", ".", ".", "3", "2", "+", ".", ".", ".", ".", "."], "C": "II", "D": "0.4"},
        {"name": "Oxalis acetosella", "cells": ["2", "2", "4", "3", ".", ".", ".", ".", ".", ".", ".", "2", ".", "."], "C": "II", "D": "1.1"},
        {"name": "Thymus drucei", "cells": ["1", ".", ".", ".", ".", "1", "3", "3", ".", ".", ".", ".", ".", "."], "C": "II", "D": "0.6"},
        {"name": "Anoectangium aestivum", "cells": [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "4", "4", ".", "."], "C": "I", "D": "0.6"},
        {"name": "Camptothecium sericeum", "cells": ["1", ".", ".", ".", ".", "5", "1", ".", ".", ".", ".", ".", "4", "."], "C": "II", "D": "0.5"},
        {"name": "Ctenidium molluscum", "cells": [".", ".", ".", ".", ".", ".", "5", "1", "6", "6", "6", "5", ".", "."], "C": "III", "D": "2.5"},
        {"name": "Eucladium verticillatum", "cells": [".", ".", ".", ".", ".", "2", ".", ".", ".", "2", ".", ".", ".", "."], "C": "I", "D": "0.3"},
        {"name": "Fissidens cristatus", "cells": ["4", "2", "3", "3", "2", "3", "4", ".", ".", ".", ".", "3", "3", "."], "C": "V", "D": "3.4"},
        {"name": "Isopterygium pulchellum", "cells": [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "2", "3", "."], "C": "I", "D": "0.5"},
        {"name": "Neckera complanata", "cells": [".", ".", ".", ".", ".", ".", "4", ".", ".", ".", "4", ".", "1", "."], "C": "II", "D": "0.5"},
        {"name": "N. crispa", "cells": [".", ".", ".", ".", ".", ".", "4", "3", ".", ".", ".", "1", "3", "."], "C": "II", "D": "0.4"},
        {"name": "Orthothecium rufescens", "cells": [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "1", "1", "3", "1"], "C": "II", "D": "0.4"},
        {"name": "Pohlia cruda", "cells": [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "5", ".", "4", "."], "C": "I", "D": "0.4"},
        {"name": "Thamnium alopecurum", "cells": [".", ".", "2", ".", ".", ".", ".", ".", "3", "2", "1", ".", ".", "."], "C": "II", "D": "0.5"},
        {"name": "Tortella tortuosa", "cells": [".", ".", ".", ".", ".", ".", "3", "3", "4", "3", ".", ".", "6", "."], "C": "III", "D": "1.5"},
        {"name": "Trichostomum crispulum", "cells": [".", ".", ".", ".", ".", ".", "3", "3", ".", "1", ".", "3", ".", "."], "C": "III", "D": "1.0"},
        {"name": "Cololejeunea calcarea", "cells": [".", ".", ".", ".", ".", ".", ".", ".", "1", "2", ".", ".", "4", "."], "C": "I", "D": "0.2"},
        {"name": "Conocephalum conicum", "cells": [".", ".", "3", "3", ".", ".", ".", ".", ".", "3", ".", "1", ".", "."], "C": "II", "D": "0.5"},
        {"name": "Frullania tamarisci", "cells": ["3", ".", "1", ".", ".", ".", ".", ".", ".", ".", ".", ".", "1", "."], "C": "I", "D": "0.3"},
        {"name": "Lejeunea cavifolia", "cells": ["3", "1", "3", "3", ".", ".", ".", ".", "3", ".", ".", "1", ".", "."], "C": "II", "D": "1.0"},
        {"name": "Metzgeria furcata", "cells": [".", "2", "6", "4", ".", ".", ".", ".", "3", ".", ".", "1", ".", "."], "C": "II", "D": "1.0"},
        {"name": "Pellia endiviifolia", "cells": [".", ".", ".", ".", ".", ".", ".", ".", ".", "1", "3", ".", "1", "."], "C": "I", "D": "0.3"},
        {"name": "P. epiphylla", "cells": [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "2", ".", "1", "."], "C": "I", "D": "0.2"},
        {"name": "Plagiochila asplenioides", "cells": [".", "3", "4", "3", ".", ".", "3", "5", ".", ".", "2", "1", "1", "."], "C": "III", "D": "1.6"},
        {"name": "Preissia quadrata", "cells": ["3", ".", ".", ".", ".", ".", "1", ".", ".", "3", "3", ".", "1", "."], "C": "II", "D": "0.7"},
        {"name": "Scapania aspera", "cells": [".", ".", ".", ".", ".", ".", "3", "1", ".", ".", ".", "1", ".", "."], "C": "II", "D": "0.4"},
        {"name": "Gyalecta jenensis", "cells": [".", ".", ".", ".", ".", ".", "2", ".", "2", ".", "3", ".", ".", "2"], "C": "II", "D": "0.6"},
        {"name": "Solorina saccata", "cells": [".", ".", ".", ".", ".", ".", "2", "2", ".", ".", ".", ".", ".", "."], "C": "I", "D": "0.3"},
    ],
}


# Table 4.8 = Asteretea tripolium, Armerion maritimae, printed sideways with 26 releve
# columns in two subassociations. This is the one page where a single visual read leaves
# genuine uncertainty (rotation + many columns + sparse rows), so both halves are flagged
# needs_review. 4.8A = releves 1-17 (Juncus gerardii-Carex extensa), 4.8B = releves 18-26
# (Armeria maritima-Grimmia maritima).
_T48_SPECIES = [
    "Agrostis stolonifera", "Festuca rubra", "Blysmus rufus", "Carex extensa", "C. flacca",
    "C. scandinavica", "Juncus gerardii", "Triglochin maritima", "Armeria maritima",
    "Aster tripolium", "Cochlearia officinalis agg.", "Glaux maritima", "Leontodon autumnalis",
    "Ligusticum scoticum", "Plantago coronopus", "P. maritima", "Sagina maritima",
    "Sedum anglicum", "Spergularia media", "Thymus drucei", "Amblystegium serpens",
    "Grimmia maritima", "Trichostomum brachydontium", "Anaptychia fusca", "Ramalina siliquosa",
    "Xanthoria parietina",
]

# Subassociation 1 (cols 1-17): cells then (C, D).
_T48A = [
    ([".", "4", "3", "3", "4", "4", "3", "3", ".", "3", "3", "4", "4", "4", "5", "3", "."], "V", "3.2"),
    ([".", "3", "4", "3", "2", "5", "4", "2", "3", "4", "3", "4", "4", "6", "3", ".", "5"], "V", "3.3"),
    ([".", ".", "2", ".", ".", ".", ".", "2", "4", "2", ".", "4", ".", ".", ".", "5", "6"], "III", "1.5"),
    ([".", "1", "3", "3", "4", ".", ".", ".", "3", "2", ".", "3", ".", ".", "3", ".", "3"], "III", "1.6"),
    ([".", ".", "2", ".", ".", ".", ".", ".", "2", "2", ".", ".", "3", "4", "3", ".", "1"], "II", "0.6"),
    ([".", ".", "2", ".", ".", ".", "3", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "II", "0.6"),
    (["5", "9", "3", "4", "6", "5", "5", "7", "7", "3", "8", "7", "8", "9", "8", "8", "6"], "V", "6.3"),
    ([".", ".", ".", ".", ".", ".", ".", ".", "1", "3", "3", "3", ".", "2", ".", "4", "+"], "III", "1.1"),
    (["6", "4", "4", "8", "2", "7", "4", "4", "3", "6", "4", "3", "3", "5", "6", "4", "3"], "V", "4.5"),
    ([".", ".", ".", ".", ".", ".", ".", "5", ".", "5", ".", "3", ".", ".", "1", ".", "."], "II", "1.0"),
    (["5", "3", "3", ".", ".", "3", "4", "+", "+", ".", ".", "1", "1", ".", "1", ".", "."], "I", "0.3"),
    ([".", ".", ".", ".", ".", "1", "3", ".", "5", "4", "3", "4", "4", ".", "5", "4", "4"], "V", "3.4"),
    ([".", ".", ".", ".", ".", ".", ".", "+", ".", ".", ".", ".", ".", ".", ".", ".", "3"], "II", "0.6"),
    ([".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "I", "0.2"),
    (["8", "7", "8", "3", "3", "3", "1", "6", "6", "4", "7", "5", "5", "4", "3", "4", "4"], "V", "5.2"),
    ([".", ".", ".", "3", ".", ".", ".", ".", ".", ".", ".", ".", ".", "+", ".", ".", "."], "I", "0.5"),
    ([".", ".", ".", "5", ".", ".", ".", ".", ".", ".", "1", "2", ".", ".", ".", ".", "."], "II", "0.6"),
    ([".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "2", ".", ".", ".", ".", "."], "I", "0.2"),
    ([".", ".", ".", ".", "3", ".", ".", "3", ".", ".", ".", ".", ".", ".", ".", ".", "."], "II", "0.6"),
    ([".", "+", ".", "3", "1", "4", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "I", "0.2"),
    ([".", ".", "1", "1", ".", ".", ".", ".", ".", ".", ".", ".", "3", "1", ".", ".", "1"], "I", "0.4"),
    ([".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "II", "0.7"),
    ([".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
]

# Subassociation 2 (cols 18-26): cells then (C, D). Reading uncertain here; flagged.
_T48B = [
    (["3", "5", "6", "7", "2", "6", "3", "5", "5"], "I", "0.4"),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "V", "4.6"),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    (["9", "8", "8", "7", "9", "8", "7", "8", "8"], "", ""),
    (["5", ".", ".", ".", "1", ".", ".", ".", "1"], "", ""),
    ([".", ".", ".", "4", ".", ".", ".", ".", "."], "V", "3.0"),
    ([".", "5", ".", "3", ".", "1", ".", ".", "4"], "II", "0.8"),
    (["3", "+", "5", "3", "3", "2", "2", ".", "3"], "II", "0.9"),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "II", "0.6"),
    ([".", ".", ".", "2", ".", ".", ".", ".", "."], "II", "0.4"),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    (["4", "4", "5", "4", "4", "2", "5", "6", "5"], "V", "4.1"),
    ([".", ".", ".", ".", "1", "1", ".", "4", "3"], "III", "0.3"),
    ([".", "2", ".", "2", ".", "3", ".", ".", "1"], "II", "0.6"),
    ([".", "4", ".", ".", ".", ".", ".", ".", "."], "II", "0.3"),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", "3", "3", "3"], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", ".", ".", ".", ".", ".", "."], "", ""),
    ([".", ".", ".", "+", ".", ".", ".", ".", "."], "", ""),
]

_T48_REF_A = ["B68-129", "B68-119", "B68-131", "B68-127", "B68-132", "B68-278", "B68-290",
              "B68-135", "B68-143", "B68-177", "B68-178", "B68-355", "B68-116", "B68-117",
              "B68-126", "B68-130", "B68-144"]
_T48_MAP_A = ["597269", "305437", "597269", "596268", "540273", "703158", "565222", "485418",
              "416519", "273433", "273433", "698116", "308427", "308427", "596268", "597269", "416519"]
_T48_SREP_A = [6, 8, 10, 10, 11, 8, 11, 11, 9, 11, 9, 13, 11, 13, 8, 7, 11]

_T48_REF_B = ["B68-094", "B68-148", "B68-175", "B68-145", "B68-176", "B68-199", "B68-203",
              "B68-204", "B68-212"]
_T48_MAP_B = ["527627", "154507", "297420", "131475", "297420", "222613", "323385", "323385", "583189"]
_T48_SREP_B = [5, 8, 7, 9, 8, 7, 10, 11, 13]

TABLE_4_8A = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_8.png",
    "table_id_raw": "Table 4.8",
    "class": "ASTERETEA TRIPOLIUM",
    "order": "GLAUCETO-PUCCINELLIETALIA",
    "alliance": "Armerion maritimae",
    "association": "Armerion maritimae (Juncus gerardii-Carex extensa subass.)",
    "n_releves": "17",
    "total_species": "43",
    "low_confidence": True,
    "releves": [
        releve(i + 1, _T48_REF_A[i], _T48_MAP_A[i], "", "", "", "", 4, _T48_SREP_A[i])
        for i in range(17)
    ],
    "species": [
        {"name": _T48_SPECIES[i], "cells": _T48A[i][0], "C": _T48A[i][1], "D": _T48A[i][2]}
        for i in range(26)
    ],
}

TABLE_4_8B = {
    "image": "images/Birks-HJB-1973-Present-Flora-Veg-Skye_8.png",
    "table_id_raw": "Table 4.8",
    "class": "ASTERETEA TRIPOLIUM",
    "order": "GLAUCETO-PUCCINELLIETALIA",
    "alliance": "Armerion maritimae",
    "association": "Armerion maritimae (Armeria maritima-Grimmia maritima subass.)",
    "n_releves": "9",
    "total_species": "43",
    "low_confidence": True,
    "releves": [
        releve(i + 18, _T48_REF_B[i], _T48_MAP_B[i], "", "", "", "", 4, _T48_SREP_B[i])
        for i in range(9)
    ],
    "species": [
        {"name": _T48_SPECIES[i], "cells": _T48B[i][0], "C": _T48B[i][1], "D": _T48B[i][2]}
        for i in range(26)
    ],
}


TABLES = [
    TABLE_4_2,
    TABLE_4_3,
    TABLE_4_4,
    TABLE_4_5,
    TABLE_4_6A,
    TABLE_4_6B,
    TABLE_4_7A,
    TABLE_4_7B,
    TABLE_4_8A,
    TABLE_4_8B,
    TABLE_4_9,
    TABLE_4_10,
    TABLE_4_11,
]
