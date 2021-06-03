#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest

from nomad.datamodel import EntryArchive
from bigdftparser import BigDFTParser


def approx(value, abs=0, rel=1e-6):
    return pytest.approx(value, abs=abs, rel=rel)


@pytest.fixture(scope='module')
def parser():
    return BigDFTParser()


def test_basic(parser):
    archive = EntryArchive()
    parser.parse('tests/data/n2_output.out', archive, None)

    sec_run = archive.section_run[0]
    assert sec_run.program_version == '1.8'

    sec_method = sec_run.section_method[0]
    assert sec_method.scf_max_iteration == 50
    assert sec_method.number_of_spin_channels == 1
    assert sec_method.section_XC_functionals[0].XC_functional_name == 'LDA_XC_TETER93'

    sec_system = sec_run.section_system[0]
    assert sec_system.atom_positions[0][2].magnitude == approx(3.60977554e-10)
    assert sec_system.lattice_vectors[2][2].magnitude == approx(8.3345e-10)
    assert True not in sec_system.configuration_periodic_dimensions

    sec_scc = sec_run.section_single_configuration_calculation[0]
    assert sec_scc.energy_total.value.magnitude == approx(-8.66869132e-17)
    assert sec_scc.forces_total.value[0][2].magnitude == approx(4.67181276e-09)
    sec_scfs = sec_scc.section_scf_iteration
    assert len(sec_scfs) == 11
    assert sec_scfs[3].energy_total_scf_iteration.magnitude == approx(-8.66861188e-17)
    assert sec_scfs[6].energy_XC_potential_scf_iteration.magnitude == approx(-2.7272656e-17)
    assert sec_scfs[7].electronic_kinetic_energy_scf_iteration.magnitude == approx(6.34717211e-17)


def test_1(parser):
    archive = EntryArchive()
    parser.parse('tests/data/periodic.out', archive, None)


def test_2(parser):
    archive = EntryArchive()
    parser.parse('tests/data/abinit_1.out', archive, None)


def test_3(parser):
    archive = EntryArchive()
    parser.parse('tests/data/libxc_101130.out', archive, None)


def test_4(parser):
    archive = EntryArchive()
    parser.parse('tests/data/output.out', archive, None)
