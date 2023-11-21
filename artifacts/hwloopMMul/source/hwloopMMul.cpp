// hwloopMMul.cpp
// Multithreading simulation

// Standard library
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
#include <fstream>             // fstream
#include <atomic>              // atomic
#include "mqtt/async_client.h"
#include <thread>
#include <unordered_map>
#include <mutex>
#include <condition_variable>

// satsim
#include <Capacitor.hpp>       // Capacitor
#include <EHSatellite.hpp>     // EHSatellite
#include <EHSystem.hpp>        // EHSystem
#include <EnergyConsumer.hpp>  // EnergyConsumer
#include <EnergyHarvester.hpp> // EnergyHarvester
#include <CubeSat.hpp>         // CubeSat
#include <Job.hpp>             // Job
#include <Logger.hpp>          // Logger
#include <Orbit.hpp>           // Orbit
#include <Satellite.hpp>       // Satellite
#include <SimpleSolarCell.hpp> // SimpleSolarCell
#include <Task.hpp>     // NonFuncData


std::vector<std::string> split(std::string s, std::string del);
size_t splitLength(std::string s, std::string del = ",");
size_t splitLengthMultiple(std::string s, std::string del = ",");
std::string splitGetFirst(std::string s, std::string del);
std::vector<std::vector<double>> doubleSplit(std::string s, std::string outerDel = ";", std::string innerDel = ",");
std::vector<size_t> innerSplitFirstValue(std::string s, std::string outerDel, std::string innerDel);
bool containsString(std::string s, std::string substring);
bool physicalSatellitesAreBusy();
satsim::Job* checkThatAtLeastAJobHasFinished(std::vector<satsim::Job*> jobsOccupied);
void simulationThread(size_t idEhSat, size_t orbitDuration, double energyHarvestMaximumVolt, double energyHarvestMaximumCurrent, double energyStorageCapacity, double energyStorageEsr, satsim::Logger* logger, size_t numberOfJobs, std::vector<satsim::Job*> jobs, bool multipleJobs, double timeStaticToUpdateTheSimulation);
void sendInstanceFreedPhysicalSatellite(int instance);
void sendInstanceCubeSatWorking(int instance);
void setUpPhysicalMap(int maxInstance);
void setUpCubeSatMap(int maxInstance);


std::string SERVER_ADDRESS;
std::string CLIENT_ID_PUB;
std::string CLIENT_ID_SUB;

std::string TOPIC_PUB;
std::string TOPIC_SUB;

char* PAYLOAD_EXECUTE;
const char* LWT_PAYLOAD = "Last will and testament.";

const int  QOS = 1;
const int	N_RETRY_ATTEMPTS = 5;
const auto TIMEOUT = std::chrono::seconds(10);

std::string TOPIC_APP_DATA;
std::string TOPIC_DURATION;
std::string TOPIC_NON_FUNC;
std::string TOPIC_PAYLOAD;

std::string ERROR_MESSAGE;

size_t DURATION_DATA = 0;
std::string APP_DATA = "";
std::vector<std::vector<double>> NON_FUNC_DATA;
std::vector<size_t> NON_FUNC_TIMESTAMPS;
std::vector<std::vector<double>> PAYLOAD_DATA;
std::vector<size_t> PAYLOAD_TIMESTAMPS;
size_t WAITING_DATA = 4;
std::string SATELLITE_NO_DATA;
bool RECEIVE_NO_DATA = false;
bool WAITING_CONNECTION = false;

std::unordered_map<std::string, satsim::Task*> tasksToFinish;
std::unordered_map<satsim::Job*, std::vector<std::string>> stringsPerJob;
std::unordered_map<satsim::Task*, satsim::Job*> tasksPerJob;
std::unordered_map<satsim::Job*, int> numberOfTasksPerJob;
std::unordered_map<satsim::Job*, int> physicalSatelliteUsed;
std::unordered_map<satsim::Job*, bool> jobHasFinishedWorking;

std::mutex taskMutex;
std::mutex unorderedMapsMutex;
std::mutex availableSatellitesMutex;
std::mutex concurrentAvailableSatellitesMutex;
std::mutex jobFinishedMutex;
std::mutex parameterMapsMutex;
std::mutex stringsPerJobMutex;
std::mutex waitForInstanceTurn;
std::mutex waitForInstanceTurnMap;
std::mutex multipleMessagesArrivedMutex;

std::vector<int> availablePhysicalSatellite;
std::vector<int> concurrentAccessToPhysicalSatellitesVector;

std::unordered_map<int, bool> instanceReceived;

std::condition_variable cv;
std::condition_variable cv2;

std::unordered_map<int, bool> instanceMapReceived;

static const std::mutex mutexLoggerEvent;

size_t print_value = 1000;
std::mutex printMutex;


class action_listener : public virtual mqtt::iaction_listener
{
    std::string name_;

    void on_failure(const mqtt::token& tok) override {
        std::cout << name_ << " failure";
        if (tok.get_message_id() != 0)
            std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
        std::cout << std::endl;
    }

    void on_success(const mqtt::token& tok) override {
        std::cout << name_ << " success";
        std::lock_guard<std::mutex> lockMultipleMessages(multipleMessagesArrivedMutex);
        if (tok.get_message_id() != 0)
            std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
        auto top = tok.get_topics();
        if (top && !top->empty())
            WAITING_CONNECTION = true;
        std::cout << "Token topic: '" << (*top)[0] << std::endl;
        std::cout << std::endl;
    }

public:
    action_listener(const std::string& name) : name_(name) {}
};

/////////////////////////////////////////////////////////////////////////////

/**
 * Local callback & listener class for use with the client connection.
 * This is primarily intended to receive messages, but it will also monitor
 * the connection to the broker. If the connection is lost, it will attempt
 * to restore the connection and re-subscribe to the topic.
 */
class callback : public virtual mqtt::callback,
                 public virtual mqtt::iaction_listener

{
    // Counter for the number of connection retries
    int nretry_;
    // The MQTT client
    mqtt::async_client& cli_;
    // Options to use if we need to reconnect
    mqtt::connect_options& connOpts_;
    // An action listener to display the result of actions.
    action_listener subListener_;
    // Physical satellite
    // int physicalSatellite;

    // This demonstrates manually reconnecting to the broker by calling
    // connect() again. This is a possibility for an application that keeps
    // a copy of its original connect_options, or if the app wants to
    // reconnect with different options.
    // Another way this can be done manually, if using the same options, is
    // to just call the async_client::reconnect() method.
    void reconnect() {
        std::this_thread::sleep_for(std::chrono::milliseconds(2500));
        try {
            cli_.connect(connOpts_, nullptr, *this);
        }
        catch (const mqtt::exception& exc) {
            std::cerr << "Sub client error: " << exc.what() << std::endl;
            exit(1);
        }
    }

    // Re-connection failure
    void on_failure(const mqtt::token& tok) override {
        std::cout << "Sub client connection attempt failed" << std::endl;
        if (++nretry_ > N_RETRY_ATTEMPTS)
            exit(1);
        reconnect();
    }

    // (Re)connection success
    // Either this or connected() can be used for callbacks.
    void on_success(const mqtt::token& tok) override {}

    // (Re)connection success
    void connected(const std::string& cause) override {
        std::cout << "\nSub client connection success" << std::endl;
        std::cout << "\nSubscribing to topic '" << TOPIC_SUB << "'"
                  << " for client '" << CLIENT_ID_SUB << "'"
                  << " using QoS '" << QOS << "'\n" << std::endl;
        //<< "\nPress Q<Enter> to quit\n" << std::endl;

        cli_.subscribe(TOPIC_SUB, QOS, nullptr, subListener_);
    }

    // Callback for when the connection is lost.
    // This will initiate the attempt to manually reconnect.
    void connection_lost(const std::string& cause) override {
        std::cout << "\nSub client connection lost" << std::endl;
        if (!cause.empty())
            std::cout << "\tcause: " << cause << std::endl;

        std::cout << "Sub client Reconnecting..." << std::endl;
        nretry_ = 0;
        reconnect();
    }

    // Callback for when a message arrives.
    void message_arrived(mqtt::const_message_ptr msg) override {
        const auto topicPubCopy = TOPIC_PUB;

        // Check if the message topic matches the expected publishing topic
        if (msg->get_topic().rfind(topicPubCopy, 0) != 0) {
            // Retrieve id of satellite from the topic
            std::vector<std::string> temp = split(msg->get_topic(), "/");
            // PhSat + Instance of Sat + Task
            std::string idOfSatWithTask = temp[2] + "/" + temp[3] + "/" + temp[4];

            const auto topicAppCopy = TOPIC_APP_DATA;
            const auto topicDurationCopy = TOPIC_DURATION;
            const auto topicNonFuncCopy = TOPIC_NON_FUNC;
            const auto topicPayloadCopy = TOPIC_PAYLOAD;

            const auto errorMessageCopy = ERROR_MESSAGE;

            satsim::Task* taskSelected = nullptr;
            satsim::Job* jobSelected = nullptr;

            // Retrieve the task and job associated with the received message
            if (taskSelected == nullptr && jobSelected == nullptr) {
                std::lock_guard<std::mutex> lockUnorderedMaps(unorderedMapsMutex);
                taskSelected = tasksToFinish[idOfSatWithTask];
                jobSelected = tasksPerJob[taskSelected];
            }

            bool addedAllTaskToJob = false;
            if (taskSelected != nullptr){
                // Handle different types of messages based on the message topic
                if ((msg->get_topic().rfind(topicAppCopy, 0) == 0)) {
                    // Handle application data message
                    if (true) {
                        std::lock_guard<std::mutex> lockTask(taskMutex);
                        std::string tempData = msg->to_string();
                        taskSelected->setAppData(tempData);
                        if (taskSelected->allValuesAddedOnTask()) {
                            addedAllTaskToJob = true;
                        }
                    }
                    if (addedAllTaskToJob) {
                        //add to map with job and string
                        std::lock_guard<std::mutex> lockStringsPerJob(stringsPerJobMutex);
                        stringsPerJob[jobSelected].push_back(idOfSatWithTask);
                    }
                    if (msg->to_string().rfind(errorMessageCopy, 0) == 0) {
                        jobSelected->logEvent(
                                "cubesat-"+std::to_string(jobSelected->getInstanceOfSatellite())+"-error-found",
                                jobSelected->getJobId()
                        );
                        std::cout << "!RADIATION ERROR FOUND!" << std::endl;
                    }
                } else if ((msg->get_topic().rfind(topicDurationCopy, 0) == 0)) {
                    // Handle duration message
                    if (true) {
                        std::lock_guard<std::mutex> lockTask(taskMutex);
                        size_t tempDur = std::stoi(msg->to_string());
                        taskSelected->setDurationMilliseconds(tempDur);
                        if (taskSelected->allValuesAddedOnTask()) {
                            addedAllTaskToJob = true;
                        }
                    }
                    if (addedAllTaskToJob) {
                        //add to map with job and string
                        std::lock_guard<std::mutex> lockStringsPerJob(stringsPerJobMutex);
                        stringsPerJob[jobSelected].push_back(idOfSatWithTask);
                    }
                } else if ((msg->get_topic().rfind(topicNonFuncCopy, 0) == 0)) {
                    // Handle non-functional data message
                    if (msg->to_string() != ""){
                        std::lock_guard<std::mutex> lockTask(taskMutex);
                        taskSelected->setNonFuncData(msg->to_string());
                        taskSelected->setTimestampsNonFuncData(msg->to_string());
                        if (taskSelected->allValuesAddedOnTask()) {
                            addedAllTaskToJob = true;
                        }
                    }
                    if (addedAllTaskToJob) {
                        //add to map with job and string
                        std::lock_guard<std::mutex> lockStringsPerJob(stringsPerJobMutex);
                        stringsPerJob[jobSelected].push_back(idOfSatWithTask);
                    }
                } else if ((msg->get_topic().rfind(topicPayloadCopy, 0) == 0)) {
                    // Handle payload data message
                    if (msg->to_string() != ""){
                        std::lock_guard<std::mutex> lockTask(taskMutex);
                        taskSelected->setPayloadData(msg->to_string());
                        taskSelected->setTimestampsPayloadData(msg->to_string());
                        if (taskSelected->allValuesAddedOnTask()) {
                            addedAllTaskToJob = true;
                        }
                    }
                    if (addedAllTaskToJob) {
                        //add to map with job and string
                        std::lock_guard<std::mutex> lockStringsPerJob(stringsPerJobMutex);
                        stringsPerJob[jobSelected].push_back(idOfSatWithTask);
                    }
                }

                // Reset task after processing
                taskSelected = NULL;

                bool checkString = true;
                bool checkValuesAdded = false;
                bool addedAllTasks = false;
                bool lockingMapJob = true;
                std::vector<std::string> tempVector;
                int numberOfTaskOfThisJob = 0;

                if (checkString) {
                    // Check if all the tasks have arrived
                    if (true) {
                        std::lock_guard<std::mutex> lockParameterMaps(parameterMapsMutex);
                        numberOfTaskOfThisJob = numberOfTasksPerJob[jobSelected];
                    }
                    checkString = false;
                    std::lock_guard<std::mutex> lockStringsPerJob(stringsPerJobMutex);
                    if (stringsPerJob[jobSelected].size() == numberOfTaskOfThisJob){
                        checkValuesAdded = true;
                        tempVector = stringsPerJob[jobSelected];
                    }
                }
                if (checkValuesAdded) {
                    // Add tasks to the job and mark it as finished
                    std::lock_guard<std::mutex> lockUnorderedMaps(unorderedMapsMutex);
                    std::string sitStr = "Finish job: " + std::to_string(jobSelected->getJobId()) + ", for instance of satellite: " + std::to_string(jobSelected->getInstanceOfSatellite());
                    std::cout << sitStr << std::endl;
                    for (int r = 0; r < tempVector.size(); r++){
                        jobSelected->addTaskValues(*tasksToFinish[tempVector[r]]);
                        addedAllTasks = true;
                    }
                    //std::cout << "Number of tasks added: " << jobSelected->getTasksValues().size() << ", for the job: " << jobSelected->getJobId() << std::endl;
                    checkValuesAdded = false;
                }

                if (addedAllTasks){
                    addedAllTasks = false;
                    if (lockingMapJob) {
                        // Proceed the execution since job has finished working
                        std::lock_guard<std::mutex> lockJobFinished(jobFinishedMutex);
                        jobHasFinishedWorking[jobSelected] = true;
                        lockingMapJob = false;
                    }

                    // Take physical satellite to free
                    int satellitesToAddAgain = 0;
                    if (true) {
                        std::lock_guard<std::mutex> lockParameterMaps(parameterMapsMutex);
                        satellitesToAddAgain = physicalSatelliteUsed[jobSelected];
                    }

                    // Free physical satellite
                    if (true) {
                        std::lock_guard<std::mutex> lockAvailableSatellites(availableSatellitesMutex);
                        auto it = std::lower_bound(availablePhysicalSatellite.begin(), availablePhysicalSatellite.end(), satellitesToAddAgain);
                        availablePhysicalSatellite.insert(it, satellitesToAddAgain);
                    }

                    // Let 1 instance of satellite waiting for a physical satellite to proceed
                    int tempValue = -1;
                    if (true) {
                        std::lock_guard<std::mutex> lockConcurrentAvailableSatellites(concurrentAvailableSatellitesMutex);
                        if (concurrentAccessToPhysicalSatellitesVector.size() > 0) {
                            tempValue = concurrentAccessToPhysicalSatellitesVector[0];
                            concurrentAccessToPhysicalSatellitesVector.erase(concurrentAccessToPhysicalSatellitesVector.begin());
                        }
                    }

                    // Continue with satellite waiting for tasks
                    sendInstanceCubeSatWorking(jobSelected->getInstanceOfSatellite());

                    // Continue with satellite waiting for physical satellite
                    sendInstanceFreedPhysicalSatellite(tempValue);
                }
                // Reset job after processing
                jobSelected = NULL;
            }
        }
    }

    void delivery_complete(mqtt::delivery_token_ptr token) override {}

public:
    callback(mqtt::async_client& cli, mqtt::connect_options& connOpts)
            : nretry_(0), cli_(cli), connOpts_(connOpts), subListener_("Subscription") {}
};

/////////////////////////////////////////////////////////////////////////////






int main(int argc, char** argv) {
    size_t print_value = 1000;
    size_t numberOfSatellites = 1;
    size_t numberOfJobs = 1;
    bool multipleJobs = false;
    std::string mapperFile = "";
    size_t phSat = 1;
    size_t publishPhSat = 1;
    double orbitDuration = 0.0;
    double energyHarvestMaximumVolt = 0.0;
    double energyHarvestMaximumCurrent = 0.0;
    double energyStorageCapacity = 0.0;
    double energyStorageEsr = 0.0;
    double timeStaticToUpdateTheSimulation = 0.0;
    // Parse command line argument(s)
    if(argc != 25) {
        std::cout << "Usage: ./" << argv[0] << " int int string string int string string string string string string string string string string string string double string double double double double"
                  << std::endl
                  << "1 - int: pipeline depth (minimum 1)"
                  << std::endl
                  << "2 - int: number of jobs per satellite"
                  << std::endl
                  << "3 - string: s for single job or m for multiple jobs"
                  << std::endl
                  << "4 - string: mapper file position"
                  << std::endl
                  << "5 - int: number of physical satellites"
                  << std::endl
                  << "6 - string: server MQTT"
                  << std::endl
                  << "7 - string: port MQTT"
                  << std::endl
                  << "8 - string: subscriber ID"
                  << std::endl
                  << "9 - string: publisher ID"
                  << std::endl
                  << "10 - string: generic topic to subscribe"
                  << std::endl
                  << "11 - string: topic for publish the commands"
                  << std::endl
                  << "12 - string: command to execute"
                  << std::endl
                  << "13 - string: topic to receive the applicative data"
                  << std::endl
                  << "14 - string: topic to receive the duration"
                  << std::endl
                  << "15 - string: topic to receive the non-functional data"
                  << std::endl
                  << "16 - string: topic to receive the payload"
                  << std::endl
                  << "17 - string: message received when there is no more jobs to execute"
                  << std::endl
                  << "18 - double: orbit duration"
                  << std::endl
                  << "19 - string: default error string"
                  << std::endl
                  << "20 - double: energy harvest maximum volt"
                  << std::endl
                  << "21 - double: energy harvest maximum current"
                  << std::endl
                  << "22 - double: energy storage capacity"
                  << std::endl
                  << "23 - double: energy storage esr"
                  << std::endl
                  << "24 - double: time to update the simulation"
                  << std::endl;

        std::exit(EXIT_FAILURE);
    } else {
        numberOfSatellites = std::max(1, std::stoi(argv[1]));
        numberOfJobs = std::max(1, std::stoi(argv[2]));
        if (std::string(argv[3]) == "m"){
            multipleJobs = true;
        }
        mapperFile = std::string(argv[4]);
        phSat = std::max(1, std::stoi(argv[5]));
        SERVER_ADDRESS = std::string(argv[6]) + ":" +  std::string(argv[7]);
        CLIENT_ID_SUB = std::string(argv[8]);
        CLIENT_ID_PUB = std::string(argv[9]);
        TOPIC_SUB = std::string(argv[10]);
        TOPIC_PUB = std::string(argv[11]);
        PAYLOAD_EXECUTE = argv[12];
        TOPIC_APP_DATA = std::string(argv[13]);
        TOPIC_DURATION = std::string(argv[14]);
        TOPIC_NON_FUNC = std::string(argv[15]);
        TOPIC_PAYLOAD = std::string(argv[16]);
        SATELLITE_NO_DATA = std::string(argv[17]);
        orbitDuration = std::atof(std::string(argv[18]).c_str());
        ERROR_MESSAGE = std::string(argv[19]);
        energyHarvestMaximumVolt = std::atof(std::string(argv[20]).c_str());
        energyHarvestMaximumCurrent = std::atof(std::string(argv[21]).c_str());
        energyStorageCapacity = std::atof(std::string(argv[22]).c_str());
        energyStorageEsr = std::atof(std::string(argv[23]).c_str());
        timeStaticToUpdateTheSimulation = std::atof(std::string(argv[24]).c_str());
    }

    // Set up logger
    satsim::Logger logger("s");

    // Read mapper file - Single job
    std::ifstream inputFile(mapperFile);
    std::vector<size_t> tasksCounter;

    std::vector<std::vector<size_t>> tasksCounterMultipleJobs;

    // Read from mapper file to retrieve tasks
    if (!multipleJobs) {
        if (inputFile.is_open()) {
            std::string line;
            while (std::getline(inputFile, line)) {
                tasksCounter.push_back(splitLength(line, ","));
            }
            inputFile.close();
        } else {
            std::cout << "Unable to open the file" << std::endl;
        }
    } else {
        if (inputFile.is_open()) {
            std::string line;
            int counterVector = 0;
            int oldCounter = 0;
            tasksCounter.clear();
            while (std::getline(inputFile, line)) {
                oldCounter = counterVector;
                counterVector = std::atoi(splitGetFirst(line, ",").c_str());
                if (counterVector != oldCounter) {
                    tasksCounterMultipleJobs.push_back(tasksCounter);
                    tasksCounter.clear();
                }
                tasksCounter.push_back(splitLengthMultiple(line, ","));
            }
            tasksCounterMultipleJobs.push_back(tasksCounter);
            tasksCounter.clear();
            inputFile.close();
        } else {
            std::cout << "Unable to open the file" << std::endl;
        }
    }

    for (int i = 1; i <= phSat; i++) {
        availablePhysicalSatellite.push_back(i);
    }

    // ASYNC SUBSCRIBE
    mqtt::async_client cli_sub(SERVER_ADDRESS, CLIENT_ID_SUB);

    mqtt::connect_options connOpts_sub;
    connOpts_sub.set_clean_session(false);

    // Install the callback(s) before connecting.
    callback cb_sub(cli_sub, connOpts_sub);
    cli_sub.set_callback(cb_sub);

    // Start the connection.
    // When completed, the callback will subscribe to topic.
    try {
        std::cout << "Sub client Connecting to the MQTT server...\n" << std::flush;
        cli_sub.connect(connOpts_sub, nullptr, cb_sub);
    }
    catch (const mqtt::exception& exc) {
        std::cerr << "\nSub client ERROR: Unable to connect to MQTT server: '"
                  << SERVER_ADDRESS << "'" << exc << std::endl;
        return 1;
    }

    std::cout << "Waiting for subscriber connection..." << std::endl;
    while (!WAITING_CONNECTION);

    // Set up jobs
    std::vector<std::vector<satsim::Job*>> jobsPerSat;
    for(size_t i = 0; i < numberOfSatellites; i++) {
        std::vector<satsim::Job*> temp;
        for(size_t j = 0; j < numberOfJobs; j++) {
            if (!multipleJobs){
                // Jobs array is divided in the following way -> [all jobs instance 1, all jobs instance 2, ...]
                temp.push_back(new satsim::Job(j,tasksCounter[i], i, &logger));
            } else {
                // Jobs array is divided in the following way -> [all jobs instance 1, all jobs instance 2, ...]
                temp.push_back(new satsim::Job(j,tasksCounterMultipleJobs[std::floor(i / numberOfJobs)][i % numberOfJobs], i, &logger));
            }
        }
        jobsPerSat.push_back(temp);
        temp.clear();
    }



    std::vector<std::thread> threads;

    setUpCubeSatMap(numberOfSatellites);
    setUpPhysicalMap(numberOfSatellites);

    // Create and start multiple threads
    for (int i = 0; i < numberOfSatellites; ++i) {
        threads.push_back(std::thread(simulationThread, i, orbitDuration, energyHarvestMaximumVolt, energyHarvestMaximumCurrent, energyStorageCapacity, energyStorageEsr, &logger, numberOfJobs, jobsPerSat[i], multipleJobs, timeStaticToUpdateTheSimulation));
    }

    // Wait for all threads to finish
    for (auto& thread : threads) {
        thread.join();
    }

    //Disconnecting subscriber
    std::cout << "\nDisconnecting subscriber... " << std::endl;
    cli_sub.disconnect()->wait();
    std::cout << "...Disconnected" << std::endl;

    // Write out logs
    std::ostringstream oss;
    std::cout << "Writing logs" << std::endl;
    oss << "../logs/" << std::setfill('0') << std::setw(3)
        << std::atoi(argv[1]);
    logger.exportCsvs(oss.str());

    std::cout << "Logs written" << std::endl;
    // Clean up jobs
    for(size_t i = 0; i < jobsPerSat.size(); i++) {
        for(size_t j = 0; j < jobsPerSat.at(i).size(); j++) {
            delete jobsPerSat.at(i).at(j);
            jobsPerSat.at(i).at(j) = nullptr;
        }
        jobsPerSat.at(i).clear();
    }
    jobsPerSat.clear();

    tasksPerJob.clear();
    tasksToFinish.clear();
    stringsPerJob.clear();
    numberOfTasksPerJob.clear();
    physicalSatelliteUsed.clear();
    jobHasFinishedWorking.clear();

    std::exit(EXIT_SUCCESS);
}



std::vector<std::string> split(std::string s, std::string del)
{
    int start, end = -1*del.size();
    size_t total = 0;
    std::vector<std::string> results;
    do {
        start = end + del.size();
        end = s.find(del, start);
        results.push_back(s.substr(start, end - start));
    } while (end != -1);
    return results;
}

size_t splitLength(std::string s, std::string del)
{
    int start, end = -1*del.size();
    size_t total = 0;
    do {
        start = end + del.size();
        end = s.find(del, start);
        total++;
    } while (end != -1);
    return total - 1;
}

size_t splitLengthMultiple(std::string s, std::string del)
{
    int start, end = -1*del.size();
    size_t total = 0;
    do {
        start = end + del.size();
        end = s.find(del, start);
        total++;
    } while (end != -1);
    return total - 2;
}

std::string splitGetFirst(std::string s, std::string del)
{
    int start, end = -1*del.size();
    start = end + del.size();
    end = s.find(del, start);
    return s.substr(start, end - start);
}

std::vector<std::vector<double>> doubleSplit(std::string s, std::string outerDel, std::string innerDel)
{
    int start, end = -1*outerDel.size();
    bool firstVal = true;
    std::vector<std::vector<double>> finalResult;
    std::vector<double> tempResults;
    std::vector<std::string> intermediateResults;
    do {
        start = end + outerDel.size();
        end = s.find(outerDel, start);
        intermediateResults.push_back(s.substr(start, end - start));
    } while (end != -1);
    for (int k = 0; k < intermediateResults.size(); k++) {
        end = -1*innerDel.size();
        do {
            start = end + innerDel.size();
            end = intermediateResults[k].find(innerDel, start);
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

std::vector<size_t> innerSplitFirstValue(std::string s, std::string outerDel, std::string innerDel)
{
    int start, end = -1*outerDel.size();
    std::vector<size_t> finalResult;
    std::vector<std::string> intermediateResults;
    size_t temp;
    do {
        start = end + outerDel.size();
        end = s.find(outerDel, start);
        intermediateResults.push_back(s.substr(start, end - start));
    } while (end != -1);
    for (int k = 0; k < intermediateResults.size(); k++) {
        end = -1*innerDel.size();
        start = end + innerDel.size();
        end = intermediateResults[k].find(innerDel, start);
        std::stringstream stream(intermediateResults[k].substr(start, end - start));
        stream >> temp;
        finalResult.push_back(temp);
        temp = 0;
    }
    return finalResult;
}

bool containsString(std::string s, std::string substring)
{
    return s.rfind(substring, 0) == 0;
}

bool physicalSatellitesAreBusy() {
    const std::vector<int>& constAvailablePhysicalSatellite = availablePhysicalSatellite;
    return constAvailablePhysicalSatellite.empty();
}

satsim::Job* checkThatAtLeastAJobHasFinished(std::vector<satsim::Job*> jobsOccupied){
    for (satsim::Job* job: jobsOccupied) {
        if (job != nullptr) {
            if (job->getAllTasksArrived()) {
                return job;
            }
        }
    }
    return nullptr;
}


void simulationThread(size_t idEhSat, size_t orbitDuration, double energyHarvestMaximumVolt, double energyHarvestMaximumCurrent, double energyStorageCapacity, double energyStorageEsr, satsim::Logger* logger, size_t numberOfJobs, std::vector<satsim::Job*> jobs, bool multipleJobs, double timeStaticToUpdateTheSimulation) {
    bool multipleJobsInner = multipleJobs;
    size_t publishPhSat = 1;

    // PUBLISH
    std::string address_pub = SERVER_ADDRESS;

    std::string pubString = "Pub client initializing for server '" + address_pub + "'...";
    std::cout << pubString << std::endl;
    mqtt::async_client cli_pub(address_pub, CLIENT_ID_PUB + std::to_string(idEhSat));

    try {
        std::cout << "\nPub client Connecting..." << std::endl;
        cli_pub.connect()->wait();
    }
    catch (const mqtt::exception& exc) {
        std::cerr << exc << std::endl;
        return;
    }

    // Orbit: 400 km altitude polar orbit (93 min period = 5580.0 sec)
    // For CSFP, all satellites are at the same radial position (0.0)
    satsim::Orbit orbit(orbitDuration, 0.0);

    // Energy harvester
    // Azur Space 3G30A 2.5E14; three in series of two cells in parallel (6 ct.)
    double sscVmp_V = energyHarvestMaximumVolt; //7.0290;
    double sscCmp_A = energyHarvestMaximumCurrent; //1.0034;
    double nodeVoltage_V = sscVmp_V; // Start at maximum node voltage
    //satsim::EnergyHarvester* simpleSolarCell = new satsim::SimpleSolarCell(sscVmp_V, sscCmp_A, nodeVoltage_V, &logger);
    satsim::EnergyHarvester* simpleSolarCell = new satsim::SimpleSolarCell(sscVmp_V, sscCmp_A, nodeVoltage_V, logger);
    simpleSolarCell->setWorkerId(idEhSat);

    // Energy storage
    // AVX SuperCapacitor SCMR22L105M; five in parallel
    // Cap_V: nodeVoltage_V - sscCmp_A * esr_Ohm is max valid voltage for this model
    // Assuming sim starts with this Cap_V, charge is Cap_V * capacity_F
    double capacity_F = energyStorageCapacity; //5.0;
    double esr_Ohm    = energyStorageEsr; //0.168;
    double charge_C = (nodeVoltage_V - sscCmp_A * esr_Ohm) * capacity_F;
    satsim::Capacitor capacitor(capacity_F,esr_Ohm,charge_C,sscCmp_A,logger);

    // Minimal energy harvesting system
    satsim::EHSystem ehsystem(*simpleSolarCell, capacitor, logger);

    // Clean up energy harvester
    delete simpleSolarCell;

    satsim::CubeSat cubesat(
            nodeVoltage_V, satsim::CubeSat::PowerState::IDLE, logger
    );
    cubesat.setWorkerId(idEhSat);
    cubesat.logEvent(
            "cubesat-"+std::to_string(cubesat.getWorkerId())+"-idle-start",0.0
    );
    ehsystem.addEnergyConsumer(cubesat);

    // Push back new energy harvesting satellite
    satsim::EHSatellite* ehSatellite = new satsim::EHSatellite(orbit, ehsystem, logger);

    // Run simulation
    const double PI = satsim::Orbit::TAU/2.0;

    // Simulate the amount of radians into which a job could be found
    const double radPerJob = PI/numberOfJobs;

    bool simulate = true;
    double timeToUpdateTheSimulation;
    while(simulate) {
        // Prove that the simulation should still run
        simulate = false;

        // Run simulation of this satellite
        double ehsPosn = ehSatellite->getOrbit().getPosn();
        size_t remainingTasks;
        bool waitedForPhSat = false;
        bool enterWaiting = false;

        // if posn < PI check to see if new jobs are added (so look only before PI of the orbit)
        if(ehsPosn < PI) {
            simulate = true;
            std::vector<satsim::EnergyConsumer*> ecs = ehSatellite->getEnergyConsumers();
            satsim::CubeSat* cubePtr = dynamic_cast<satsim::CubeSat*>(ecs.at(0));

            // Here we take the job available at the radiant position in which the satellite is
            satsim::Job* jobPtr = jobs.at(std::floor(ehsPosn/radPerJob));

            // In this point I claim all the tasks of the job at the orbital position in which the current satellite is.
            // In this way, the next satellite that will reach this position, will not have the job available.
            // I claim the job only if some tasks are available and if the Jetson is not currently working
            if(jobPtr->getUnclaimedTaskCount() > 0 && cubePtr->getClaimedJobCount() == 0 && !jobPtr->isAcquired()) {

                cubePtr->logEvent(
                        "cubesat-"+std::to_string(cubePtr->getWorkerId())+"-found-job",
                        ehsPosn
                );

                // Acquiring job
                jobPtr->acquiringJob();

                // Save value to later loop to wait the end of all tasks
                remainingTasks = jobPtr->getUnclaimedTaskCount();

                // For CSFP, all tasks are claimed
                jobPtr->claimTasks(cubePtr->getWorkerId(), (jobPtr->getUnclaimedTaskCount()));

                // Send command to execute the job to the satellite and wait all response of the tasks.
                // Once the requested tasks have arrived, proceed with the simulation
                try {
                    if (true) {
                        std::lock_guard<std::mutex> lockAvailableSatellites(availableSatellitesMutex);
                        if (physicalSatellitesAreBusy()) {
                            enterWaiting = true;
                        }
                    }

                    // Start waiting for a physical satellite
                    if (enterWaiting) {
                        waitedForPhSat = true;

                        if (waitedForPhSat) {
                            std::lock_guard<std::mutex> lockConcurrentAvailableSatellites(concurrentAvailableSatellitesMutex);
                            concurrentAccessToPhysicalSatellitesVector.push_back(idEhSat);
                        }

                        std::string beforeRecStr = "WAITING A PHYSICAL SATELLITE FOR SAT: " + std::to_string(idEhSat);
                        std::cout << beforeRecStr << std::endl;

                        std::unique_lock<std::mutex> lock(waitForInstanceTurn);
                        if (!instanceReceived[idEhSat]) {
                            cv.wait(lock, [&idEhSat] { return instanceReceived[idEhSat]; });
                        }
                        instanceReceived[idEhSat] = false;
                        lock.unlock();

                        std::string afterRecStr = "PHYSICAL SATELLITE RECEIVED FOR SAT: " + std::to_string(idEhSat);
                        std::cout << afterRecStr << std::endl;
                    }

                    // Take the number of physical satellite for which i could publish
                    if (true) {
                        std::lock_guard<std::mutex> lockAvailableSatellites(availableSatellitesMutex);
                        publishPhSat = availablePhysicalSatellite[0];
                        availablePhysicalSatellite.erase(availablePhysicalSatellite.begin());
                    }

                    int counter = 1;
                    bool finishAddingTasks = false;
                    bool startAddingTasks = false;
                    bool startAddingParamsToMaps = true;

                    // Save the job, to later access it
                    if (startAddingParamsToMaps) {
                        startAddingParamsToMaps = false;
                        startAddingTasks = true;
                        std::lock_guard<std::mutex> lockParameterMaps(parameterMapsMutex);
                        numberOfTasksPerJob[jobPtr] = remainingTasks;
                        physicalSatelliteUsed[jobPtr] = publishPhSat;
                    }

                    // Add empty tasks to satellite
                    if (startAddingTasks) {
                        startAddingTasks = false;
                        std::lock_guard<std::mutex> lockUnorderedMaps(unorderedMapsMutex);
                        while(remainingTasks != 0) {
                            std::string savedString = std::to_string(publishPhSat) + "/" + std::to_string(idEhSat) + "/" + std::to_string(counter);
                            tasksToFinish[savedString] = new satsim::Task(0);

                            tasksPerJob[tasksToFinish[savedString]] = jobPtr;
                            remainingTasks--;
                            counter++;
                        }
                        finishAddingTasks = true;
                    }

                    // To understand when a satellite has end
                    if (finishAddingTasks) {
                        std::lock_guard<std::mutex> lockJobFinished(jobFinishedMutex);
                        jobHasFinishedWorking[jobPtr] = false;
                        finishAddingTasks = false;
                    }

                    // Needs to be added a check on when to proceed with the working phase (stop until the whole job is arrived)
                    cubePtr->addClaimedJob(jobPtr);

                    if (!multipleJobsInner) {
                        // For multiple jobs, we send to MQTT the instance of satellite we want to execute and the job we want to execute
                        mqtt::topic top_pub(cli_pub, TOPIC_PUB + std::to_string(publishPhSat) + "/" + std::to_string(idEhSat), QOS);
                        mqtt::token_ptr tok_pub;

                        tok_pub = top_pub.publish(PAYLOAD_EXECUTE);
                        tok_pub->wait();
                    } else {
                        // For single job, we send to MQTT the instance of satellite we want to execute
                        mqtt::topic top_pub(cli_pub, TOPIC_PUB + std::to_string(publishPhSat) + "/" + std::to_string(idEhSat) + "/" + std::to_string(jobPtr->getJobId()), QOS);
                        mqtt::token_ptr tok_pub;

                        tok_pub = top_pub.publish(PAYLOAD_EXECUTE);
                        tok_pub->wait();
                    }
                }
                catch (const mqtt::exception& exc) {
                    std::cerr << exc << std::endl;
                    return;
                }
            }

            if (cubePtr->isWorking()) {
                // If I'm working, I want to proceed the simulation by the duration of a task
                satsim::Job* jobToWorkWith = cubePtr->getFirstClaimedJob();
                bool waitingForValues = false;

                if (true) {
                    std::lock_guard<std::mutex> lockJobFinished(jobFinishedMutex);
                    if (!jobHasFinishedWorking[jobToWorkWith]){
                        std::string waitTaskValStr = "WAITING THE TASKS TO ARRIVE FOR SAT: " + std::to_string(idEhSat);
                        std::cout << waitTaskValStr << std::endl;
                        waitingForValues = true;
                    }
                }

                // If I don't have the task values but I have reached this point, I need to wait for the tasks to arrive
                if (waitingForValues) {
                    std::unique_lock<std::mutex> lock(waitForInstanceTurnMap);

                    if (!instanceMapReceived[idEhSat]) {
                        cv2.wait(lock, [&idEhSat] {
                            return instanceMapReceived[idEhSat];
                        });
                    }
                    instanceMapReceived[idEhSat] = false;
                    lock.unlock();

                    std::string taskArrivedStr = "TASKS ARRIVED FOR SAT: " + std::to_string(idEhSat);
                    std::cout << taskArrivedStr << std::endl;
                }

                satsim::Task taskOfWorkingJob = jobToWorkWith->getTaskToExecute(jobToWorkWith->getTotalTasks(cubePtr->getWorkerId()));

                timeToUpdateTheSimulation = taskOfWorkingJob.getDurationSeconds();

                jobToWorkWith = nullptr;
            } else {
                if (idEhSat == 1){
                    if (print_value <= 0) {
                        print_value = 1000000;
                        std::string print_check = "POSITION IN THE ORBIT " + std::to_string(ehsPosn) + ", TRYING TO ACCESS THE JOB " + std::to_string(ehsPosn/radPerJob) + ".";
                        std::cout << print_check << std::endl;
                    }
                    print_value--;
                }
                // Otherwise proceed the simulation
                timeToUpdateTheSimulation = timeStaticToUpdateTheSimulation;
            }

            // Clean up
            cubePtr  = nullptr;
            jobPtr = nullptr;

            for(size_t j = 0; j < ecs.size(); j++) {
                ecs.at(j) = nullptr;
            }
            ecs.clear();
            // Update
            ehSatellite->update(timeToUpdateTheSimulation);
        }
            // otherwise, continue updating if CubeSat is not idle
        else {
            std::vector<satsim::EnergyConsumer*> ecs = ehSatellite->getEnergyConsumers();
            satsim::CubeSat* cubePtr = dynamic_cast<satsim::CubeSat*>(ecs.at(0));

            // Update
            if(!cubePtr->isIdle()) {
                simulate = true;
                if (cubePtr->isWorking()) {
                    // If I'm working, I want to proceed the simulation by the duration of a task
                    satsim::Job* jobToWorkWith = cubePtr->getFirstClaimedJob();
                    bool waitingForValues = false;

                    if (true) {
                        std::lock_guard<std::mutex> lockJobFinished(jobFinishedMutex);
                        if (!jobHasFinishedWorking[jobToWorkWith]){
                            std::string waitTaskValStr2 = "WAITING THE TASKS TO ARRIVE FOR SAT: " + std::to_string(idEhSat);
                            std::cout << waitTaskValStr2 << std::endl;
                            waitingForValues = true;
                        }
                    }

                    // If I don't have the task values but I have reached this point, I need to wait for the tasks to arrive
                    if (waitingForValues) {
                        // Two cv2 brings to a condition race
                        while (true) {
                            std::this_thread::sleep_for(std::chrono::milliseconds(100));
                            std::lock_guard<std::mutex> lockJobFinished(jobFinishedMutex);
                            if (!jobHasFinishedWorking[jobToWorkWith]) {
                                break;
                            }
                        }
                    }

                    satsim::Task taskOfWorkingJob = jobToWorkWith->getTaskToExecute(jobToWorkWith->getTotalTasks(cubePtr->getWorkerId()));
                    timeToUpdateTheSimulation = taskOfWorkingJob.getDurationSeconds();

                    jobToWorkWith = nullptr;
                } else {
                    // Otherwise proceed the simulation
                    timeToUpdateTheSimulation = timeStaticToUpdateTheSimulation;
                }

                // Update
                ehSatellite->update(timeToUpdateTheSimulation);
            }

            // Clean up
            cubePtr  = nullptr;

            for(size_t j = 0; j < ecs.size(); j++) {
                ecs.at(j) = nullptr;
            }
            ecs.clear();
        }

    }
    // Simulation is over, all Cubesats are in idle mode
    std::vector<satsim::EnergyConsumer*> ecs = ehSatellite->getEnergyConsumers();
    satsim::CubeSat* cubePtr = dynamic_cast<satsim::CubeSat*>(ecs.at(0));
    cubePtr->logEvent(
            "cubesat-"+std::to_string(cubePtr->getWorkerId())+"-idle-stop",
            cubePtr->getSimTime()
    );


    //delete cubePtr;
    //cubePtr->cleanClaimedJobs();
    //cubePtr->cleanCompletedJobs();
    cubePtr  = nullptr;
    for(size_t j = 0; j < ecs.size(); j++) {
        //delete ecs.at(j);
        ecs.at(j) = nullptr;
    }
    ecs.clear();

    std::string endSimStr = "SATELLITE ENDING THE SIMULATION: " + std::to_string(idEhSat);
    std::cout << endSimStr << std::endl;

    /*if (true) {
        std::lock_guard<std::mutex> lock(waitForInstanceTurnMap);

        std::string satWaitingForTasksStr = "SATELLITES WAITING FOR TASKS: \n";
        for(int j = 0; j < 6; j++){
            std::string s = "- SAT: " + std::to_string(j) + " -> " + std::to_string(instanceMapReceived[j]) + "\n";
            satWaitingForTasksStr = satWaitingForTasksStr + s;
        }
        std::cout << satWaitingForTasksStr << std::endl;
    }*/

    // Disconnect publisher
    std::cout << "Disconnecting publisher..." << std::endl;
    cli_pub.disconnect()->wait();
    std::cout << "  ...Disconnected" << std::endl;

    if (ehSatellite != nullptr) {
        delete ehSatellite;
        ehSatellite = nullptr;
    }
}

void sendInstanceFreedPhysicalSatellite(int instance) {
    std::lock_guard<std::mutex> lock(waitForInstanceTurn);
    instanceReceived[instance] = true;

    // Notify the waiting threads
    cv.notify_all();
}

void setUpPhysicalMap(int maxInstance) {
    std::lock_guard<std::mutex> lock(waitForInstanceTurn);
    for (int i = 0; i < maxInstance; i++){
        instanceReceived[i] = false;
    }
}

void sendInstanceCubeSatWorking(int instance) {
    std::lock_guard<std::mutex> lock(waitForInstanceTurnMap);
    instanceMapReceived[instance] = true;

    // Notify the waiting threads
    cv2.notify_all();
}

void setUpCubeSatMap(int maxInstance) {
    std::lock_guard<std::mutex> lock(waitForInstanceTurnMap);
    for (int i = 0; i < maxInstance; i++){
        instanceMapReceived[i] = false;
    }
}