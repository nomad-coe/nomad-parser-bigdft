import os
import unittest
import logging
import numpy as np
from bigdftparser import BigDFTParser
from nomadcore.unit_conversion.unit_conversion import convert_unit


def get_result(folder, metaname=None):
    """Get the results from the calculation in the given folder. By default goes through different

    Args:
        folder: The folder relative to the directory of this script where the
            parsed calculation resides.
        metaname(str): Optional quantity to return. If not specified, returns
            the full dictionary of results.
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join("bigdft_{}".format(VERSION), dirname, folder, "output.out")
    parser = BigDFTParser(None, debug=True, log_level=logging.CRITICAL)
    results = parser.parse(filename)

    if metaname is None:
        return results
    else:
        return results[metaname]


class TestSinglePoint(unittest.TestCase):
    """Tests that the parser can handle single point calculations.
    """
    @classmethod
    def setUpClass(cls):
        cls.results = get_result("single_point")
        # cls.results.print_summary()

    def test_program_name(self):
        result = self.results["program_name"]
        self.assertEqual(result, "BigDFT")

    def test_program_version(self):
        result = self.results["program_version"]
        self.assertEqual(result, "1.8")

    def test_program_basis_set_type(self):
        result = self.results["program_basis_set_type"]
        self.assertEqual(result, "real-space grid")

    def test_simulation_cell(self):
        result = self.results["simulation_cell"]
        expected_result = convert_unit(np.array(
            [
                [7.1439,  0, 0],
                [0, 7.1439, 0],
                [0, 0, 8.3345],
            ]
        ), "angstrom")
        self.assertTrue(np.array_equal(result, expected_result))

    def test_configuration_periodic_dimensions(self):
        result = self.results["configuration_periodic_dimensions"]
        self.assertTrue(np.array_equal(result, np.array([False, False, False])))

    def test_xc_functional(self):
        result = self.results["XC_functional"]
        self.assertEqual(result, "1.0*LDA_XC_TETER93")

    def test_atom_labels(self):
        atom_labels = self.results["atom_labels"]
        expected_labels = np.array(["N", "N"])
        self.assertTrue(np.array_equal(atom_labels, expected_labels))

    def test_atom_positions(self):
        atom_position = self.results["atom_positions"]
        expected_position = convert_unit(np.array(
            [
                [3.571946174,  3.571946174,  3.609775538],
                [3.571946174,  3.571946174,  4.724765534],
            ]
        ), "angstrom")
        self.assertTrue(np.array_equal(atom_position, expected_position))

    def test_atom_forces(self):
        result = self.results["atom_forces"]
        expected_result = convert_unit(np.array(
            [
                [-1.694065894509E-21,  -3.388131789017E-21, 5.670554140677E-02],
                [1.694065894509E-21,  3.388131789017E-21, -5.670554140677E-02],
            ]
        ), "hartree/bohr")
        self.assertTrue(np.array_equal(result, expected_result))

    def test_number_of_atoms(self):
        n_atoms = self.results["number_of_atoms"]
        self.assertEqual(n_atoms, 2)

    def test_electronic_structure_method(self):
        result = self.results["electronic_structure_method"]
        self.assertEqual(result, "DFT")

    def test_total_charge(self):
        charge = self.results["total_charge"]
        self.assertEqual(charge, 0)

    def test_number_of_spin_channels(self):
        result = self.results["number_of_spin_channels"]
        self.assertEqual(result, 1)

    def test_energy_total(self):
        result = self.results["energy_total"]
        expected_result = convert_unit(np.array(-1.98834837256869790E+01), "hartree")
        self.assertTrue(np.array_equal(result, expected_result))

    def test_energy_total_scf_iteration(self):
        result = self.results["energy_total_scf_iteration"]
        # Test the first and last energies
        expected_result = convert_unit(np.array(
            [
                [-1.96096887307935432E+01],
                [-1.98834837256869790E+01],
            ]), "hartree")
        self.assertTrue(np.array_equal(np.array([[result[0]], [result[-1]]]), expected_result))

    def test_energy_change_scf_iteration(self):
        result = self.results["energy_change_scf_iteration"]
        expected_result = convert_unit(np.array(
            [
                [-1.58E-03],
                [-1.78E-09],
            ]), "hartree")
        self.assertTrue(np.array_equal(np.array([[result[0]], [result[-1]]]), expected_result))

    def test_scf_max_iteration(self):
        result = self.results["scf_max_iteration"]
        self.assertEqual(result, 50)

    def test_scf_dft_number_of_iterations(self):
        result = self.results["number_of_scf_iterations"]
        self.assertEqual(result, 11)

    def test_single_configuration_to_calculation_method_ref(self):
        result = self.results["single_configuration_to_calculation_method_ref"]
        self.assertEqual(result, 0)

    def test_single_configuration_calculation_to_system_description_ref(self):
        result = self.results["single_configuration_calculation_to_system_ref"]
        self.assertEqual(result, 0)

    # def test_single_configuration_calculation_converged(self):
        # result = self.results["single_configuration_calculation_converged"]
        # self.assertTrue(result)

    # def test_section_method_atom_kind(self):
        # kind = self.results["section_method_atom_kind"][0]
        # self.assertEqual(kind["method_atom_kind_atom_number"][0], 1)
        # self.assertEqual(kind["method_atom_kind_label"][0], "H")


class TestPeriodicity(unittest.TestCase):
    """Tests that the parser can handle different boundary conditions.
    """
    def test_periodic(self):
        results = get_result("periodicity/periodic")
        result = results["configuration_periodic_dimensions"]
        self.assertTrue(np.array_equal(result, np.array([True, True, True])))

    def test_surface(self):
        results = get_result("periodicity/surface")
        result = results["configuration_periodic_dimensions"]
        self.assertTrue(np.array_equal(result, np.array([True, False, True])))

    def test_free(self):
        results = get_result("periodicity/free")
        result = results["configuration_periodic_dimensions"]
        self.assertTrue(np.array_equal(result, np.array([False, False, False])))


class TestXCFunctionals(unittest.TestCase):
    """Tests that the parser can handle different XC functional codes.
    """
    def test_abinit_1(self):
        results = get_result("xc_functionals/abinit_1")
        result = results["XC_functional"]
        self.assertEqual(result, "1.0*LDA_XC_TETER93")

    def test_abinit_11(self):
        results = get_result("xc_functionals/abinit_11")
        result = results["XC_functional"]
        self.assertEqual(result, "1.0*GGA_C_PBE_1.0*GGA_X_PBE")

    def test_abinit_12(self):
        results = get_result("xc_functionals/abinit_12")
        result = results["XC_functional"]
        self.assertEqual(result, "1.0*GGA_X_PBE")

    # YAML parse error
    # def test_abinit_15(self):
        # results = get_results("xc_functionals/abinit_15")
        # result = results["XC_functional"]
        # self.assertEqual(result, "1.0*GGA_C_PBE_1.0*GGA_X_RPBE")

    # Error
    # def test_abinit_16(self):
        # results = get_results("xc_functionals/abinit_16")
        # result = results["XC_functional"]
        # self.assertEqual(result, "1.0*GGA_XC_HCTH_93")

    # Error
    # def test_abinit_17(self):
        # results = get_results("xc_functionals/abinit_17")
        # result = results["XC_functional"]
        # self.assertEqual(result, "1.0*GGA_XC_HCTH_120")

    # Error
    # def test_abinit_26(self):
        # results = get_results("xc_functionals/abinit_26")
        # result = results["XC_functional"]
        # self.assertEqual(result, "1.0*GGA_XC_HCTH_147")

    # Error
    # def test_abinit_27(self):
        # results = get_results("xc_functionals/abinit_27")
        # result = results["XC_functional"]
        # self.assertEqual(result, "1.0*GGA_XC_HCTH_407")

    def test_abinit_100(self):
        results = get_result("xc_functionals/abinit_100")
        result = results["XC_functional"]
        self.assertEqual(result, "1.0*HF_X")

    def test_libxc_001(self):
        results = get_result("xc_functionals/libxc_001")
        result = results["XC_functional"]
        self.assertEqual(result, "1.0*LDA_X")

    def test_libxc_010(self):
        results = get_result("xc_functionals/libxc_010")
        result = results["XC_functional"]
        self.assertEqual(result, "1.0*LDA_C_PZ_MOD")

    def test_libxc_101(self):
        results = get_result("xc_functionals/libxc_101")
        result = results["XC_functional"]
        self.assertEqual(result, "1.0*GGA_X_PBE")

    def test_libxc_101130(self):
        results = get_result("xc_functionals/libxc_101130")
        result = results["XC_functional"]
        self.assertEqual(result, "1.0*GGA_C_PBE_1.0*GGA_X_PBE")


if __name__ == '__main__':

    VERSIONS = ["1.8"]

    for VERSION in VERSIONS:
        suites = []
        suites.append(unittest.TestLoader().loadTestsFromTestCase(TestSinglePoint))
        suites.append(unittest.TestLoader().loadTestsFromTestCase(TestPeriodicity))
        suites.append(unittest.TestLoader().loadTestsFromTestCase(TestXCFunctionals))

        alltests = unittest.TestSuite(suites)
        unittest.TextTestRunner(verbosity=0).run(alltests)
