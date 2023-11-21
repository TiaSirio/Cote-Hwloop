// Job.cpp
// Job class implementation file
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
#include <algorithm>  // max
#include <string>     // string

// satsim
#include <Logger.hpp> // Logger
#include <Job.hpp>    // Job

namespace satsim {
    Job::Job(const size_t& id, const size_t& taskCount, const size_t& instanceOfSatellite, Logger* logger) :
            id(id), unclaimedTasks(taskCount), instanceOfSatellite(instanceOfSatellite), acquired(false),
            logger(logger), allTasksArrived(false) {}

    Job::Job(const size_t& id, const size_t& taskCount, Logger* logger) :
            id(id), unclaimedTasks(taskCount), logger(logger), allTasksArrived(false),
            instanceOfSatellite(0) {}

    Job* Job::clone() const {
        return new Job(*this);
    }

    size_t Job::getJobId() const {
        return this->id;
    }

    void Job::checkThatAllTasksHaveArrived() {
        for (auto & tasksValue : this->tasksValues) {
            if (!tasksValue.allValuesAddedOnTask()) {
                this->allTasksArrived = false;
                return;
            }
        }
        this->allTasksArrived = true;
    }

    bool Job::getAllTasksArrived() {
        return this->allTasksArrived;
    }

    size_t Job::getUnclaimedTaskCount() const {
        return this->unclaimedTasks;
    }

    size_t Job::getInstanceOfSatellite() const {
        return this->instanceOfSatellite;
    }

    void Job::addTaskValues(Task task) {
        this->tasksValues.push_back(task);
    }

    void Job::addTaskValuesInJob(Task task, int index) {
        if (this->tasksValues.size() < index) {
            this->tasksValues.push_back(task);
        } else {
            this->tasksValues.insert(this->tasksValues.begin() + index - 1, task);
        }
    }

    void Job::clearAddedTask() {
        this->tasksValues.clear();
    }

    Task* Job::getTaskValueAtIndex(int index) {
        if (tasksValues.size() > index) {
            return &(tasksValues[index]);
        } else {
            return nullptr;
        }
        /*
        std::cout << "AAA" << std::endl;
        Task taskToReturn = tasksValues[index];
        taskToReturn.setAppData("BBB");
        return &taskToReturn;
         */
    }

    std::vector<Task> Job::getTasksValues() {
        return this->tasksValues;
    }

    Task Job::getTaskToExecute(int index) {
        return this->tasksValues.at(index);
    }

    size_t Job::getTotalTasks(const size_t& workerId) {
        if(this->taskCounter.count(workerId) != 0) {
            return this->taskCounter.at(workerId);
        } else {
            return 0;
        }
    }

    void Job::setTotalTasks(size_t tasks, const size_t& workerId) {
        if(this->taskCounter.count(workerId) == 0) {
            this->taskCounter[workerId] = 0;
        }
        this->taskCounter[workerId] = tasks;
    }

    void Job::addTaskToComplete(const size_t& workerId) {
        if(this->taskCounter.count(workerId) == 0) {
            this->taskCounter[workerId] = 0;
        }
        this->taskCounter[workerId]++;
    }

    void Job::claimTasks(const size_t& workerId, const size_t& count) {
        this->acquired = true;
        if(this->workerIdToClaimedTaskCount.count(workerId) == 0) {
            this->workerIdToClaimedTaskCount[workerId] = 0;
        }
        if(this->unclaimedTasks < count) {
            this->workerIdToClaimedTaskCount[workerId] += this->unclaimedTasks;
            this->unclaimedTasks = 0;
        } else {
            this->unclaimedTasks -= count;
            this->workerIdToClaimedTaskCount[workerId] += count;
        }
    }

    void Job::unclaimTasks(const size_t& workerId) {
        if(this->workerIdToClaimedTaskCount.count(workerId) != 0) {
            this->unclaimedTasks += this->workerIdToClaimedTaskCount[workerId];
            this->workerIdToClaimedTaskCount[workerId] = 0;
        }
    }

    bool Job::isAcquired() {
        return this->acquired;
    }

    void Job::acquiringJob() {
        this->acquired = true;
    }

    size_t Job::getClaimedTaskCount(const size_t& workerId) const {
        if(this->workerIdToClaimedTaskCount.count(workerId) != 0) {
            //std::cout << "WORKING SATELLITE " << std::to_string(workerId) << " REMAINING TASKS " << std::to_string(this->workerIdToClaimedTaskCount.at(workerId)) << std::endl;
            return this->workerIdToClaimedTaskCount.at(workerId);
        } else {
            return 0;
        }
    }

    size_t Job::getWorkerTaskCount(const size_t& workerId) const {
        size_t total = 0;
        if(this->workerIdToClaimedTaskCount.count(workerId) != 0) {
            total += this->workerIdToClaimedTaskCount.at(workerId);
        }
        if(this->workerIdToCompletedTaskCount.count(workerId) != 0) {
            total += this->workerIdToCompletedTaskCount.at(workerId);
        }
        return total;
    }

    void Job::completeTask(const size_t& workerId) {
        if(this->workerIdToClaimedTaskCount.count(workerId) != 0) {
            if(this->workerIdToCompletedTaskCount.count(workerId) == 0) {
                this->workerIdToCompletedTaskCount[workerId] = 0;
            }
            this->workerIdToClaimedTaskCount[workerId] -= 1;
            this->workerIdToCompletedTaskCount[workerId] += 1;
            //std::cout << "WORKING SATELLITE " << std::to_string(workerId) << " NUMBER OF TASK " << std::to_string(this->workerIdToClaimedTaskCount[workerId]) << std::endl;
        }
    }

    void Job::logEvent(const std::string& name, const double& time) {
        if(this->logger!=NULL) {
            this->logger->logEvent(name, time);
        }
    }

    void Job::logConsumption(const std::string& name, const double& consumption) {
        if(this->logger!=NULL) {
            this->logger->logConsumption(name, consumption);
        }
    }

    void Job::logMeasurement(
            const std::string& name, const double& time, const double& measurement
    ) {
        if(this->logger!=NULL) {
            this->logger->logMeasurement(name, time, measurement);
        }
    }

    void Job::update(const double& seconds) {}
}
