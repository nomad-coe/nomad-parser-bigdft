"""
This is a module for unit testing the BigDFT parser. The unit tests are run with
a custom backend that outputs the results directly into native python object for
easier and faster analysis.

Each property that has an enumerable list of different possible options is
assigned a new test class, that should ideally test through all the options.

The properties that can have non-enumerable values will be tested only for one
specific case inside a test class that is designed for a certain type of run
(MD, optimization, QM/MM, etc.)
"""
import os
import unittest
import logging
import numpy as np
from bigdftparser import BigDFTParser
from nomadcore.unit_conversion.unit_conversion import convert_unit


#===============================================================================
def get_results(folder, metainfo_to_keep=None):
    """Get the given result from the calculation in the given folder by using
    the Analyzer in the nomadtoolkit package. Tries to optimize the parsing by
    giving the metainfo_to_keep argument.

    Args:
        folder: The folder relative to the directory of this script where the
            parsed calculation resides.
        metaname: The quantity to extract.
    """
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, folder, "output.out")
    parser = BigDFTParser(filename, None, debug=True, log_level=logging.WARNING)
    results = parser.parse()
    return results


#===============================================================================
def get_result(folder, metaname, optimize=True):
    if optimize:
        results = get_results(folder, None)
    else:
        results = get_results(folder)
    result = results[metaname]
    return result


#===============================================================================
class TestSinglePoint(unittest.TestCase):
    """Tests that the parser can handle single point calculations.
    """
    @classmethod
    def setUpClass(cls):
        cls.results = get_results("single_point", "section_run")
        # cls.results.print_summary()

    def test_program_name(self):
        result = self.results["program_name"]
        self.assertEqual(result, "BigDFT")

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

    # def test_configuration_periodic_dimensions(self):
        # result = self.results["configuration_periodic_dimensions"]
        # self.assertTrue(np.array_equal(result, np.array([False, False, False])))

    def test_program_version(self):
        result = self.results["program_version"]
        self.assertEqual(result, "1.8")

    # def test_xc_functional(self):
        # result = self.results["XC_functional"]
        # self.assertEqual(result, "1.0*MGGA_C_TPSS+1.0*MGGA_X_TPSS")

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

    def test_number_of_atoms(self):
        n_atoms = self.results["number_of_atoms"]
        self.assertEqual(n_atoms, 2)

    def test_electronic_structure_method(self):
        result = self.results["electronic_structure_method"]
        self.assertEqual(result, "DFT")

    # def test_total_charge(self):
        # charge = self.results["total_charge"]
        # self.assertEqual(charge, 0)

    # def test_energy_total(self):
        # result = self.results["energy_total"]
        # expected_result = convert_unit(np.array(-76.436222730188), "hartree")
        # self.assertTrue(np.array_equal(result, expected_result))

    # def test_energy_x(self):
        # result = self.results["energy_X"]
        # expected_result = convert_unit(np.array(-9.025345841743), "hartree")
        # self.assertTrue(np.array_equal(result, expected_result))

    # def test_energy_c(self):
        # result = self.results["energy_C"]
        # expected_result = convert_unit(np.array(-0.328011552453), "hartree")
        # self.assertTrue(np.array_equal(result, expected_result))

    # def test_energy_total_scf_iteration(self):
        # result = self.results["energy_total_scf_iteration"]
        # # Test the first and last energies
        # expected_result = convert_unit(np.array(
            # [
                # [-76.3916403957],
                # [-76.4362227302],
            # ]), "hartree")
        # self.assertTrue(np.array_equal(np.array([[result[0]], [result[-1]]]), expected_result))

    # def test_energy_change_scf_iteration(self):
        # result = self.results["energy_change_scf_iteration"]
        # expected_result = convert_unit(np.array(
            # [
                # [-8.55E+01],
                # [-3.82E-07],
            # ]), "hartree")
        # self.assertTrue(np.array_equal(np.array([[result[0]], [result[-1]]]), expected_result))

    # def test_scf_max_iteration(self):
        # result = self.results["scf_max_iteration"]
        # self.assertEqual(result, 50)

    # def test_scf_threshold_energy_change(self):
        # result = self.results["scf_threshold_energy_change"]
        # self.assertEqual(result, convert_unit(1.00E-06, "hartree"))


    # def test_scf_dft_number_of_iterations(self):
        # result = self.results["number_of_scf_iterations"]
        # self.assertEqual(result, 6)

    # def test_spin_target_multiplicity(self):
        # multiplicity = self.results["spin_target_multiplicity"]
        # self.assertEqual(multiplicity, 1)

    # def test_single_configuration_to_calculation_method_ref(self):
        # result = self.results["single_configuration_to_calculation_method_ref"]
        # self.assertEqual(result, 0)

    # def test_single_configuration_calculation_to_system_description_ref(self):
        # result = self.results["single_configuration_calculation_to_system_ref"]
        # self.assertEqual(result, 0)

    # def test_single_configuration_calculation_converged(self):
        # result = self.results["single_configuration_calculation_converged"]
        # self.assertTrue(result)

    # def test_section_method_atom_kind(self):
        # kind = self.results["section_method_atom_kind"][0]
        # self.assertEqual(kind["method_atom_kind_atom_number"][0], 1)
        # self.assertEqual(kind["method_atom_kind_label"][0], "H")

    # def test_section_method_basis_set(self):
        # kind = self.results["section_method_basis_set"][0]
        # self.assertEqual(kind["method_basis_set_kind"][0], "wavefunction")
        # self.assertTrue(np.array_equal(kind["mapping_section_method_basis_set_cell_associated"][0], 0))

    # def test_number_of_spin_channels(self):
        # result = self.results["number_of_spin_channels"]
        # self.assertEqual(result, 1)

    # def test_simulation_cell(self):
        # cell = self.results["simulation_cell"]
        # n_vectors = cell.shape[0]
        # n_dim = cell.shape[1]
        # self.assertEqual(n_vectors, 3)
        # self.assertEqual(n_dim, 3)
        # expected_cell = convert_unit(np.array([[15.1178, 0, 0], [0, 15.1178, 0], [0, 0, 15.1178]]), "bohr")
        # self.assertTrue(np.array_equal(cell, expected_cell))

    # def test_basis_set_cell_dependent(self):
        # kind = self.results["basis_set_cell_dependent_kind"]
        # name = self.results["basis_set_cell_dependent_name"]
        # cutoff = self.results["basis_set_planewave_cutoff"]

        # self.assertEqual(kind, "plane_waves")
        # self.assertEqual(name, "PW_70.0")
        # self.assertEqual(cutoff, convert_unit(70.00000, "rydberg"))


#===============================================================================
if __name__ == '__main__':
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(TestSinglePoint))

    alltests = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=0).run(alltests)
