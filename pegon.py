class Pegon:
    SUKUN = "\u0652"
    FATHA = "\u064E"
    DAMMA = "\u064F"
    KASRA = "\u0650"
    PEPET = "\u0653"
    WAW = "\u0648"
    YEH = "\u064a"
    ALEF = "\u0627"
    ALEF_HAMZA_ABOVE = "\u0623"
    ALEF_HAMZA_BELOW = "\u0625"

    DIGRAPH_LIST = {
        (FATHA, WAW),
        (FATHA, YEH),
        (ALEF_HAMZA_ABOVE, FATHA),
        (ALEF_HAMZA_ABOVE, DAMMA),
        (ALEF_HAMZA_BELOW, KASRA),
        (ALEF_HAMZA_ABOVE, PEPET),
        (ALEF, FATHA),
        (ALEF, DAMMA),
        (ALEF, KASRA),
        (ALEF, PEPET),
    }
