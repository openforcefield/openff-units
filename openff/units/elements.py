"""
Symbols and masses for the chemical elements.

This module provides mappings from atomic number to atomic mass and symbol.
These dicts were seeded from running the below script using OpenMM 7.7.

It's not completely clear where OpenMM sourced these values from [1] but they are generally
consistent with recent IUPAC values [2].

1. https://github.com/openmm/openmm/issues/3434#issuecomment-1023406296
2. https://www.ciaaw.org/publications.htm

.. code-block:: python

    import openmm.app

    masses = {
        atomic_number: openmm.app.element.Element.getByAtomicNumber(
            atomic_number
        ).mass._value
        for atomic_number in range(1, 117)
    }

    symbols = {
        atomic_number: openmm.app.element.Element.getByAtomicNumber(atomic_number).symbol
        for atomic_number in range(1, 117)
    }

"""

from typing import Dict

from openff.units import Quantity, unit

__all__ = [
    "MASSES",
    "SYMBOLS",
    "NUMBERS",
]

"""Mapping from atomic number to atomic mass"""
MASSES: Dict[int, Quantity] = {
    # https://github.com/hgrecco/pint/issues/1804
    index + 1: Quantity(mass, unit.dalton)  # type: ignore[call-overload]
    for index, mass in enumerate(
        [
            1.007947,
            4.003,
            6.9412,
            9.0121823,
            10.8117,
            12.01078,
            14.00672,
            15.99943,
            18.99840325,
            20.17976,
            22.989769282,
            24.30506,
            26.98153868,
            28.08553,
            30.9737622,
            32.0655,
            35.4532,
            39.9481,
            39.09831,
            40.0784,
            44.9559126,
            47.8671,
            50.94151,
            51.99616,
            54.9380455,
            55.8452,
            58.9331955,
            58.69342,
            63.5463,
            65.4094,
            69.7231,
            72.641,
            74.921602,
            78.963,
            79.9041,
            83.7982,
            85.46783,
            87.621,
            88.905852,
            91.2242,
            92.906382,
            95.942,
            98,
            101.072,
            102.905502,
            106.421,
            107.86822,
            112.4118,
            114.8183,
            118.7107,
            121.7601,
            127.603,
            126.904473,
            131.2936,
            132.90545192,
            137.3277,
            138.905477,
            140.1161,
            140.907652,
            144.2423,
            145,
            150.362,
            151.9641,
            157.253,
            158.925352,
            162.5001,
            164.930322,
            167.2593,
            168.934212,
            173.043,
            174.9671,
            178.492,
            180.947882,
            183.841,
            186.2071,
            190.233,
            192.2173,
            195.0849,
            196.9665694,
            200.592,
            204.38332,
            207.21,
            208.980401,
            209,
            210,
            222.018,
            223,
            226,
            227,
            232.038062,
            231.035882,
            238.028913,
            237,
            244,
            243,
            247,
            247,
            251,
            252,
            257,
            258,
            259,
            262,
            261,
            262,
            266,
            264,
            269,
            268,
            281,
            272,
            285,
            284,
            289,
            288,
            292,
        ]
    )
}

"""Mapping from atomic number to element symbol"""
SYMBOLS: Dict[int, str] = {
    index + 1: symbol
    for index, symbol in enumerate(
        [
            "H",
            "He",
            "Li",
            "Be",
            "B",
            "C",
            "N",
            "O",
            "F",
            "Ne",
            "Na",
            "Mg",
            "Al",
            "Si",
            "P",
            "S",
            "Cl",
            "Ar",
            "K",
            "Ca",
            "Sc",
            "Ti",
            "V",
            "Cr",
            "Mn",
            "Fe",
            "Co",
            "Ni",
            "Cu",
            "Zn",
            "Ga",
            "Ge",
            "As",
            "Se",
            "Br",
            "Kr",
            "Rb",
            "Sr",
            "Y",
            "Zr",
            "Nb",
            "Mo",
            "Tc",
            "Ru",
            "Rh",
            "Pd",
            "Ag",
            "Cd",
            "In",
            "Sn",
            "Sb",
            "Te",
            "I",
            "Xe",
            "Cs",
            "Ba",
            "La",
            "Ce",
            "Pr",
            "Nd",
            "Pm",
            "Sm",
            "Eu",
            "Gd",
            "Tb",
            "Dy",
            "Ho",
            "Er",
            "Tm",
            "Yb",
            "Lu",
            "Hf",
            "Ta",
            "W",
            "Re",
            "Os",
            "Ir",
            "Pt",
            "Au",
            "Hg",
            "Tl",
            "Pb",
            "Bi",
            "Po",
            "At",
            "Rn",
            "Fr",
            "Ra",
            "Ac",
            "Th",
            "Pa",
            "U",
            "Np",
            "Pu",
            "Am",
            "Cm",
            "Bk",
            "Cf",
            "Es",
            "Fm",
            "Md",
            "No",
            "Lr",
            "Rf",
            "Db",
            "Sg",
            "Bh",
            "Hs",
            "Mt",
            "Ds",
            "Rg",
            "Uub",
            "Uut",
            "Uuq",
            "Uup",
            "Uuh",
        ]
    )
}

"""Mapping from element symbol to atomic number"""
NUMBERS: dict[str, int] = {val: key for key, val in SYMBOLS.items()}
