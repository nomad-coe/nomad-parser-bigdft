import re
import logging
import numpy as np
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from nomadcore.baseclasses import BasicParser
LOGGER = logging.getLogger("nomad")


#===============================================================================
class BigDFTMainParser(BasicParser):
    """The main parser class that is called for all run types. Parses the NWChem
    output file.
    """
    def __init__(self, file_path, parser_context):
        """
        """
        super(BigDFTMainParser, self).__init__(file_path, parser_context)

    def parse(self):
        """The output file of a BigDFT run is a YAML document. Here we directly
        parse this document with an existing YAML library, and push its
        contents into the backend. Currently this function will read the whole
        document into memory. If this leads to memory issues with large files,
        this function will need to be changed to a token base version.
        """
        with open(self.file_path, "r") as fin:
            data = load(fin, Loader=Loader)

            # Parse SCF information
            scf_data = data["Ground State Optimization"]
            self.scf(scf_data)

    def scf(self, scf):
        """Parse the SCF loop information.
        """
        print("Moi")
        return
