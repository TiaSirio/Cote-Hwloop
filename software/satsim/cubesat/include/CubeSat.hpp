// CubeSat.hpp
// CubeSat class header file
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

#ifndef CUBESAT_HPP
#define CUBESAT_HPP

// Standard library
#include <cstddef>            // size_t
#include <deque>              // deque

// satsim
#include <EnergyConsumer.hpp> // EnergyConsumer
#include <IWork.hpp>          // IWork
#include <Logger.hpp>         // Logger

namespace satsim {
    class CubeSat: public EnergyConsumer, public IWork {
    public:
        enum class PowerState: uint8_t {
            OFF    = 0,
            SLEEP  = 1,
            IDLE   = 2,
            WORKING = 3
        };
        CubeSat(
                const double& initialVoltage_V, const PowerState& initialPowerState,
                Logger* logger=NULL
        );
        CubeSat(const CubeSat& cubesat) = default;
        CubeSat(CubeSat&& cubesat) = default;
        virtual ~CubeSat() = default;
        virtual CubeSat& operator=(const CubeSat& cubesat) = default;
        virtual CubeSat& operator=(CubeSat&& cubesat) = default;
        virtual CubeSat* clone() const;
        double getSimTime() const;
        void setSimTime(const double& seconds);
        size_t getWorkerId() const;
        void setWorkerId(const size_t& id);
        size_t getClaimedJobCount() const;
        std::deque<Job*> getClaimedJobs();
        Job* getFirstClaimedJob();
        void addClaimedJob(Job* job);
        void cleanClaimedJobs();
        void cleanCompletedJobs();
        size_t getCompletedJobCount() const;
        std::deque<Job*> getCompletedJobs();
        bool isIdle() const;
        bool isWorking() const;
        virtual void update(const double& seconds);
        int getTasksCompleted();
        void addTaskCompleted();
    private:
        static const double overheadCubeSat;
        PowerState powerState;                  // Power state
        double simTime_sec;                     // Simulation time
        double workingTime_sec;                 // Time spent on working task
        size_t workerId;
        int tasksCompleted;
        bool beginFlag;
        std::deque<Job*> claimedJobs;
        std::deque<Job*> completedJobs;
        double workingPower;
        double getWatt(const PowerState& powerState);
        void setPowerState(const PowerState& powerState);
    };
}

#endif
