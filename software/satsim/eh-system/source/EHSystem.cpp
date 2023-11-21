// EHSystem.cpp
// EHSystem class implementation file
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
#include <algorithm>    // max
#include <cmath>        // pow, sqrt
#include <string>       // string
#include <utility>      // move

// satsim
#include <Logger.hpp>   // Logger
#include <EHSystem.hpp> // EHSystem

namespace satsim {
    EHSystem::EHSystem(
            const EnergyHarvester& energyHarvester, const Capacitor& capacitor,
            Logger* logger
    ) : energyHarvester(energyHarvester.clone()), capacitor(capacitor),
        logger(logger), totalPower_W(0.0), simTime_sec(0.0) {
        updateNodeVoltage(); // initializes this->nodeVoltage_V
    }

    EHSystem::EHSystem(const EHSystem& ehsystem) :
            energyHarvester(ehsystem.getEnergyHarvester()),
            capacitor(ehsystem.getCapacitor()), totalPower_W(ehsystem.getTotalPower()),
            nodeVoltage_V(ehsystem.getNodeVoltage()), simTime_sec(ehsystem.getSimTime()),
            logger(ehsystem.getLogger()) {
        std::vector<const EnergyConsumer*> energyConsumers =
                ehsystem.getEnergyConsumers();
        for(size_t i=0; i<energyConsumers.size(); i++) {
            this->energyConsumers.push_back(energyConsumers.at(i)->clone());
            delete energyConsumers.at(i);
        }
    }

    EHSystem::EHSystem(EHSystem&& ehsystem) :
            energyHarvester(ehsystem.energyHarvester),
            capacitor(std::move(ehsystem.capacitor)),
            nodeVoltage_V(ehsystem.nodeVoltage_V), simTime_sec(ehsystem.simTime_sec),
            logger(ehsystem.logger) {
        ehsystem.energyHarvester = NULL;
        ehsystem.logger = NULL;
        for(size_t i=0; i<ehsystem.energyConsumers.size(); i++) {
            this->energyConsumers.push_back(ehsystem.energyConsumers.at(i));
            ehsystem.energyConsumers.at(i) = NULL;
        }
    }

    EHSystem::~EHSystem() {
        delete this->energyHarvester;
        for(size_t i=0; i<this->energyConsumers.size(); i++) {
            delete this->energyConsumers.at(i);
        }
    }

    EHSystem& EHSystem::operator=(const EHSystem& ehsystem) {
        EHSystem temp(ehsystem);
        *this = std::move(temp);
        return *this;
    }

    EHSystem& EHSystem::operator=(EHSystem&& ehsystem) {
        delete this->energyHarvester;
        this->energyHarvester = ehsystem.energyHarvester;
        ehsystem.energyHarvester = NULL;
        this->capacitor = std::move(ehsystem.capacitor);
        this->logger = ehsystem.logger;
        ehsystem.logger = NULL;
        for(size_t i=0; i<this->energyConsumers.size(); i++) {
            delete this->energyConsumers.at(i);
        }
        this->energyConsumers.clear();
        this->energyConsumers =
                std::vector<EnergyConsumer*>(ehsystem.energyConsumers.size());
        for(size_t i=0; i<ehsystem.energyConsumers.size(); i++) {
            this->energyConsumers.at(i) = ehsystem.energyConsumers.at(i);
            ehsystem.energyConsumers.at(i) = NULL;
        }
        return *this;
    }

    EnergyHarvester* EHSystem::getEnergyHarvester() const {
        return this->energyHarvester->clone();
    }

    Capacitor EHSystem::getCapacitor() const {
        return this->capacitor;
    }

    std::vector<const EnergyConsumer*> EHSystem::getEnergyConsumers() const {
        std::vector<const EnergyConsumer*> energyConsumers;
        for(size_t i=0; i<this->energyConsumers.size(); i++) {
            energyConsumers.push_back(this->energyConsumers.at(i)->clone());
        }
        return energyConsumers;
    }

    double EHSystem::getTotalPower() const {
        return this->totalPower_W;
    }

    double EHSystem::getNodeVoltage() const {
        return this->nodeVoltage_V;
    }

    double EHSystem::getSimTime() const {
        return this->simTime_sec;
    }

    // Send the actual pointers to allow for energy consumer state updates
    std::vector<EnergyConsumer*> EHSystem::getEnergyConsumers() {
        return this->energyConsumers;
    }

    Logger* EHSystem::getLogger() const {
        return this->logger;
    }

    void EHSystem::addEnergyConsumer(const EnergyConsumer& energyConsumer) {
        this->energyConsumers.push_back(energyConsumer.clone());
    }

    void EHSystem::logEvent(const std::string& name, const double& time) {
        if(this->logger!=NULL) {
            this->logger->logEvent(name, time);
        }
    }

    void EHSystem::logConsumption(const std::string& name, const double& consumption) {
        if(this->logger!=NULL) {
            this->logger->logConsumption(name, consumption);
        }
    }

    void EHSystem::logMeasurement(
            const std::string& name, const double& time, const double& measurement
    ) {
        if(this->logger!=NULL) {
            this->logger->logMeasurement(name, time, measurement);
        }
    }

    void EHSystem::update(const double& seconds) {
        // Sanitize input
        double sanitizedSeconds = std::max(0.0,seconds);

        // Update this->nodeVoltage_V (no time dep, required for all other updates)
        updateNodeVoltage();

        // Update energy harvester and get the current
        this->energyHarvester->setVoltage(this->nodeVoltage_V);

        // Here is called the update of the SimpleSolarCell
        energyHarvester->update(sanitizedSeconds);
        double harvestCurrent_A = energyHarvester->getCurrent();

        // Update each energy consuming device and get the total current draw
        double deviceCurrent_A = 0.0;
        for(size_t i = 0; i < this->energyConsumers.size(); i++) {
            energyConsumers.at(i)->setVoltage(this->nodeVoltage_V);

            // Here is called the update function of all the energy consumers
            energyConsumers.at(i)->update(sanitizedSeconds);

            //After I have updated the watt of the energy consumer, I can retrieve the current draw
            deviceCurrent_A += energyConsumers.at(i)->getCurrent();
        }
        // Takes the sum of just updated energy consumers and sum it
        updateTotalPower(); // call this anytime energy consumers may have changed

        // Update capacitor
        capacitor.setCurrent(harvestCurrent_A - deviceCurrent_A);
        capacitor.update(sanitizedSeconds);

        // Update simulation time
        this->simTime_sec += sanitizedSeconds;
    }



    // (((Solar Cell Amp * OHM Capacitor) + (Charge capacitor/capacity capacitor))^2) - 4 * Charge capacitor * Total power
    // Current of the energy harvester (provided by the solar cell) by the equivalent series resistance (Esr) of the capacitor
    // The charge of the capacitor divided by its capacity, resulting in the voltage across the capacitor.
    // Subtract 4 * the equivalent series resistance (Esr) of the capacitor * the instantaneous power draw of all energy-consuming devices
    // b^2 - 4 * a * c
    double EHSystem::calculateDiscriminant() const {
        return
        std::pow(energyHarvester->getCurrent() * capacitor.getEsr() +
        capacitor.getCharge()/capacitor.getCapacity(), 2.0)
        - 4.0 * capacitor.getEsr() * this->totalPower_W;
    }

    // Multiplies the current of the energy harvester (provided by the solar cell) by the equivalent series resistance (Esr) of the capacitor.
    // It signifies the voltage drop caused by the internal resistance of the capacitor due to the current flowing through it.

    // The charge of the capacitor divided by its capacity, resulting in the voltage across the capacitor.
    // The result represents the voltage contributed by the stored charge in the capacitor.

    // If the discriminant is positive or zero, implying that the quadratic equation has real roots,
    // the inclusion of the square root of the discriminant helps adjust the node voltage calculation
    // while considering the energy harvester's current, the capacitor's equivalent series resistance,
    // and the maximum valid voltage (Cap_V). This adjustment ensures that the calculated node voltage
    // remains within acceptable bounds and satisfies the system's constraints.
    double EHSystem::calculateNodeVoltage() const {
        return
        (energyHarvester->getCurrent() * capacitor.getEsr() +
        capacitor.getCharge()/capacitor.getCapacity() +
        std::sqrt(calculateDiscriminant())) * 0.5;
    }

    void EHSystem::updateTotalPower() {
        double tally_W = 0.0;
        for(size_t i = 0; i < this->energyConsumers.size(); i++) {
            tally_W += energyConsumers.at(i)->getPower();
        }
        this->totalPower_W = tally_W;
    }

    void EHSystem::updateNodeVoltage() {
        // See if system is stable
        if(calculateDiscriminant() < 0.0) {
            //Set energy consumers to 0 because we have reached a blackout of the system
            for(size_t i = 0; i<this->energyConsumers.size(); i++) {
                energyConsumers.at(i)->setOff();
            }
            updateTotalPower();
            logEvent("ehs-blackout", this->simTime_sec);
        }

        this->nodeVoltage_V = calculateNodeVoltage();
    }
}
