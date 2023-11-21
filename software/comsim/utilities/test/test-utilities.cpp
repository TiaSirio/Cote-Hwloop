// test-utilities.cpp
// Utilities test file
//
// Copyright 2019 Bradley Denby
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may not
// use this file except in compliance with the License. You may obtain a copy of
// the License at <http://www.apache.org/licenses/LICENSE-2.0>.
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations under
// the License.

// Standard library
#include <cstdlib>       // exit, EXIT_SUCCESS
#include <iomanip>       // setprecision
#include <ios>           // fixed, showpoint
#include <iostream>      // cout
#include <ostream>       // endl

// comsim
#include <constants.hpp> // constants
#include <utilities.hpp> // utilities

int main(int argc, char** argv) {
  // Test calcJulianDayFromYMD
  std::cout << "calcJulianDayFromYMD(1995,10,1): "
            << std::fixed << std::showpoint << std::setprecision(2)
            << comsim::util::calcJulianDayFromYMD(1995,10,1)
            << std::endl
            << " Correct result: 2449991.5"
            << std::endl;
  // Test calcGMSTRadFromUT1
  std::cout << "calcGMSTRadFromUT1(2449991.5,0,0): "
            << std::fixed << std::showpoint << std::setprecision(3)
            << comsim::util::calcGMSTRadFromUT1(2449991.5,0,0)/
               comsim::cnst::RAD_PER_DEG
            << std::endl
            << " Correct result: 9.257"
            << std::endl;
  std::cout << "calcGMSTRadFromUT1(2449991.5,32400,0): "
            << std::fixed << std::showpoint << std::setprecision(3)
            << comsim::util::calcGMSTRadFromUT1(2449991.5,32400,0)/
               comsim::cnst::RAD_PER_DEG
            << std::endl
            << " Correct result: 144.627"
            << std::endl;
  std::cout << "calcGMSTRadFromUT1(2449991.5,32400,0): "
            << std::fixed << std::showpoint << std::setprecision(6)
            << comsim::util::calcGMSTRadFromUT1(2449991.5,32400,0)
            << std::endl
            << " Correct result: 2.524218"
            << std::endl;
  // Test dtlla2eci
  std::array<double,3> eciPosn =
   comsim::util::dtlla2eci(
    2449991.5,32400,0,
    40.0*comsim::cnst::RAD_PER_DEG,-75.0*comsim::cnst::RAD_PER_DEG,0.0
   );
  std::cout << "dtlla2eci(2449991.5,32400,0,40.0*RAD_PER_DEG,-75.0*RAD_PER_DEG,0.0): "
            << std::fixed << std::showpoint << std::setprecision(3)
            << eciPosn.at(0) << " " << eciPosn.at(1) << " " << eciPosn.at(2)
            << std::endl
            << " Correct result: 1703.296 4586.651 4077.986"
            << std::endl;
  // Test calcAzimuthDeg
  std::array<double,3> eciPosnSat = {-4400.594, 1932.870, 4760.712};
  std::cout << "calcAzimuthDeg(calcJulianDayFromYMD(1995,11,18),45960,0,45.0*RAD_PER_DEG,-93.0*RAD_PER_DEG,0.0,-4400.594,1932.870,4760.712): "
            << std::fixed << std::showpoint << std::setprecision(2)
            << comsim::util::calcAzimuthDeg(
                comsim::util::calcJulianDayFromYMD(1995,11,18),45960,0,
                45.0*comsim::cnst::RAD_PER_DEG,-93.0*comsim::cnst::RAD_PER_DEG,
                0.0, eciPosnSat
               )
            << std::endl
            << " Correct result: 100.36"
            << std::endl;
  // Test calcElevationDeg
  std::cout << "calcElevationDeg(calcJulianDayFromYMD(1995,11,18),45960,0,45.0*RAD_PER_DEG,-93.0*RAD_PER_DEG,0.0,-4400.594,1932.870,4760.712): "
            << std::fixed << std::showpoint << std::setprecision(2)
            << comsim::util::calcElevationDeg(
                comsim::util::calcJulianDayFromYMD(1995,11,18),45960,0,
                45.0*comsim::cnst::RAD_PER_DEG,-93.0*comsim::cnst::RAD_PER_DEG,
                0.0, eciPosnSat
               )
            << std::endl
            << " Correct result: 81.52"
            << std::endl;
  // Test calcGreatCircleArc
  std::cout << "calcGreatCircleArc(118.80,80.24,100.36,81.52): "
            << std::fixed << std::showpoint << std::setprecision(2)
            << comsim::util::calcGreatCircleArc(118.80,80.24,100.36,81.52)/
               comsim::cnst::RAD_PER_DEG
            << std::endl
            << " Correct result: 3.17"
            << std::endl;
  // Test satellite subpoint latitude
  std::cout << "calcSubpointLatitude(eciPosnSat): "
            << std::fixed << std::showpoint << std::setprecision(2)
            << comsim::util::calcSubpointLatitude(eciPosnSat)
            << std::endl
            << " Correct result: 44.91"
            << std::endl;
  // Test satellite subpoint longitude
  std::cout << "calcSubpointLongitude(comsim::util::calcJulianDayFromYMD(1995,11,18),45960,0,eciPosnSat): "
            << std::fixed << std::showpoint << std::setprecision(2)
            << comsim::util::calcSubpointLongitude(
                comsim::util::calcJulianDayFromYMD(1995,11,18),45960,0,
                eciPosnSat
               )
            << std::endl
            << " Correct result: -92.31"
            << std::endl;
  // Test satellite height above ellipsoid
  std::cout << "calcAltitudeKm(eciPosnSat): "
            << std::fixed << std::showpoint << std::setprecision(3)
            << comsim::util::calcAltitudeKm(eciPosnSat)
            << std::endl
            << " Correct result: 397.505"
            << std::endl;
  std::exit(EXIT_SUCCESS);
}
