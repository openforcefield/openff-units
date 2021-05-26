import pytest
from openff.utilities.testing import skip_if_missing
from openff.utilities.utilities import has_package

from openff.units import unit
from openff.units.simtk import from_simtk

if has_package("simtk.unit"):
    from simtk import unit as simtk_unit

    from openff.units.simtk import simtk_unit_to_string, string_to_simtk_unit, to_simtk

    simtk_quantitites = [
        4.0 * simtk_unit.nanometer,
        5.0 * simtk_unit.angstrom,
        1.0 * simtk_unit.elementary_charge,
        0.5 * simtk_unit.erg,
        1.0 * simtk_unit.dimensionless,
    ]

    pint_quantities = [
        4.0 * unit.nanometer,
        5.0 * unit.angstrom,
        1.0 * unit.elementary_charge,
        0.5 * unit.erg,
        1.0 * unit.dimensionless,
    ]
else:
    simtk_quantitites = []
    pint_quantities = []


@skip_if_missing("simtk.unit")
class TestSimTKUnits:
    @pytest.mark.parametrize(
        "simtk_quantity,pint_quantity",
        [(s, p) for s, p in zip(simtk_quantitites, pint_quantities)],
    )
    def test_simtk_to_pint(self, simtk_quantity, pint_quantity):
        """Test conversion from SimTK Quantity to pint Quantity."""
        converted_pint_quantity = from_simtk(simtk_quantity)

        assert pint_quantity == converted_pint_quantity

    @skip_if_missing("simtk.unit")
    @pytest.mark.parametrize(
        "simtk_unit_,unit_str",
        [
            (simtk_unit.kilojoule_per_mole, "mole**-1 * kilojoule"),
            (
                simtk_unit.kilocalories_per_mole / simtk_unit.angstrom ** 2,
                "angstrom**-2 * mole**-1 * kilocalorie",
            ),
            (
                simtk_unit.joule / (simtk_unit.mole * simtk_unit.nanometer ** 2),
                "nanometer**-2 * mole**-1 * joule",
            ),
            (
                simtk_unit.picosecond ** (-1),
                "picosecond**-1",
            ),
            (simtk_unit.dimensionless, "dimensionless"),
            (simtk_unit.second, "second"),
            (simtk_unit.angstrom, "angstrom"),
        ],
    )
    def test_simtk_unit_string_roundtrip(self, simtk_unit_, unit_str):
        assert simtk_unit_to_string(simtk_unit_) == unit_str

        assert unit_str == simtk_unit_to_string(string_to_simtk_unit(unit_str))

    @pytest.mark.parametrize(
        "openff_quantity,simtk_quantity",
        [
            (300.0 * unit.kelvin, 300.0 * simtk_unit.kelvin),
            (
                1.5 * unit.kilojoule,
                1.5 * simtk_unit.kilojoule,
            ),
            (1.0 / unit.meter, 1.0 / simtk_unit.meter),
        ],
    )
    def test_simtk_roundtrip(self, openff_quantity, simtk_quantity):
        assert simtk_quantity == to_simtk(openff_quantity)
        assert openff_quantity == from_simtk(simtk_quantity)

        assert openff_quantity == from_simtk(to_simtk(openff_quantity))
