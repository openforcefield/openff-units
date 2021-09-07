import pytest
from openff.utilities.testing import skip_if_missing
from openff.utilities.utilities import has_package

from openff.units import unit
from openff.units.openmm import from_openmm

if has_package("openmm.unit"):
    from openmm import unit as openmm_unit

    from openff.units.openmm import (
        openmm_unit_to_string,
        string_to_openmm_unit,
        to_openmm,
    )

    openmm_quantitites = [
        4.0 * openmm_unit.nanometer,
        5.0 * openmm_unit.angstrom,
        1.0 * openmm_unit.elementary_charge,
        0.5 * openmm_unit.erg,
        1.0 * openmm_unit.dimensionless,
    ]

    pint_quantities = [
        4.0 * unit.nanometer,
        5.0 * unit.angstrom,
        1.0 * unit.elementary_charge,
        0.5 * unit.erg,
        1.0 * unit.dimensionless,
    ]
else:
    # Must be defined as something, despite not being used, because pytest
    # inspect the contents of pytest.mark.parametrize during collection;
    # otherwise NameErrors will be raised. Finding a way to skip _collection_
    # would be more elegant than mocking a module
    class openmm_unit:  # type: ignore[no-redef]
        kilojoule = 1
        kilojoule_per_mole = 1
        kilocalories_per_mole = 1
        angstrom = 1
        nanometer = 1
        meter = 1
        picosecond = 1
        joule = 1
        mole = 1
        dimensionless = 1
        second = 1
        kelvin = 1

    openmm_quantitites = []
    pint_quantities = []


@pytest.mark.xfail
@skip_if_missing("openmm.unit")
class TestOpenMMUnits:
    @pytest.mark.parametrize(
        "openmm_quantity,pint_quantity",
        [(s, p) for s, p in zip(openmm_quantitites, pint_quantities)],
    )
    def test_openmm_to_pint(self, openmm_quantity, pint_quantity):
        """Test conversion from OpenMM Quantity to pint Quantity."""
        converted_pint_quantity = from_openmm(openmm_quantity)

        assert pint_quantity == converted_pint_quantity

    @skip_if_missing("openmm.unit")
    @pytest.mark.parametrize(
        "openmm_unit_,unit_str",
        [
            (openmm_unit.kilojoule_per_mole, "mole**-1 * kilojoule"),
            (
                openmm_unit.kilocalories_per_mole / openmm_unit.angstrom ** 2,
                "angstrom**-2 * mole**-1 * kilocalorie",
            ),
            (
                openmm_unit.joule / (openmm_unit.mole * openmm_unit.nanometer ** 2),
                "nanometer**-2 * mole**-1 * joule",
            ),
            (
                openmm_unit.picosecond ** (-1),
                "picosecond**-1",
            ),
            (openmm_unit.dimensionless, "dimensionless"),
            (openmm_unit.second, "second"),
            (openmm_unit.angstrom, "angstrom"),
        ],
    )
    def test_openmm_unit_string_roundtrip(self, openmm_unit_, unit_str):
        assert openmm_unit_to_string(openmm_unit_) == unit_str

        assert unit_str == openmm_unit_to_string(string_to_openmm_unit(unit_str))

    @pytest.mark.parametrize(
        "openff_quantity,openmm_quantity",
        [
            (300.0 * unit.kelvin, 300.0 * openmm_unit.kelvin),
            (
                1.5 * unit.kilojoule,
                1.5 * openmm_unit.kilojoule,
            ),
            (1.0 / unit.meter, 1.0 / openmm_unit.meter),
        ],
    )
    def test_openmm_roundtrip(self, openff_quantity, openmm_quantity):
        assert openmm_quantity == to_openmm(openff_quantity)
        assert openff_quantity == from_openmm(openmm_quantity)

        assert openff_quantity == from_openmm(to_openmm(openff_quantity))
