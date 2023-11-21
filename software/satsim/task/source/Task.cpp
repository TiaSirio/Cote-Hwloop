// Task.cpp

#define PLUS_X_V 0
#define PLUS_X_A 1
#define PLUS_Y_V 2
#define PLUS_Y_A 3
#define BAT_V 4
#define BAT_A 5
#define BUS_V 6
#define BUS_A 7
#define MINUS_X_V 8
#define MINUS_X_A 9
#define MINUS_Y_V 10
#define MINUS_Y_A 11
#define PLUS_Z_V 12
#define PLUS_Z_A 13
#define MINUS_Z_V 14
#define MINUS_Z_A 15
#define IHU_TEMP 16

#define RSSI 0
#define SPIN 1
#define TEMP 2
#define PRES 3
#define ALT 4
#define HUMI 5
#define GYRO_X 7
#define GYRO_Y 8
#define GYRO_Z 9
#define ACCEL_X 10
#define ACCEL_Y 11
#define ACCEL_Z 12
#define XS1 14
#define XS2 15
#define XS3 16


#include <ios>
#include <vector>
#include <numeric>

#include <Task.hpp>

namespace satsim {
    Task::Task(size_t duration) : missingValueOfTask(4), duration(duration) {
        this->non_func_data = std::vector<std::vector<double>>();
        this->payload_data = std::vector<std::vector<double>>();
        this->timestamps_non_func = std::vector<size_t>();
        this->timestamps_payload = std::vector<size_t>();
        //this->app_data = "";
        //this->non_func_data = std::vector<std::vector<double>>{};
        //this->payload_data = std::vector<std::vector<double>>{};
        //this->timestamps_non_func = std::vector<size_t>{};
        //this->timestamps_payload = std::vector<size_t>{};
    }

    Task* Task::clone() const {
        return new Task(*this);
    }

    Task::Task(size_t duration, std::string app_data, std::vector<std::vector<double>> non_func_data,
               std::vector<std::vector<double>> payload_data, std::vector<size_t> timestamps_non_func,
               std::vector<size_t> timestamps_payload) : duration(duration),
               app_data(app_data), non_func_data(non_func_data),
               payload_data(payload_data), timestamps_non_func(timestamps_non_func),
               timestamps_payload(timestamps_payload), missingValueOfTask(0){}

    bool Task::allValuesAddedOnTask() {
        return this->missingValueOfTask == 0;
    }

    std::vector<std::vector<double>> Task::getNonFuncData() {
        return this->non_func_data;
    }

    std::vector<std::vector<double>> Task::getPayloadData() {
        return this->payload_data;
    }

    size_t Task::getDurationMilliseconds() {
        return this->duration;
    }

    double Task::getDurationSeconds() {
        return static_cast<double>(this->duration) / 1000;
    }

    std::string Task::getAppData() {
        return this->app_data;
    }

    std::vector<size_t> Task::getTimestampsNonFuncData() {
        return this->timestamps_non_func;
    }

    std::vector<size_t> Task::getTimestampsPayloadData() {
        return this->timestamps_payload;
    }

    void Task::setNonFuncData(const std::string& msg) {
        //std::cout << "AAA" << std::endl;
        this->non_func_data = doubleSplitTask(msg, ";", ",");
    }

     void Task::setPayloadData(const std::string& msg) {
         //std::cout << "BBB" << std::endl;
         this->payload_data = doubleSplitTask(msg, ";", ",");

    }

    void Task::setDurationMilliseconds(const size_t& dur) {
        //std::cout << "CCC" << std::endl;
        this->duration = dur;
        this->missingValueOfTask--;
    }

    void Task::setAppData(const std::string& app) {
        //std::cout << "DDD" << std::endl;
        this->app_data = app;
        this->missingValueOfTask--;
    }

    void Task::setTimestampsNonFuncData(const std::string& msg) {
        //std::cout << "EEE" << std::endl;
        this->timestamps_non_func = innerSplitFirstValueTask(msg, ";", ",");
        this->missingValueOfTask--;
    }

    void Task::setTimestampsPayloadData(const std::string& msg) {
        //std::cout << "FFF" << std::endl;
        this->timestamps_payload = innerSplitFirstValueTask(msg, ";", ",");
        this->missingValueOfTask--;
    }

    std::vector<double> Task::getVoltSolarPanelPlusX() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->voltSolarPanelPlusX.empty()){
            return this->voltSolarPanelPlusX;
        } else {
            for(auto & val : this->non_func_data){
                this->voltSolarPanelPlusX.push_back(val[PLUS_X_V]);
            }
            return this->voltSolarPanelPlusX;
        }
    }

    std::vector<double> Task::getAmpereSolarPanelPlusX() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ampereSolarPanelPlusX.empty()) {
            return this->ampereSolarPanelPlusX;
        } else {
            for (auto& val : this->non_func_data) {
                this->ampereSolarPanelPlusX.push_back(val[PLUS_X_A]/1000);
            }
            return this->ampereSolarPanelPlusX;
        }
    }

    std::vector<double> Task::getWattArraySolarPanelPlusX() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->wattArraySolarPanelPlusX.empty()) {
            return this->wattArraySolarPanelPlusX;
        } else {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelPlusX.push_back(val[PLUS_X_V] * val[PLUS_X_A]/1000);
            }
            return this->wattArraySolarPanelPlusX;
        }
    }

    void Task::fillWattArraySolarPanelPlusX() {
        if (this->non_func_data.empty()){
            return;
        }
        if (this->wattArraySolarPanelPlusX.empty()) {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelPlusX.push_back(val[PLUS_X_V] * val[PLUS_X_A]/1000);
            }
        }
    }

    double Task::getWattSolarPanelPlusX() {
        if (this->non_func_data.empty()){
            this->wattSolarPanelPlusX = 0;
            return this->wattSolarPanelPlusX;
        }
        if (this->wattArraySolarPanelPlusX.empty()) {
            fillWattArraySolarPanelPlusX();
        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArraySolarPanelPlusX);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattSolarPanelPlusX = calculateTotalEnergy(periodAverages, timestampRanges);
        //this->wattSolarPanelPlusX = std::accumulate(this->wattArraySolarPanelPlusX.begin(), this->wattArraySolarPanelPlusX.end(), decltype(this->wattArraySolarPanelPlusX)::value_type(0.0f));
        return this->wattSolarPanelPlusX;
    }

    std::vector<double> Task::getVoltSolarPanelMinusX() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->voltSolarPanelMinusX.empty()) {
            return this->voltSolarPanelMinusX;
        } else {
            for (auto& val : this->non_func_data) {
                this->voltSolarPanelMinusX.push_back(val[MINUS_X_V]);
            }
            return this->voltSolarPanelMinusX;
        }
    }

    std::vector<double> Task::getAmpereSolarPanelMinusX() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ampereSolarPanelMinusX.empty()) {
            return this->ampereSolarPanelMinusX;
        } else {
            for (auto& val : this->non_func_data) {
                this->ampereSolarPanelMinusX.push_back(val[MINUS_X_A]/1000);
            }
            return this->ampereSolarPanelMinusX;
        }
    }

    std::vector<double> Task::getWattArraySolarPanelMinusX() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->wattArraySolarPanelMinusX.empty()) {
            return this->wattArraySolarPanelMinusX;
        } else {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelMinusX.push_back(val[MINUS_X_V] * val[MINUS_X_A]/1000);
            }
            return this->wattArraySolarPanelMinusX;
        }
    }

    void Task::fillWattArraySolarPanelMinusX() {
        if (this->non_func_data.empty()){
            return;
        }
        if (this->wattArraySolarPanelMinusX.empty()) {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelMinusX.push_back(val[MINUS_X_V] * val[MINUS_X_A]/1000);
            }
        }
    }

    double Task::getWattSolarPanelMinusX() {
        if (this->non_func_data.empty()){
            this->wattSolarPanelMinusX = 0;
            return this->wattSolarPanelMinusX;
        }
        if (this->non_func_data.empty()){
            this->wattSolarPanelMinusX = 0;
            return this->wattSolarPanelMinusX;
        }
        if (this->wattArraySolarPanelMinusX.empty()) {
            fillWattArraySolarPanelMinusX();
        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArraySolarPanelMinusX);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattSolarPanelMinusX = calculateTotalEnergy(periodAverages, timestampRanges);
        return this->wattSolarPanelMinusX;
    }

    std::vector<double> Task::getVoltSolarPanelPlusY() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->voltSolarPanelPlusY.empty()) {
            return this->voltSolarPanelPlusY;
        } else {
            for (auto& val : this->non_func_data) {
                this->voltSolarPanelPlusY.push_back(val[PLUS_Y_V]);
            }
            return this->voltSolarPanelPlusY;
        }
    }

    std::vector<double> Task::getAmpereSolarPanelPlusY() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ampereSolarPanelPlusY.empty()) {
            return this->ampereSolarPanelPlusY;
        } else {
            for (auto& val : this->non_func_data) {
                this->ampereSolarPanelPlusY.push_back(val[PLUS_Y_A]/1000);
            }
            return this->ampereSolarPanelPlusY;
        }
    }

    std::vector<double> Task::getWattArraySolarPanelPlusY() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->wattArraySolarPanelPlusY.empty()) {
            return this->wattArraySolarPanelPlusY;
        } else {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelPlusY.push_back(val[PLUS_Y_V] * val[PLUS_Y_A]/1000);
            }
            return this->wattArraySolarPanelPlusY;
        }
    }

    void Task::fillWattArraySolarPanelPlusY() {
        if (this->non_func_data.empty()){
            return;
        }
        if (this->wattArraySolarPanelPlusY.empty()) {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelPlusY.push_back(val[PLUS_Y_V] * val[PLUS_Y_A]/1000);
            }
        }
    }

    double Task::getWattSolarPanelPlusY() {
        if (this->non_func_data.empty()){
            this->wattSolarPanelPlusY = 0;
            return this->wattSolarPanelPlusY;
        }
        if (this->wattArraySolarPanelPlusY.empty()) {
            fillWattArraySolarPanelPlusY();
        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArraySolarPanelPlusY);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattSolarPanelPlusY = calculateTotalEnergy(periodAverages, timestampRanges);
        return this->wattSolarPanelPlusY;
    }

    std::vector<double> Task::getVoltSolarPanelMinusY() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->voltSolarPanelMinusY.empty()) {
            return this->voltSolarPanelMinusY;
        } else {
            for (auto &val: this->non_func_data) {
                this->voltSolarPanelMinusY.push_back(val[MINUS_Y_V]);
            }
            return this->voltSolarPanelMinusY;
        }
    }

    std::vector<double> Task::getAmpereSolarPanelMinusY() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ampereSolarPanelMinusY.empty()) {
            return this->ampereSolarPanelMinusY;
        } else {
            for (auto& val : this->non_func_data) {
                this->ampereSolarPanelMinusY.push_back(val[MINUS_Y_A]/1000);
            }
            return this->ampereSolarPanelMinusY;
        }
    }

    std::vector<double> Task::getWattArraySolarPanelMinusY() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->wattArraySolarPanelMinusY.empty()) {
            return this->wattArraySolarPanelMinusY;
        } else {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelMinusY.push_back(val[MINUS_Y_V] * val[MINUS_Y_A]/1000);
            }
            return this->wattArraySolarPanelMinusY;
        }
    }

    void Task::fillWattArraySolarPanelMinusY() {
        if (this->non_func_data.empty()){
            return;
        }
        if (this->wattArraySolarPanelMinusY.empty()) {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelMinusY.push_back(val[MINUS_Y_V] * val[MINUS_Y_A]/1000);
            }
        }
    }

    double Task::getWattSolarPanelMinusY() {
        if (this->non_func_data.empty()){
            this->wattSolarPanelMinusY = 0;
            return this->wattSolarPanelMinusY;
        }
        if (this->wattArraySolarPanelMinusY.empty()) {
            fillWattArraySolarPanelMinusY();
        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArraySolarPanelMinusY);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattSolarPanelMinusY = calculateTotalEnergy(periodAverages, timestampRanges);
        return this->wattSolarPanelMinusY;
    }

    std::vector<double> Task::getVoltSolarPanelPlusZ() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->voltSolarPanelPlusZ.empty()) {
            return this->voltSolarPanelPlusZ;
        } else {
            for (auto& val : this->non_func_data) {
                this->voltSolarPanelPlusZ.push_back(val[PLUS_Z_V]);
            }
            return this->voltSolarPanelPlusZ;
        }
    }

    std::vector<double> Task::getAmpereSolarPanelPlusZ() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ampereSolarPanelPlusZ.empty()) {
            return this->ampereSolarPanelPlusZ;
        } else {
            for (auto& val : this->non_func_data) {
                this->ampereSolarPanelPlusZ.push_back(val[PLUS_Z_A]/1000);
            }
            return this->ampereSolarPanelPlusZ;
        }
    }

    std::vector<double> Task::getWattArraySolarPanelPlusZ() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->wattArraySolarPanelPlusZ.empty()) {
            return this->wattArraySolarPanelPlusZ;
        } else {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelPlusZ.push_back(val[PLUS_Z_V] * val[PLUS_Z_A]/1000);
            }
            return this->wattArraySolarPanelPlusZ;
        }
    }

    void Task::fillWattArraySolarPanelPlusZ() {
        if (this->non_func_data.empty()){
            return;
        }
        if (this->wattArraySolarPanelPlusZ.empty()) {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelPlusZ.push_back(val[PLUS_Z_V] * val[PLUS_Z_A]/1000);
            }
        }
    }

    double Task::getWattSolarPanelPlusZ() {
        if (this->non_func_data.empty()){
            this->wattSolarPanelPlusZ = 0;
            return this->wattSolarPanelPlusZ;
        }
        if (this->wattArraySolarPanelPlusZ.empty()) {
            fillWattArraySolarPanelPlusZ();
        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArraySolarPanelPlusZ);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattSolarPanelPlusZ = calculateTotalEnergy(periodAverages, timestampRanges);
        return this->wattSolarPanelPlusZ;
    }

    std::vector<double> Task::getVoltSolarPanelMinusZ() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->voltSolarPanelMinusZ.empty()) {
            return this->voltSolarPanelMinusZ;
        } else {
            for (auto& val : this->non_func_data) {
                this->voltSolarPanelMinusZ.push_back(val[MINUS_Z_V]);
            }
            return this->voltSolarPanelMinusZ;
        }
    }

    std::vector<double> Task::getAmpereSolarPanelMinusZ() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ampereSolarPanelMinusZ.empty()) {
            return this->ampereSolarPanelMinusZ;
        } else {
            for (auto& val : this->non_func_data) {
                this->ampereSolarPanelMinusZ.push_back(val[MINUS_Z_A]/1000);
            }
            return this->ampereSolarPanelMinusZ;
        }
    }

    std::vector<double> Task::getWattArraySolarPanelMinusZ() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->wattArraySolarPanelMinusZ.empty()) {
            return this->wattArraySolarPanelMinusZ;
        } else {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelMinusZ.push_back(val[MINUS_Z_V] * val[MINUS_Z_A]/1000);
            }
            return this->wattArraySolarPanelMinusZ;
        }
    }

    void Task::fillWattArraySolarPanelMinusZ() {
        if (this->non_func_data.empty()){
            return;
        }
        if (this->wattArraySolarPanelMinusZ.empty()) {
            for (auto& val : this->non_func_data) {
                this->wattArraySolarPanelMinusZ.push_back(val[MINUS_Z_V] * val[MINUS_Z_A]/1000);
            }
        }
    }

    double Task::getWattSolarPanelMinusZ() {
        if (this->non_func_data.empty()){
            this->wattSolarPanelMinusZ = 0;
            return this->wattSolarPanelMinusZ;
        }
        if (this->wattArraySolarPanelMinusZ.empty()) {
            fillWattArraySolarPanelMinusZ();
        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArraySolarPanelMinusZ);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattSolarPanelMinusZ = calculateTotalEnergy(periodAverages, timestampRanges);
        return this->wattSolarPanelMinusZ;
    }

    std::vector<double> Task::getVoltBattery() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->voltBattery.empty()) {
            return this->voltBattery;
        } else {
            for (auto& val : this->non_func_data) {
                this->voltBattery.push_back(val[BAT_V]);
            }
            return this->voltBattery;
        }
    }

    std::vector<double> Task::getAmpereBattery() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ampereBattery.empty()) {
            return this->ampereBattery;
        } else {
            for (auto& val : this->non_func_data) {
                this->ampereBattery.push_back(val[BAT_A]/1000);
            }
            return this->ampereBattery;
        }
    }

    std::vector<double> Task::getWattArrayBattery() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->wattArrayBattery.empty()) {
            return this->wattArrayBattery;
        } else {
            for (auto& val : this->non_func_data) {
                this->wattArrayBattery.push_back(val[BAT_V] * val[BAT_A]/1000);
            }
            return this->wattArrayBattery;
        }
    }

    void Task::fillWattArrayBattery() {
        if (this->non_func_data.empty()){
            return;
        }
        if (this->wattArrayBattery.empty()) {
            for (auto& val : this->non_func_data) {
                this->wattArrayBattery.push_back(val[BAT_V] * val[BAT_A]/1000);
            }
        }
    }

    double Task::getWattBattery() {
        if (this->non_func_data.empty()){
            this->wattBattery = 0;
            return this->wattBattery;
        }
        if (this->wattArrayBattery.empty()) {
            fillWattArrayBattery();

        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArrayBattery);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattBattery = calculateTotalEnergy(periodAverages, timestampRanges);
        return this->wattBattery;
    }

    std::vector<double> Task::getVoltBus() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->voltBus.empty()) {
            return this->voltBus;
        } else {
            for (auto& val : this->non_func_data) {
                this->voltBus.push_back(val[BUS_V]);
            }
            return this->voltBus;
        }
    }

    std::vector<double> Task::getAmpereBus() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ampereBus.empty()) {
            return this->ampereBus;
        } else {
            for (auto& val : this->non_func_data) {
                this->ampereBus.push_back(val[BUS_A]/1000);
            }
            return this->ampereBus;
        }
    }

    std::vector<double> Task::getWattArrayBus() {
        if (this->non_func_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->wattArrayBus.empty()) {
            return this->wattArrayBus;
        } else {
            for (auto& val : this->non_func_data) {
                this->wattArrayBus.push_back(val[BUS_V] * val[BUS_A]/1000);
            }
            return this->wattArrayBus;
        }
    }

    void Task::fillWattArrayBus() {
        if (this->non_func_data.empty()){
            return;
        }
        if (this->wattArrayBus.empty()) {
            for (auto& val : this->non_func_data) {
                this->wattArrayBus.push_back(val[BUS_V] * val[BUS_A]/1000);
            }
        }
    }

    double Task::getWattBus() {
        if (this->non_func_data.empty()){
            this->wattBus = 0;
            return this->wattBus;
        }
        if (this->wattArrayBus.empty()) {
            fillWattArrayBus();
        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArrayBus);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattBus = calculateTotalPower(periodAverages);
        this->energyBus = calculateTotalEnergy(periodAverages, timestampRanges);
        if (this->wattBus < 0) {
            this->wattBus = this->wattBus * -1;
        }
        if (this->energyBus < 0) {
            this->energyBus = this->energyBus * -1;
        }
        return this->wattBus;
    }

    double Task::getEnergyBus() {
        return this->energyBus;
    }

    /*double Task::getWattBusPositive() {
        if (this->non_func_data.empty()){
            this->wattBus = 0;
            return this->wattBus;
        }
        if (this->wattArrayBus.empty()) {
            fillWattArrayBus();
        }
        std::vector<double> periodAverages = calculatePeriodAverages(this->wattArrayBus);
        std::vector<size_t> timestampRanges = calculateTimestampRanges(this->timestamps_non_func);
        this->wattBus = calculateTotalEnergy(periodAverages, timestampRanges);
        if (this->wattBus < 0) {
            this->wattBus = this->wattBus * -1;
        }
        return this->wattBus;
    }*/

    std::vector<double> Task::getRSSI() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->rssiVal.empty()) {
            return this->rssiVal;
        } else {
            for (auto& val : this->payload_data) {
                this->rssiVal.push_back(val[RSSI]);
            }
            return this->rssiVal;
        }
    }

    std::vector<double> Task::getIHUTemp() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->ihuTemp.empty()) {
            return this->ihuTemp;
        } else {
            for (auto& val : this->payload_data) {
                this->ihuTemp.push_back(val[IHU_TEMP]);
            }
            return this->ihuTemp;
        }
    }

    std::vector<double> Task::getSPIN() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->spinVal.empty()) {
            return this->spinVal;
        } else {
            for (auto& val : this->payload_data) {
                this->spinVal.push_back(val[SPIN]);
            }
            return this->spinVal;
        }
    }

    std::vector<double> Task::getTemperature() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->temperaturePayload.empty()) {
            return this->temperaturePayload;
        } else {
            for (auto& val : this->payload_data) {
                this->temperaturePayload.push_back(val[TEMP]);
            }
            return this->temperaturePayload;
        }
    }

    std::vector<double> Task::getPressure() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->pressurePayload.empty()) {
            return this->pressurePayload;
        } else {
            for (auto& val : this->payload_data) {
                this->pressurePayload.push_back(val[PRES]);
            }
            return this->pressurePayload;
        }
    }

    std::vector<double> Task::getAltitude() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->altitudePayload.empty()) {
            return this->altitudePayload;
        } else {
            for (auto& val : this->payload_data) {
                this->altitudePayload.push_back(val[ALT]);
            }
            return this->altitudePayload;
        }
    }

    std::vector<double> Task::getHumidity() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->humidityPayload.empty()) {
            return this->humidityPayload;
        } else {
            for (auto& val : this->payload_data) {
                this->humidityPayload.push_back(val[HUMI]);
            }
            return this->humidityPayload;
        }
    }

    std::vector<double> Task::getGyroX() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->gyroX.empty()) {
            return this->gyroX;
        } else {
            for (auto& val : this->payload_data) {
                this->gyroX.push_back(val[GYRO_X]);
            }
            return this->gyroX;
        }
    }

    std::vector<double> Task::getGyroY() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->gyroY.empty()) {
            return this->gyroY;
        } else {
            for (auto& val : this->payload_data) {
                this->gyroY.push_back(val[GYRO_Y]);
            }
            return this->gyroY;
        }
    }

    std::vector<double> Task::getGyroZ() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->gyroZ.empty()) {
            return this->gyroZ;
        } else {
            for (auto& val : this->payload_data) {
                this->gyroZ.push_back(val[GYRO_Z]);
            }
            return this->gyroZ;
        }
    }

    std::vector<double> Task::getAccelX() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->accelX.empty()) {
            return this->accelX;
        } else {
            for (auto& val : this->payload_data) {
                this->accelX.push_back(val[ACCEL_X]);
            }
            return this->accelX;
        }
    }

    std::vector<double> Task::getAccelY() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->accelY.empty()) {
            return this->accelY;
        } else {
            for (auto& val : this->payload_data) {
                this->accelY.push_back(val[ACCEL_Y]);
            }
            return this->accelY;
        }
    }

    std::vector<double> Task::getAccelZ() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->accelZ.empty()) {
            return this->accelZ;
        } else {
            for (auto& val : this->payload_data) {
                this->accelZ.push_back(val[ACCEL_Z]);
            }
            return this->accelZ;
        }
    }

    std::vector<double> Task::getXS1() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->xs1Val.empty()) {
            return this->xs1Val;
        } else {
            for (auto& val : this->payload_data) {
                this->xs1Val.push_back(val[XS1]);
            }
            return this->xs1Val;
        }
    }

    std::vector<double> Task::getXS2() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->xs2Val.empty()) {
            return this->xs2Val;
        } else {
            for (auto& val : this->payload_data) {
                this->xs2Val.push_back(val[XS2]);
            }
            return this->xs2Val;
        }
    }

    std::vector<double> Task::getXS3() {
        if (this->payload_data.empty()){
            static const std::vector<double> emptyVector;
            return emptyVector;
        }
        if (!this->xs3Val.empty()) {
            return this->xs3Val;
        } else {
            for (auto& val : this->payload_data) {
                this->xs3Val.push_back(val[XS3]);
            }
            return this->xs3Val;
        }
    }

    void Task::printNonFuncData() {
        for(int i = 0; i < this->non_func_data.size(); i++){
            for(int j=0; j < this->non_func_data[i].size(); j++)
                std::cout << this->non_func_data[i][j] << " ";
            std::cout << std::endl;
        }
    }

    void Task::printPayloadData() {
        for(int i = 0; i < this->payload_data.size(); i++){
            for(int j = 0; j < this->payload_data[i].size() ; j++)
                std::cout << this->payload_data[i][j] << " ";
            std::cout << std::endl;
        }
    }

    void Task::printTimestampNonFuncData() {
        for(int j = 0; j < this->timestamps_non_func.size(); j++)
            std::cout << this->timestamps_non_func[j] << " ";
        std::cout << std::endl;
    }

    void Task::printTimestampPayloadData() {
        for(int j = 0; j < this->timestamps_payload.size(); j++)
            std::cout << this->timestamps_payload[j] << " ";
        std::cout << std::endl;
    }


    std::vector<std::vector<double>> Task::doubleSplitTask(const std::string& s, std::string outerDel, std::string innerDel)
    {
        int start, end = -1*outerDel.size();
        bool firstVal = true;
        std::vector<std::vector<double>> finalResult;
        std::vector<double> tempResults;
        std::vector<std::string> intermediateResults;
        do {
            start = end + outerDel.size();
            end = s.find(outerDel, start);
            //std::cout << s.substr(start, end - start) << std::endl;
            intermediateResults.push_back(s.substr(start, end - start));
        } while (end != -1);
        for (int k = 0; k < intermediateResults.size(); k++) {
            end = -1*innerDel.size();
            do {
                start = end + innerDel.size();
                end = intermediateResults[k].find(innerDel, start);
                //std::cout << s.substr(start, end - start) << std::endl;
                if (!firstVal) {
                    tempResults.push_back(std::stof(intermediateResults[k].substr(start, end - start)));
                } else {
                    firstVal = false;
                }
            } while (end != -1);
            finalResult.push_back(tempResults);
            tempResults.clear();
            firstVal = true;
        }
        return finalResult;
    }

    std::vector<size_t> Task::innerSplitFirstValueTask(const std::string& s, std::string outerDel, std::string innerDel)
    {
        int start, end = -1 * outerDel.size();
        std::vector<size_t> finalResult;
        std::vector<std::string> intermediateResults;
        size_t temp;
        do {
            start = end + outerDel.size();
            end = s.find(outerDel, start);
            //std::cout << s.substr(start, end - start) << std::endl;
            intermediateResults.push_back(s.substr(start, end - start));
        } while (end != -1);
        for (int k = 0; k < intermediateResults.size(); k++) {
            end = -1 * innerDel.size();
            start = end + innerDel.size();
            end = intermediateResults[k].find(innerDel, start);
            //std::cout << s.substr(start, end - start) << std::endl;
            std::stringstream stream(intermediateResults[k].substr(start, end - start));
            stream >> temp;
            finalResult.push_back(temp);
            temp = 0;
            //finalResult.push_back(std::stoi(intermediateResults[k].substr(start, end - start)));
        }
        return finalResult;
    }

    std::vector<double> Task::calculatePeriodAverages(const std::vector<double>& watts) {
        std::vector<double> periodAverages;

        if (watts.size() == 0) {
            periodAverages.push_back(0);
            return periodAverages;
        } else if (watts.size() == 1) {
            periodAverages.push_back(watts[0]);
            return periodAverages;
        }

        for (size_t i = 0; i < watts.size() - 1; i++) {
            double average = (watts[i] + watts[i + 1]) / 2.0;
            periodAverages.push_back(average);
        }

        return periodAverages;
    }

    std::vector<size_t> Task::calculateTimestampRanges(const std::vector<size_t>& timestamps) {
        std::vector<size_t> timestampRanges;

        // With size 0, we are not interested in timestamp, since the value of Watt is 0
        if (timestamps.size() == 0) {
            timestampRanges.push_back(100);
            return timestampRanges;
        } else if (timestamps.size() == 1) {
            timestampRanges.push_back(this->getDurationMilliseconds());
            return timestampRanges;
        }

        // Data are sent from the last arrived till the first, so they are in reverse order
        for (size_t i = 0; i < timestamps.size() - 1; i++) {
            double average = (timestamps[i] - timestamps[i + 1]);
            timestampRanges.push_back(average);
        }

        return timestampRanges;
    }

    double Task::calculateTotalEnergy(const std::vector<double>& periodAverages, const std::vector<size_t>& timestampRanges) {
        if (periodAverages.size() != timestampRanges.size()) {
            // Handle error - the number of period averages and timestamp ranges should match
            return 0.0;
        }


        // This is the energy, so I have to calculate [Watt * ms]
        double totalEnergy = 0.0;
        if (periodAverages.size() == 0 && timestampRanges.size() == 0) {
            return 0.0;
        } else if (periodAverages.size() == 1 && timestampRanges.size() == 1) {
            totalEnergy = periodAverages[0] * timestampRanges[0];
            //totalEnergy = totalEnergy / this->getDurationMilliseconds();
            //totalEnergy = totalEnergy * this->getDurationMilliseconds();
            return totalEnergy;
        }

        for (size_t i = 0; i < periodAverages.size(); i++) {
            double energyUsed = periodAverages[i] * timestampRanges[i];
            totalEnergy += energyUsed;
        }
        //size_t totalTime = this->timestamps_non_func[timestamps_non_func.size() - 1] - this->timestamps_non_func[0];
        //size_t totalTime = this->timestamps_non_func[0] - this->timestamps_non_func[timestamps_non_func.size() - 1];

        //totalEnergy = totalEnergy / totalTime;
        //totalEnergy = totalEnergy * totalTime;
        return totalEnergy;
    }

    double Task::calculateTotalPower(const std::vector<double>& periodAverages) {
        // This is the power, so I have to calculate [Watt]
        double totalPower = 0.0;
        if (periodAverages.size() == 0) {
            return 0.0;
        } else if (periodAverages.size() == 1) {
            totalPower = periodAverages[0];
            return totalPower;
        }

        for (size_t i = 0; i < periodAverages.size(); i++) {
            totalPower += periodAverages[i];
        }

        return totalPower;
    }
}