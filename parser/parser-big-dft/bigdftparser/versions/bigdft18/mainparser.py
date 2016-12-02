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
            # "Atomic Forces (Ha/Bohr)": self.atomic_structure
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

    def scf(self, scf):
        """Parse the SCF loop information.
        """
        print("Moi")
        return

    def atomic_structure(self, structure):
        np_positions = []
        np_labels = []
        positions = structure["Positions"]
        for position in positions:
            np_positions.append(*position.values())
            np_labels.append(*position.keys())
        np_positions = np.array(np_positions)
        np_labels = np.array(np_labels)
        self.backend.addArrayValues("atom_positions", np_positions, unit="angstrom")
        self.backend.addArrayValues("atom_labels", np_labels)
        self.backend.addValue("number_of_atoms", np_labels.size)

    def simulation_domain(self, value):
        simulation_cell = np.diag(value["Angstroem"])
        self.backend.addArrayValues("simulation_cell", simulation_cell, unit="angstrom")
