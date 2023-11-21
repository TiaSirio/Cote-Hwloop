// Logger.hpp
// Logger class header file
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

#ifndef SATSIM_LOGGER_HPP
#define SATSIM_LOGGER_HPP

// Standard library
#include <map>     // map
#include <string>  // string
#include <utility> // pair
#include <vector>  // vector
#include <mutex>

namespace satsim {
    class Logger {
    public:
        Logger(const std::string& timeUnits);
        void logEvent(const std::string& name, const double& time);
        void logConsumption(const std::string& name, const double& consumption);
        void logMeasurement(
                const std::string& name, const double& time, const double& measurement
        );
        void exportCsvs(const std::string& pathToDir);
    private:
        std::mutex mutexLoggerEvent;
        std::mutex mutexLoggerMeasurement;
        std::mutex mutexLoggerConsumption;
        std::string timeUnits;
        std::map<std::string,std::vector<double>> eventLogs;
        std::map<std::string,std::vector<double>> eventConsumption;
        std::map<std::string,std::vector<std::pair<double,double>>> measurementLogs;
    };
}

#endif
