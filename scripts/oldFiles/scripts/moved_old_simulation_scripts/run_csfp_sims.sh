#!/bin/bash
#
# run_csfp_sims.sh
# A bash script that runs the close-spaced, frame-parallel simulations
#
# Copyright 2019 Bradley Denby
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at <http://www.apache.org/licenses/LICENSE-2.0>.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

cd $HOME/git-repos/cote-hwloop/artifacts/csfp-base/scripts/
./run_csfp_base_sims.sh
: '
cd $HOME/git-repos/cote-hwloop/artifacts/csfp-mcap/scripts/
./run_csfp_mcap_sims.sh
cd $HOME/git-repos/cote-hwloop/artifacts/csfp-mpow/scripts/
./run_csfp_mpow_sims.sh
cd $HOME/git-repos/cote-hwloop/artifacts/csfp-mprc/scripts/
./run_csfp_mprc_sims.sh
'
echo "CSFP simulations are running in the background."
echo "It may be awhile before they complete, check with 'top'."
