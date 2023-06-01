import enum


class Sectors(enum.Enum):
    AUTOMOTIVE = enum.auto()
    TECHNOLOGY = enum.auto()
    BANKING = enum.auto()
    HEALTHCARE = enum.auto()
    ENERGY = enum.auto()
    FOOD = enum.auto()
    TELECOMUNICATION = enum.auto()
    SOFTWARE = enum.auto()
    MEDIA = enum.auto()
    RETAIL = enum.auto()


chosen_stocks: dict[Sectors, list[str]] = {
    Sectors.AUTOMOTIVE: [
        "VWAGY",  # VOLKSWAGEN
        "BMW.DE",  # Bayerische Motoren Werke AG
        "TM",  # Toyota Motor Corporation
        "GM",  # General Motors Company
        "F",  # Ford Motor Company
    ],
    Sectors.TECHNOLOGY: [
        "SMSN.IL",  # samsung
        "AAPL",  # apple
        "AMD",  # amd
        "INTC",  # intel
        "NVDA",  # nvidia
    ],
    Sectors.BANKING: [
        "JPM",  # JPMorgan Chase & Co
        "BAC",  # Bank of America Corporation
        "C",  # Citigroup Inc.
        "SAN",  # Banco Santander
        "HSBC",  # HSBC Holdings
    ],
    Sectors.HEALTHCARE: [
        "JNJ",  # Johnson & Johnson
        "PFE",  # Pfizer Inc.
        "CVS",  # CVS Health Corporation
        "UNH",  # UnitedHealth Group Incorporated
        "BAYN.DE",  # Bayer
    ],
    Sectors.ENERGY: [
        "XOM",  # Exxon Mobil Corporation
        "CVX",  # Chevron Corporation
        "GBX",  # Shell
        "BP",  # BP p.l.c.
        "TTE",  # TotalEnergies SE
    ],
    Sectors.FOOD: [
        "KO",  # The Coca-Cola Company
        "MCD",  # McDonald's Corporation
        "NSRGF",  # Nestle S.A.
        "PEP",  # PepsiCo, Inc.
        "MDLZ",  # Mondelez International
    ],
    Sectors.TELECOMUNICATION: [
        "T",  # AT&T Inc.
        "VZ",  # Verizon Communications Inc.
        "TMUS",  # T-Mobile US, Inc.
        "VOD",  # Vodafone Group Plc
        "NOK",  # Nokia
    ],
    Sectors.SOFTWARE: [
        "MSFT",  # Microsoft
        "SAP",  # SAP
        "CRM",  # Salesforce
        "ORCL",  # Oracle
        "IBM",  # IBM
    ],
    Sectors.MEDIA: [
        "DIS",  # The Walt Disney Company
        "NFLX",  # Netflix, Inc.
        "NWSA",  # News corporation
        "META",  # Facebook
        "GOOGL",  # Alphabet Inc.
    ],
    Sectors.RETAIL: [
        "AMZN",  # Amazon.com, Inc.
        "WMT",  # Walmart Inc.
        "TGT",  # Target Corporation
        "HD",  # The Home Depot, Inc.
        "COST",  # Costco Wholesale Corporation
    ],
}
