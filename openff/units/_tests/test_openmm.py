import pytest
from openff.utilities.testing import skip_if_missing
from openff.utilities.utilities import has_package

from openff.units import Quantity, unit
from openff.units.exceptions import NoneQuantityError, NoneUnitError
from openff.units.openmm import ensure_quantity, from_openmm

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
        0.5 * openmm_unit.dalton,
    ]

    pint_quantities = [
        4.0 * unit.nanometer,
        5.0 * unit.angstrom,
        1.0 * unit.elementary_charge,
        0.5 * unit.erg,
        1.0 * unit.dimensionless,
        0.5 * unit.gram / unit.mol,
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
        kilogram = 1
        ampere = 1

    openmm_quantitites = []
    pint_quantities = []


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

    def test_from_openmm_quantity_none(self):
        with pytest.raises(NoneQuantityError, match=r"Input is None.*OpenMM.*Quantity"):
            from_openmm(None)

    def test_to_openmm_quantity_none(self):
        with pytest.raises(NoneQuantityError, match=r"Input is None.*OpenFF.*Quantity"):
            to_openmm(None)

    def test_openmm_unit_to_string_none(self):
        with pytest.raises(NoneUnitError, match=r"Input is None.*OpenMM.*Unit"):
            openmm_unit_to_string(None)

    @pytest.mark.parametrize(
        "openmm_quantity,pint_quantity",
        [(s, p) for s, p in zip(openmm_quantitites, pint_quantities)],
    )
    def test_pint_to_openmm(self, openmm_quantity, pint_quantity):
        """Test conversion from pint Quantity to OpenMM Quantity."""
        converted_openmm_quantity = to_openmm(pint_quantity)

        assert openmm_quantity == converted_openmm_quantity

    @skip_if_missing("openmm.unit")
    @pytest.mark.parametrize(
        "openmm_unit_,unit_str",
        [
            (openmm_unit.kilojoule_per_mole, "mole**-1 * kilojoule"),
            (
                openmm_unit.kilocalories_per_mole / openmm_unit.angstrom**2,
                "angstrom**-2 * mole**-1 * kilocalorie",
            ),
            (
                openmm_unit.joule / (openmm_unit.mole * openmm_unit.nanometer**2),
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

    @pytest.mark.parametrize(
        "from_openff_quantity,to_openmm_quantity",
        [
            (
                1.0 * unit.k_B,
                1.380649e-23
                * openmm_unit.meter**2
                * openmm_unit.kilogram
                * openmm_unit.second**-2
                * openmm_unit.kelvin**-1,
            ),
            (
                1.0 / unit.pi,
                0.31830988618 * openmm_unit.dimensionless,
            ),
            (
                1.0 * unit.avogadro_constant,
                6.02214076e23 / openmm_unit.mole,
            ),
            (
                1.0 * unit.vacuum_permittivity,
                8.85418782e-12
                * openmm_unit.meter**-3
                * openmm_unit.kilogram**-1
                * openmm_unit.second**4
                * openmm_unit.ampere**2,
            ),
        ],
    )
    def test_openmm_unit_constants(self, from_openff_quantity, to_openmm_quantity):
        """Test conversion of units that do not exist in the OpenMM registry

        For these units, the magnitude/value may change due to limited floating
        point precision. We therefore do not require the final values to be
        exact - we accept a variance of one part in one million."""
        converted = to_openmm(from_openff_quantity)

        assert abs(converted - to_openmm_quantity) < (
            # Multiply by dimensionless to ensure result is an openmm quantity
            1.0e-6 * to_openmm_quantity * openmm_unit.dimensionless
        )


@skip_if_missing("openmm.unit")
class TestEnsureType:
    from openff.units import unit

    @pytest.mark.parametrize(
        "registry",
        ["openmm", "openff"],
    )
    def test_ensure_units(self, registry):
        x = unit.Quantity(4.0, unit.angstrom)
        y = openmm_unit.Quantity(4.0, openmm_unit.angstrom)

        assert ensure_quantity(x, registry) == ensure_quantity(y, registry)

    def test_unsupported_type(self):
        x = unit.Quantity(4.0, unit.angstrom)

        with pytest.raises(ValueError, match=r"Unsupported.*type_to_ensure.*pint"):
            ensure_quantity(x, "pint")

    def test_short_circuit(self):
        x = unit.Quantity(4.0, unit.angstrom)
        y = openmm_unit.Quantity(4.0, openmm_unit.angstrom)

        assert id(ensure_quantity(x, "openff")) == id(x)
        assert id(ensure_quantity(y, "openmm")) == id(y)

    @pytest.mark.parametrize(
        "value",
        [
            1,
            2.0,
        ],
    )
    def test_primitives(self, value):
        assert ensure_quantity(value, "openff") == unit.Quantity(value, unit.dimensionless)
        assert ensure_quantity(value, "openmm") == openmm_unit.Quantity(
            value, openmm_unit.dimensionless
        )

    @pytest.mark.parametrize("use_numpy", [True, False])
    def test_array(self, use_numpy):
        import numpy

        value = [4, 5]

        if use_numpy:
            value = numpy.asarray(value)

        numpy.testing.assert_allclose(
            ensure_quantity(value, "openff").m,
            Quantity(value, unit.dimensionless).m,
        )

        numpy.testing.assert_equal(
            numpy.array(ensure_quantity(value, "openmm")),
            numpy.array(openmm_unit.Quantity(value, openmm_unit.dimensionless)),
        )
