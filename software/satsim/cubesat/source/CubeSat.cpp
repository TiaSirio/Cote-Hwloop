// CubeSat.cpp
// CubeSat class implementation file
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
#include <algorithm>          // max
#include <cstddef>            // size_t

// satsim
#include <EnergyConsumer.hpp> // EnergyConsumer
#include <CubeSat.hpp>      // CubeSat
#include <Logger.hpp>         // Logger

namespace satsim {
    // Data retrieved from a benchmark created
    //const double CubeSat::overheadCubeSat = 0.0000076797665693141186;
    const double CubeSat::overheadCubeSat = 0.00330544019226069397;

    CubeSat::CubeSat(
            const double& initialVoltage_V, const PowerState& initialPowerState,
            Logger* logger
    ) : EnergyConsumer(initialVoltage_V, 0.0, logger),
        powerState(initialPowerState), simTime_sec(0.0), workingTime_sec(0.0),
        workerId(0), beginFlag(true), tasksCompleted(0), workingPower(0) {
        this->setPower(getWatt(this->powerState));
    }

    CubeSat* CubeSat::clone() const {
        return new CubeSat(*this);
    }

    double CubeSat::getSimTime() const {
        return this->simTime_sec;
    }

    void CubeSat::setSimTime(const double& seconds) {
        this->simTime_sec = std::max(0.0,seconds);
    }

    size_t CubeSat::getWorkerId() const {
        return this->workerId;
    }

    void CubeSat::setWorkerId(const size_t& id) {
        this->workerId = id;
    }

    size_t CubeSat::getClaimedJobCount() const {
        return this->claimedJobs.size();
    }

    std::deque<Job*> CubeSat::getClaimedJobs() {
        return claimedJobs;
    }

    Job* CubeSat::getFirstClaimedJob() {
        return claimedJobs.at(0);
    }

    int CubeSat::getTasksCompleted() {
        return this->tasksCompleted;
    }

    void CubeSat::addTaskCompleted() {
        this->tasksCompleted++;
    }

    void CubeSat::addClaimedJob(Job* job) {
        this->claimedJobs.push_back(job);
    }

    void CubeSat::cleanClaimedJobs() {
        for(size_t j = 0; j < this->claimedJobs.size(); j++) {
            delete this->claimedJobs.at(j);
            this->claimedJobs.at(j) = nullptr;
        }
    }

    void CubeSat::cleanCompletedJobs() {
        for(size_t j = 0; j < this->completedJobs.size(); j++) {
            delete this->completedJobs.at(j);
            this->completedJobs.at(j) = nullptr;
        }
    }

    size_t CubeSat::getCompletedJobCount() const {
        return this->completedJobs.size();
    }

    std::deque<Job*> CubeSat::getCompletedJobs() {
        return this->completedJobs;
    }

    bool CubeSat::isIdle() const {
        if(this->powerState == PowerState::IDLE) {
            return true;
        } else {
            return false;
        }
    }

    bool CubeSat::isWorking() const {
        return this->powerState == PowerState::WORKING;
    }

    void CubeSat::update(const double& seconds) {
        // Sanitize input
        double sanitizedSeconds = std::max(0.0,seconds);

        // State machine logic
        // If power state is OFF
        if(this->powerState==CubeSat::PowerState::OFF) {


            // Only wake up if voltage is good
            if(this->getVoltage() >= 6.75) {

                // OFF -> WORKING if working was interrupted
                if(this->claimedJobs.size() != 0) {
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-off-stop",
                            this->simTime_sec + sanitizedSeconds
                    );
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-working-start",
                            this->simTime_sec + sanitizedSeconds
                    );
                    setPowerState(CubeSat::PowerState::WORKING);
                }

                // otherwise OFF -> IDLE
                else {
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-off-stop",
                            this->simTime_sec + sanitizedSeconds
                    );
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-idle-start",
                            this->simTime_sec + sanitizedSeconds
                    );
                    setPowerState(CubeSat::PowerState::IDLE);
                }
            }
        }


        // otherwise if power state is SLEEP
        else if(this->powerState == CubeSat::PowerState::SLEEP) {

            // SLEEP -> OFF if voltage is bad
            if(this->getVoltage() < 5.5) {
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-sleep-stop",
                        this->simTime_sec + sanitizedSeconds
                );
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-off-start",
                        this->simTime_sec + sanitizedSeconds
                );
                setPowerState(CubeSat::PowerState::OFF);
            }

            // otherwise if voltage is good
            else if(this->getVoltage() >= 6.75) {
                // SLEEP -> WORKING if working was interrupted
                if(this->claimedJobs.size() != 0) {
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-sleep-stop",
                            this->simTime_sec + sanitizedSeconds
                    );
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-working-start",
                            this->simTime_sec + sanitizedSeconds
                    );
                    setPowerState(CubeSat::PowerState::WORKING);
                }
                    // otherwise SLEEP -> IDLE
                else {
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-sleep-stop",
                            this->simTime_sec + sanitizedSeconds
                    );
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-idle-start",
                            this->simTime_sec + sanitizedSeconds
                    );
                    setPowerState(CubeSat::PowerState::IDLE);
                }
            }
        }


        // otherwise if power state is IDLE
        else if(this->powerState == CubeSat::PowerState::IDLE) {

            // IDLE -> OFF if voltage is bad
            if(this->getVoltage() < 5.5) {
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-idle-stop",
                        this->simTime_sec + sanitizedSeconds
                );
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-off-start",
                        this->simTime_sec + sanitizedSeconds
                );
                setPowerState(CubeSat::PowerState::OFF);
            }

                // IDLE -> SLEEP if voltage is low
            else if(this->getVoltage() < 5.75) {
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-idle-stop",
                        this->simTime_sec + sanitizedSeconds
                );
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-sleep-start",
                        this->simTime_sec + sanitizedSeconds
                );
                setPowerState(CubeSat::PowerState::SLEEP);
            }

                // otherwise IDLE -> WORKING if claimed jobs has been populated
            else if(this->claimedJobs.size() != 0) {
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-idle-stop",
                        this->simTime_sec + sanitizedSeconds
                );
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-working-start",
                        this->simTime_sec + sanitizedSeconds
                );
                setPowerState(CubeSat::PowerState::WORKING);
            }
        }


        // otherwise if power state is WORKING
        else if(this->powerState == CubeSat::PowerState::WORKING) {

            // WORKING -> OFF if voltage is bad
            if(this->getVoltage() < 5.5) {
                this->workingTime_sec = 0.0;
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-working-stop",
                        this->simTime_sec + sanitizedSeconds
                );
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-off-start",
                        this->simTime_sec + sanitizedSeconds
                );
                setPowerState(CubeSat::PowerState::OFF);
            }

            // WORKING -> SLEEP if voltage is low
            else if(this->getVoltage() < 5.75) {
                this->workingTime_sec = 0.0;
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-working-stop",
                        this->simTime_sec + sanitizedSeconds
                );
                this->logEvent(
                        "cubesat-"+std::to_string(this->workerId)+"-sleep-start",
                        this->simTime_sec + sanitizedSeconds
                );
                setPowerState(CubeSat::PowerState::SLEEP);
            }

            // WORKING state update
            else {
                if(this->beginFlag) {
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-begin-work-"+
                            std::to_string(this->claimedJobs.front()->getJobId()),
                            this->simTime_sec
                    );
                    this->beginFlag = false;

                }

                Job* jobToWorkWith = getFirstClaimedJob();

                // Total working time per job
                this->workingTime_sec = this->workingTime_sec + sanitizedSeconds;

                this->claimedJobs.front()->completeTask(this->workerId);

                //Update the power consumed by the WORKING state
                Task taskOfWorkingJob = jobToWorkWith->getTaskToExecute(jobToWorkWith->getTotalTasks(this->workerId));
                jobToWorkWith->addTaskToComplete(this->workerId);

                size_t numberTask = jobToWorkWith->getTotalTasks(this->getWorkerId()) - 1;
                /*this->logEvent(
                        "cubesat-" + std::to_string(this->getWorkerId()) + "-task-" + std::to_string(numberTask) + "-duration",
                        taskOfWorkingJob.getDurationSeconds()
                );*/
                this->logEvent(
                        "cubesat-" + std::to_string(this->workerId) + "-time-job-" + std::to_string(jobToWorkWith->getJobId()),
                        taskOfWorkingJob.getDurationSeconds()
                );

                // Considering that the sampling of the data is every 12 ms
                // Here I'm splitting the total duration of the task (to see how many input it has (if I sample every 12 ms, I divide the time for 100)) and then I multiply every interval by the overhead, to calculate the total overhead
                if (taskOfWorkingJob.getWattBus() < (static_cast<double>(taskOfWorkingJob.getDurationMilliseconds()) / 12) * satsim::CubeSat::overheadCubeSat) {
                    this->workingPower = 0;
                } else {
                    this->workingPower = taskOfWorkingJob.getWattBus() - ((static_cast<double>(taskOfWorkingJob.getDurationMilliseconds()) / 12) * satsim::CubeSat::overheadCubeSat);
                    //std::cout << "WORKING POWER -> " << this->workingPower << " NANO-SAT -> " << this->getWorkerId() << " NUMBER OF TASK -> " << numberTask << std::endl;
                }
                this->setPower(this->workingPower);

                //Save consumption in mJ per each job
                /*this->logConsumption(
                        "cubesat-" + std::to_string(this->workerId) + "-consumption-job-" + std::to_string(jobToWorkWith->getJobId()),
                        this->workingPower
                );*/
                double energy = taskOfWorkingJob.getEnergyBus();
                this->logConsumption(
                        "cubesat-" + std::to_string(this->workerId) + "-consumption-job-" + std::to_string(jobToWorkWith->getJobId()),
                        energy
                );


                if(this->claimedJobs.front()->getClaimedTaskCount(this->workerId) == 0){
                    this->completedJobs.push_back(std::move(this->claimedJobs.front()));
                    claimedJobs.pop_front();
                    this->beginFlag = true;

                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-complete-work-"+
                            std::to_string(this->completedJobs.back()->getJobId()),this->simTime_sec + sanitizedSeconds
                    );
                }

                // if this->claimedJobs.size() == 0, transition to IDLE
                if(this->claimedJobs.size() == 0) {
                    this->workingTime_sec = 0.0;
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-working-stop",
                            this->simTime_sec + sanitizedSeconds
                    );
                    this->logEvent(
                            "cubesat-"+std::to_string(this->workerId)+"-idle-start",
                            this->simTime_sec + sanitizedSeconds
                    );
                    setPowerState(CubeSat::PowerState::IDLE);
                }

                jobToWorkWith = nullptr;
            }
        }
        // Update simulation time
        this->simTime_sec += sanitizedSeconds;
    }

    double CubeSat::getWatt(const CubeSat::PowerState& powerState) {
        // I consider this as energy
        double watt = 0.0;
        switch(powerState) {
            case CubeSat::PowerState::OFF:
                watt = 0.0;
                break;
            case CubeSat::PowerState::SLEEP:
                //watt = 0.5;
                //watt = 0.08141738890992841;
                watt = 0.0008141738890992841;
                //watt = 0.8141738890992841;
                break;
            case CubeSat::PowerState::IDLE:
                //watt = 0.5;
                //watt = 0.08141738890992841;
                watt = 0.0008141738890992841;
                //watt = 0.8141738890992841;
                break;
            case CubeSat::PowerState::WORKING:
                watt = this->workingPower;
                break;
            default:
                watt = 0.0;
                break;
        }
        return watt;
    }

    void CubeSat::setPowerState(const PowerState& powerState) {
        this->powerState = powerState;
        this->setPower(getWatt(this->powerState));
    }
}
