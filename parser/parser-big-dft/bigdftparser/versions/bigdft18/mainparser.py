import re
import logging
import numpy as np
from yaml import Loader
from yaml import ScalarNode, SequenceNode, MappingNode, MappingEndEvent
from nomadcore.baseclasses import AbstractBaseParser
LOGGER = logging.getLogger("nomad")


#===============================================================================
class BigDFTMainParser(AbstractBaseParser):
    """The main parser class that is called for all run types. Parses the NWChem
    output file.
    """
    def __init__(self, file_path, parser_context):
        """
        """
        super(BigDFTMainParser, self).__init__(file_path, parser_context)

        # Map keys in the output to funtions that handle the values
        self.key_to_funct_map = {
            "Version Number": lambda x: self.backend.addValue("program_version", x),
            "Atomic structure": self.atomic_structure,
            "Sizes of the simulation domain": self.simulation_domain,
            "Atomic System Properties": self.atomic_system_properties,
            "dft": self.dft,
            "DFT parameters": self.dft_parameters,
        }

    def parse(self):
        """The output file of a BigDFT run is a YAML document. Here we directly
        parse this document with an existing YAML library, and push its
        contents into the backend. This function will read the document in
        smaller pieces, thus preventing the parser from opening too large files
        directly into memory.
        """
        self.prepare()
        with open(self.file_path, "r") as fin:

            # Open default sections and output default information
            section_run_id = self.backend.openSection("section_run")
            section_system_id = self.backend.openSection("section_system")
            section_method_id = self.backend.openSection("section_method")
            self.backend.addValue("program_name", "BigDFT")
            self.backend.addValue("electronic_structure_method", "DFT")
            self.backend.addValue("program_basis_set_type", "real-space grid")

            loader = Loader(fin)
            generator = self.generate_root_nodes(loader)

            # Go through all the keys in the mapping, and call an appropriate
            # function on the value.
            for key, value in generator:

                function = self.key_to_funct_map.get(key)
                if function is not None:
                    function(value)

            # Close default sections
            self.backend.closeSection("section_method", section_method_id)
            self.backend.closeSection("section_system", section_system_id)
            self.backend.closeSection("section_run", section_run_id)

    def generate_root_nodes(self, loader):
        # Ignore the first two events
        loader.get_event()  # StreamStarEvetn
        loader.get_event()  # DocumentStartEvent
        start_event = loader.get_event()  # MappingStartEvent
        tag = start_event.tag

        # This is the root mapping that contains everything
        node = MappingNode(tag, [],
                start_event.start_mark, None,
                flow_style=start_event.flow_style)

        while not loader.check_event(MappingEndEvent):
            key = loader.construct_scalar(loader.compose_node(node, None))
            value = loader.compose_node(node, key)
            if isinstance(value, MappingNode):
                value = loader.construct_mapping(value, deep=True)
            elif isinstance(value, SequenceNode):
                value = loader.construct_sequence(value, deep=True)
            elif isinstance(value, ScalarNode):
                value = loader.construct_scalar(value)
            yield (key, value)

    #===========================================================================
    # The following functions handle the different sections in the output
    def scf(self, scf):
        """Parse the SCF loop information.
        """
        print("Moi")
        return

    def atomic_structure(self, value):
        np_positions = []
        np_labels = []
        positions = value["Positions"]
        for position in positions:
            np_positions.append(*position.values())
            np_labels.append(*position.keys())
        np_positions = np.array(np_positions)
        np_labels = np.array(np_labels)
        self.backend.addArrayValues("atom_positions", np_positions, unit="angstrom")
        self.backend.addArrayValues("atom_labels", np_labels)

    def simulation_domain(self, value):
        simulation_cell = np.diag(value["Angstroem"])
        self.backend.addArrayValues("simulation_cell", simulation_cell, unit="angstrom")

    def atomic_system_properties(self, value):
        # Number of atoms
        n_atoms = value["Number of atoms"]
        self.backend.addValue("number_of_atoms", n_atoms)

        # Periodicity
        boundary = value["Boundary Conditions"]
        if boundary == "Free":
            periodic_dimensions = np.array([False, False, False])
        elif boundary == "Periodic":
            periodic_dimensions = np.array([True, True, True])
        elif boundary == "Surface":
            periodic_dimensions = np.array([True, False, True])
        else:
            raise Exception("Unknown boundary condtions.")
        self.backend.addArrayValues("configuration_periodic_dimensions", periodic_dimensions)

    def dft(self, value):
        # Total_charge
        charge = value["qcharge"]
        self.backend.addValue("total_charge", charge)

        # SCF options
        max_iter = value["itermax"]
        self.backend.addValue("scf_max_iteration", max_iter)
        energy_gradient = value["gnrm_cv"]
        self.backend.addRealValue("scf_threshold_energy_change", energy_gradient, unit="hartree")

        # Spin channels
        n_spin = value["nspin"]
        self.backend.addValue("number_of_spin_channels", n_spin)

    def dft_parameters(self, value):
        # XC functional
        exchange_settings = value["eXchange Correlation"]
        xc_id = exchange_settings["XC ID"]

        # LibXC codes
        if xc_id < 0:
            mapping = {
                1: ["LDA_XC_TETER93"],
                2: ["LDA_C_PZ"],
            }

        # ABINIT codes, see
        # http://www.tddft.org/programs/octopus/wiki/index.php/Developers_Manual:ABINIT
        # and
        # http://www.abinit.org/doc/helpfiles/for-v8.0/input_variables/html_automatically_generated/varbas.html#ixc
        else:
            mapping = {
                1: ["LDA_XC_TETER93"],
                2: ["LDA_C_PZ"],
                # 3: Unknown
                4: ["LDA_C_WIGNER"],
                5: ["LDA_C_HL"],
                6: ["LDA_C_XALPHA"],
                # 7: ["LDA_XC_PW"],  # Not really sure...
                # 8: ["LDA_X_PW"],  # Not really sure...
                # 9: ["LDA_X_PW", "LDA_C_RPA"],  # Not really sure...
                # 10: Internal
                11: ["GGA_C_PBE", "GGA_X_PBE"],
                12: ["GGA_X_PBE"],
                # 13: ["GGA_C_PBE","GGA_X_LB"],  # Not really sure...
                # 14: ["GGA_C_PBE","GGA_X_PBE_R"],  # Not really sure...
                15: ["GGA_C_PBE", "GGA_X_RPBE"],
                16: ["GGA_XC_HCTH_93"],
                17: ["GGA_XC_HCTH_120"],
                # 20: Unknown
                # 21: Unknown
                # 22: Unknown
                23: ["GGA_X_WC"],
                24: ["GGA_X_C09X"],
                # 25: Internal
                26: ["GGA_XC_HCTH_147"],
                27: ["GGA_XC_HCTH_147"],
                # 28: Internal
                40: ["HF_X"],
                41: ["HYB_GGA_XC_PBEH"],
                42: ["HYB_GGA_XC_PBE0_13"],
            }

        # Create the XC sections and a summary
        xc = mapping.get(xc_id)
        if xc is None:
            raise Exception("Unknown XC functional.")
        sorted_xc = sorted(xc)
        summary = ""
        n_names = len(sorted_xc)
        for i_name, name in enumerate(sorted_xc):
            weight = 1.0
            xc_id = self.backend.openSection("section_XC_functionals")
            self.backend.addValue("XC_functional_name", name)
            self.backend.addValue("XC_functional_weight", weight)
            self.backend.closeSection("section_XC_functionals", xc_id)
            summary += "{}*{}".format(weight, name)
            if i_name+1 != n_names:
                summary += "_"
        self.backend.addValue("XC_functional", summary)
