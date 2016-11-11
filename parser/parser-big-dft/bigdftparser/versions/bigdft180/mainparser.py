from __future__ import absolute_import
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.caching_backend import CachingLevel
from nomadcore.baseclasses import MainHierarchicalParser, CacheService
import re
import logging
import numpy as np
LOGGER = logging.getLogger("nomad")


#===============================================================================
class BigDFTMainParser(MainHierarchicalParser):
    """The main parser class that is called for all run types. Parses the NWChem
    output file.
    """
    def __init__(self, file_path, parser_context):
        """
        """
        super(BigDFTMainParser, self).__init__(file_path, parser_context)

        # Cache for storing current method settings
        # self.method_cache = CacheService(self.parser_context)
        # self.method_cache.add("single_configuration_to_calculation_method_ref", single=False, update=False)

        #=======================================================================
        # Cache levels
        # self.caching_levels.update({
            # 'x_nwchem_section_geo_opt_module': CachingLevel.Cache,
            # 'x_nwchem_section_geo_opt_step': CachingLevel.Cache,
            # 'x_nwchem_section_xc_functional': CachingLevel.Cache,
            # 'x_nwchem_section_qmd_module': CachingLevel.ForwardAndCache,
            # 'x_nwchem_section_qmd_step': CachingLevel.ForwardAndCache,
            # 'x_nwchem_section_xc_part': CachingLevel.ForwardAndCache,
        # })

        #=======================================================================
        # Main Structure
        self.root_matcher = SM("",
            forwardMatch=True,
            sections=['section_run'],
            subMatchers=[
                self.input(),
                self.header(),
                self.system(),

                # This repeating submatcher supports multiple different tasks
                # within one run
                SM("(?:\s+NWChem DFT Module)|(?:\s+NWChem Geometry Optimization)|(?:\s+NWChem QMD Module)|(?:\s+\*               NWPW PSPW Calculation              \*)",
                    repeats=True,
                    forwardMatch=True,
                    subFlags=SM.SubFlags.Unordered,
                    subMatchers=[
                        self.energy_force_gaussian_task(),
                        self.energy_force_pw_task(),
                        self.geo_opt_module(),
                        self.dft_gaussian_md_task(),
                    ]
                ),
            ]
        )

    #=======================================================================
    # onClose triggers
    def onClose_section_run(self, backend, gIndex, section):
        backend.addValue("program_name", "NWChem")
        backend.addValue("program_basis_set_type", "gaussians+plane_waves")

    #=======================================================================
    # onOpen triggers
    def onOpen_section_method(self, backend, gIndex, section):
        self.method_cache["single_configuration_to_calculation_method_ref"] = gIndex

    #=======================================================================
    # adHoc
    def adHoc_forces(self, save_positions=False):
        def wrapper(parser):
            match = True
            forces = []
            positions = []

            while match:
                line = parser.fIn.readline()
                if line == "" or line.isspace():
                    match = False
                    break
                components = line.split()
                position = np.array([float(x) for x in components[-6:-3]])
                force = np.array([float(x) for x in components[-3:]])
                forces.append(force)
                positions.append(position)

            forces = -np.array(forces)
            positions = np.array(positions)

            # If anything found, push the results to the correct section
            if forces.size != 0:
                self.scc_cache["atom_forces"] = forces
            if save_positions:
                if positions.size != 0:
                    self.system_cache["atom_positions"] = positions
        return wrapper

    #=======================================================================
    # SimpleMatcher specific onClose
    def save_geo_opt_sampling_id(self, backend, gIndex, section):
        backend.addValue("frame_sequence_to_sampling_ref", gIndex)

    #=======================================================================
    # Start match transforms
    def transform_dipole(self, backend, groups):
        dipole = groups[0]
        components = np.array([float(x) for x in dipole.split()])
        backend.addArrayValues("x_nwchem_qmd_step_dipole", components)

    #=======================================================================
    # Misc
    def debug_end(self):
        def wrapper():
            print("DEBUG")
        return wrapper
