// Task.hpp

#ifndef TASK_HPP
#define TASK_HPP

#include <algorithm>           // max
#include <cmath>               // floor
#include <cstddef>             // size_t
#include <cstdint>             // exit, EXIT_SUCCESS, EXIT_FAILURE
#include <cstdlib>             // atoi
#include <iomanip>             // setw, setprecision, setfill
#include <ios>                 // fixed
#include <iostream>            // cout
#include <ostream>             // endl
#include <sstream>             // ostringstream
#include <fstream>
#include <vector>

namespace satsim {
    class Task {
    public:
        Task(
                size_t duration, std::string app_data,
                std::vector<std::vector<double>> non_func_data,
                std::vector<std::vector<double>> payload_data,
                std::vector<size_t> timestamps_non_func,
                std::vector<size_t> timestamps_payload
        );
        Task(size_t duration);
        Task(const Task& nonFuncData) = default;
        Task(Task&& nonFuncData) = default;
        virtual ~Task() = default;
        virtual Task& operator=(const Task& nonFuncData) = default;
        virtual Task& operator=(Task&& nonFuncData) = default;
        virtual Task* clone() const;
        bool allValuesAddedOnTask();
        void setNonFuncData(const std::string& msg);
        void setPayloadData(const std::string& msg);
        void setDurationMilliseconds(const size_t& dur);
        void setAppData(const std::string& app);
        void setTimestampsNonFuncData(const std::string& msg);
        void setTimestampsPayloadData(const std::string& msg);
        std::vector<std::vector<double>> getNonFuncData();
        void printNonFuncData();
        std::vector<std::vector<double>> getPayloadData();
        void printPayloadData();
        size_t getDurationMilliseconds();
        double getDurationSeconds();
        std::string getAppData();
        std::vector<size_t> getTimestampsNonFuncData();
        void printTimestampNonFuncData();
        std::vector<size_t> getTimestampsPayloadData();
        void printTimestampPayloadData();
        std::vector<double> getVoltSolarPanelPlusX();
        std::vector<double> getAmpereSolarPanelPlusX();
        std::vector<double> getWattArraySolarPanelPlusX();
        void fillWattArraySolarPanelPlusX();
        double getWattSolarPanelPlusX();
        std::vector<double> getVoltSolarPanelMinusX();
        std::vector<double> getAmpereSolarPanelMinusX();
        std::vector<double> getWattArraySolarPanelMinusX();
        void fillWattArraySolarPanelMinusX();
        double getWattSolarPanelMinusX();
        std::vector<double> getVoltSolarPanelPlusY();
        std::vector<double> getAmpereSolarPanelPlusY();
        std::vector<double> getWattArraySolarPanelPlusY();
        void fillWattArraySolarPanelPlusY();
        double getWattSolarPanelPlusY();
        std::vector<double> getVoltSolarPanelMinusY();
        std::vector<double> getAmpereSolarPanelMinusY();
        std::vector<double> getWattArraySolarPanelMinusY();
        void fillWattArraySolarPanelMinusY();
        double getWattSolarPanelMinusY();
        std::vector<double> getVoltSolarPanelPlusZ();
        std::vector<double> getAmpereSolarPanelPlusZ();
        std::vector<double> getWattArraySolarPanelPlusZ();
        void fillWattArraySolarPanelPlusZ();
        double getWattSolarPanelPlusZ();
        std::vector<double> getVoltSolarPanelMinusZ();
        std::vector<double> getAmpereSolarPanelMinusZ();
        std::vector<double> getWattArraySolarPanelMinusZ();
        void fillWattArraySolarPanelMinusZ();
        double getWattSolarPanelMinusZ();
        std::vector<double> getVoltBattery();
        std::vector<double> getAmpereBattery();
        std::vector<double> getWattArrayBattery();
        void fillWattArrayBattery();
        double getWattBattery();
        std::vector<double> getVoltBus();
        std::vector<double> getAmpereBus();
        std::vector<double> getWattArrayBus();
        void fillWattArrayBus();
        double getWattBus();
        double getEnergyBus();
        //double getWattBusPositive();
        std::vector<double> getRSSI();
        std::vector<double> getIHUTemp();
        std::vector<double> getSPIN();
        std::vector<double> getTemperature();
        std::vector<double> getPressure();
        std::vector<double> getAltitude();
        std::vector<double> getHumidity();
        std::vector<double> getGyroX();
        std::vector<double> getGyroY();
        std::vector<double> getGyroZ();
        std::vector<double> getAccelX();
        std::vector<double> getAccelY();
        std::vector<double> getAccelZ();
        std::vector<double> getXS1();
        std::vector<double> getXS2();
        std::vector<double> getXS3();
        std::vector<std::vector<double>> doubleSplitTask(const std::string& msg, std::string outerDel, std::string innerDel);
        std::vector<size_t> innerSplitFirstValueTask(const std::string& msg, std::string outerDel, std::string innerDel);
        std::vector<double> calculatePeriodAverages(const std::vector<double>& watts);
        double calculateTotalEnergy(const std::vector<double>& periodAverages, const std::vector<size_t>& timestampRanges);
        double calculateTotalPower(const std::vector<double>& periodAverages);
        std::vector<size_t> calculateTimestampRanges(const std::vector<size_t>& timestamps);
    private:
        size_t duration;
        std::string app_data;
        std::vector<std::vector<double>> non_func_data;
        std::vector<std::vector<double>> payload_data;
        std::vector<size_t> timestamps_non_func;
        std::vector<size_t> timestamps_payload;
        std::vector<double> voltSolarPanelPlusX;
        std::vector<double> ampereSolarPanelPlusX;
        std::vector<double> wattArraySolarPanelPlusX;
        double wattSolarPanelPlusX;
        std::vector<double> voltSolarPanelMinusX;
        std::vector<double> ampereSolarPanelMinusX;
        std::vector<double> wattArraySolarPanelMinusX;
        double wattSolarPanelMinusX;
        std::vector<double> voltSolarPanelPlusY;
        std::vector<double> ampereSolarPanelPlusY;
        std::vector<double> wattArraySolarPanelPlusY;
        double wattSolarPanelPlusY;
        std::vector<double> voltSolarPanelMinusY;
        std::vector<double> ampereSolarPanelMinusY;
        std::vector<double> wattArraySolarPanelMinusY;
        double wattSolarPanelMinusY;
        std::vector<double> voltSolarPanelPlusZ;
        std::vector<double> ampereSolarPanelPlusZ;
        std::vector<double> wattArraySolarPanelPlusZ;
        double wattSolarPanelPlusZ;
        std::vector<double> voltSolarPanelMinusZ;
        std::vector<double> ampereSolarPanelMinusZ;
        std::vector<double> wattArraySolarPanelMinusZ;
        double wattSolarPanelMinusZ;
        std::vector<double> voltBattery;
        std::vector<double> ampereBattery;
        std::vector<double> wattArrayBattery;
        double wattBattery;
        std::vector<double> voltBus;
        std::vector<double> ampereBus;
        std::vector<double> wattArrayBus;
        double wattBus;
        double energyBus;
        std::vector<double> rssiVal;
        std::vector<double> ihuTemp;
        std::vector<double> spinVal;
        std::vector<double> temperaturePayload;
        std::vector<double> pressurePayload;
        std::vector<double> altitudePayload;
        std::vector<double> humidityPayload;
        std::vector<double> gyroX;
        std::vector<double> gyroY;
        std::vector<double> gyroZ;
        std::vector<double> accelX;
        std::vector<double> accelY;
        std::vector<double> accelZ;
        std::vector<double> xs1Val;
        std::vector<double> xs2Val;
        std::vector<double> xs3Val;
        int missingValueOfTask;
    };
}

#endif
