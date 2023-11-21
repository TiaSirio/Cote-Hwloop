// Satellite.hpp
// Satellite class header file
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

#ifndef SATSIM_SATELLITE_HPP
#define SATSIM_SATELLITE_HPP

// Standard library
#include <string>     // string

// satsim
#include <ILog.hpp>   // Logger interface
#include <ISim.hpp>   // Simulator interface
#include <Logger.hpp> // Logger
#include <Orbit.hpp>  // Orbit

namespace satsim {
    class Satellite: public ILog, public ISim {
    public:
        Satellite(const Orbit& orbit, Logger* logger=NULL);
        Satellite(const Satellite& satellite) = default;
        Satellite(Satellite&& satellite) = default;
        virtual ~Satellite() = default;
        virtual Satellite& operator=(const Satellite& satellite) = default;
        virtual Satellite& operator=(Satellite&& satellite) = default;
        virtual Satellite* clone() const;
        Orbit getOrbit() const;
        Orbit* getOrbitPtr();
        virtual void logEvent(const std::string& name, const double& time);
        virtual void logConsumption(const std::string& name, const double& consumption);
        virtual void logMeasurement(
                const std::string& name, const double& time, const double& measurement
        );
        virtual void update(const double& seconds);
    private:
        Orbit orbit;
        Logger* logger; // singleton, should not be deleted
    };
}

#endif
