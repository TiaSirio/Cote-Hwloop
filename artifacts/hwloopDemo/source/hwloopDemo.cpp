// hwloopDAG.cpp

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
size_t doubleSplitLength(std::string s, std::string outerDel, std::string innerDel);
std::vector<std::vector<double>> doubleSplit(std::string s, std::string outerDel = ";", std::string innerDel = ",");
std::vector<size_t> innerSplitFirstValue(std::string s, std::string outerDel, std::string innerDel);
bool containsString(std::string s, std::string substring);
bool physicalSatellitesAreBusy(size_t phSat);



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
size_t satelliteUsed = 1;
std::unordered_map<int, satsim::Task*> taskMap;



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

    // This deomonstrates manually reconnecting to the broker by calling
    // connect() again. This is a possibility for an application that keeps
    // a copy of it's original connect_options, or if the app wants to
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
        //std::cout << "Message arrived" << std::endl;
        //std::cout << "\ttopic: '" << msg->get_topic() << "'" << std::endl;
        //std::cout << "\tpayload: '" << msg->to_string() << "'\n" << std::endl;
        //std::cout << msg->to_string() << std::endl;
        if (containsString(msg->get_topic(),TOPIC_APP_DATA)) {
            APP_DATA = msg->to_string();
            WAITING_DATA--;
        } else if (containsString(msg->get_topic(),TOPIC_DURATION)) {
            DURATION_DATA = std::stoi(msg->to_string());
            WAITING_DATA--;
        } else if (containsString(msg->get_topic(),TOPIC_NON_FUNC)) {
            if (msg->to_string() != ""){
                NON_FUNC_DATA = doubleSplit(msg->to_string(), ";", ",");
                NON_FUNC_TIMESTAMPS = innerSplitFirstValue(msg->to_string(), ";", ",");
            }
            WAITING_DATA--;
        } else if (containsString(msg->get_topic(),TOPIC_PAYLOAD)) {
            if (msg->to_string() != ""){
                PAYLOAD_DATA = doubleSplit(msg->to_string(), ";", ",");
                PAYLOAD_TIMESTAMPS = innerSplitFirstValue(msg->to_string(), ";", ",");
            }
            WAITING_DATA--;
        }
        /*if (!containsString(msg->get_topic(),TOPIC_PUB) && msg->to_string() != SATELLITE_NO_DATA) {

        } else if (msg->to_string() == SATELLITE_NO_DATA){
            RECEIVE_NO_DATA = true;
            //std::cout << "RECEIVED NO DATA!" << std::endl;
        }*/
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
                  << "22 - double: energy storage maximum capacity"
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

    //std::cout << "Size: " << PAYLOAD_EXECUTE << std::endl;

    //size_t satellitesBusy = 0;

    // Set up logger
    satsim::Logger logger("s");

    // Read mapper file - Single job
    std::ifstream inputFile(mapperFile);
    std::vector<size_t> tasksCounter;

    std::vector<std::vector<size_t>> tasksCounterMultipleJobs;

    if (!multipleJobs) {
        if (inputFile.is_open()) {
            std::string line;
            while (std::getline(inputFile, line)) {
                tasksCounter.push_back(splitLength(line, ","));
                //std::cout << line << std::endl;
            }
            inputFile.close();
        } else {
            std::cout << "Unable to open the file" << std::endl;
        }
        /*
        for (size_t i = 0; i < tasksCounter.size(); ++i) {
          std::cout << tasksCounter[i] << " ";
        }
        std::cout << std::endl;
        */
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
        /*
        for(int i=0;i<tasksCounterMultipleJobs.size();i++){
            for(int j=0;j<tasksCounterMultipleJobs[i].size();j++)
                std::cout<<tasksCounterMultipleJobs[i][j]<<" ";
            std::cout<<std::endl;
        }
        */
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

    std::cout << "Waiting for subscriber connection...\n" << std::endl;
    while (!WAITING_CONNECTION);

    // PUBLISH
    std::string address_pub = SERVER_ADDRESS;

    std::cout << "Pub client initializing for server '" << address_pub << "'..." << std::endl;
    mqtt::async_client cli_pub(address_pub, CLIENT_ID_PUB);

    //std::cout << "  ...OK" << std::endl;

    try {
        std::cout << "\nPub client Connecting..." << std::endl;
        cli_pub.connect()->wait();
    }
    catch (const mqtt::exception& exc) {
        std::cerr << exc << std::endl;
        return 1;
    }




    // Set up jobs
    //size_t gtfCount = 1642;
    //std::vector<satsim::Job*> gtfs;
    std::vector<satsim::Job*> jobs;
    for(size_t i = 0; i < numberOfJobs * numberOfSatellites; i++) {
        if (!multipleJobs){
            // Jobs array is divided in the following way -> [all jobs instance 1, all jobs instance 2, ...]
            jobs.push_back(new satsim::Job(i % numberOfJobs,tasksCounter[std::floor(i / numberOfJobs)], std::floor(i / numberOfJobs)));
        } else {
            // Jobs array is divided in the following way -> [all jobs instance 1, all jobs instance 2, ...]
            jobs.push_back(new satsim::Job(i % numberOfJobs,tasksCounterMultipleJobs[std::floor(i / numberOfJobs)][i % numberOfJobs], std::floor(i / numberOfJobs)));
        }
    }


    /*
    for (size_t i = 0; i < jobs.size(); ++i) {
        std::cout << jobs[i]->getUnclaimedTaskCount() << " " << std::endl;
    }
    */

    // Build each satellite in the pipeline
    std::vector<satsim::EHSatellite*> ehsatellites;
    for(size_t i = 0; i < numberOfSatellites; i++) {

        // Orbit: 400 km altitude polar orbit (93 min period = 5580.0 sec)
        // For CSFP, all satellites are at the same radial position (0.0)
        satsim::Orbit orbit(orbitDuration, 0.0);

        // Energy harvester
        // Azur Space 3G30A 2.5E14; three in series of two cells in parallel (6 ct.)
        double sscVmp_V = energyHarvestMaximumVolt; //7.0290;
        double sscCmp_A = energyHarvestMaximumCurrent; //1.0034;
        double nodeVoltage_V = sscVmp_V; // Start at maximum node voltage
        satsim::EnergyHarvester* simpleSolarCell = new satsim::SimpleSolarCell(sscVmp_V, sscCmp_A, nodeVoltage_V, &logger);
        simpleSolarCell->setWorkerId(i);

        // Energy storage
        // AVX SuperCapacitor SCMR22L105M; five in parallel
        // Cap_V: nodeVoltage_V - sscCmp_A * esr_Ohm is max valid voltage for this model
        // Assuming sim starts with this Cap_V, charge is Cap_V * capacity_F
        double capacity_F = energyStorageCapacity; //5.0;
        double esr_Ohm    = energyStorageEsr; //0.168;
        double charge_C = (nodeVoltage_V - sscCmp_A * esr_Ohm) * capacity_F;
        satsim::Capacitor capacitor(capacity_F,esr_Ohm,charge_C,sscCmp_A,&logger);

        // Minimal energy harvesting system
        satsim::EHSystem ehsystem(*simpleSolarCell, capacitor, &logger);

        // Clean up energy harvester
        delete simpleSolarCell;

        /*
        // Energy consumer: Jetson TX2
        satsim::JetsonTX2 jetsonTX2(
                nodeVoltage_V, satsim::JetsonTX2::PowerState::IDLE, &logger
        );
        jetsonTX2.setWorkerId(i);
        jetsonTX2.logEvent(
                "jetson-"+std::to_string(jetsonTX2.getWorkerId())+"-idle-start",0.0
        );
         */
        // Energy consumer: Jetson TX2

        satsim::CubeSat cubesat(
                nodeVoltage_V, satsim::CubeSat::PowerState::IDLE, &logger
        );
        cubesat.setWorkerId(i);
        cubesat.logEvent(
                "cubesat-"+std::to_string(cubesat.getWorkerId())+"-idle-start",0.0
        );
        ehsystem.addEnergyConsumer(cubesat);


        // Energy consumer: Chameleon imager
        /*satsim::ChameleonImager chameleonImager(
                nodeVoltage_V, satsim::ChameleonImager::PowerState::IDLE, &logger
        );
        chameleonImager.setWorkerId(i);
        //chameleonImager.logEvent(
        // "chamgr-"+std::to_string(chameleonImager.getWorkerId())+"-idle-start",0.0
        //);
        ehsystem.addEnergyConsumer(chameleonImager);*/

        // Energy consumer: MAI ADACS
        /*satsim::MAIAdacs maiadacs(
                nodeVoltage_V, satsim::MAIAdacs::PowerState::NADIR, &logger
        );
        ehsystem.addEnergyConsumer(maiadacs);*/


        // Push back new energy harvesting satellite
        ehsatellites.push_back(new satsim::EHSatellite(orbit, ehsystem, &logger));
    }
    // Run simulation
    const double PI = satsim::Orbit::TAU/2.0;

    // Simulate the amount of radians into which a job could be found
    //const double radPerGtf = PI/jobs.size();

    // Simulate the amount of radians into which a job could be found
    const double radPerJob = PI/numberOfJobs;

    // To be implemented if we want to have a different amount of job per satellite
    //std::vector<double> radPerJob;


    //const double STEP = 0.00314159265358979323846;
    //double thresh     = 0.00314159265358979323846;
    //double percent    = 0.0;
    bool simulate = true;
    double timeToUpdateTheSimulation;
    size_t tasksBackup;
    //double simulationTime = 1;
    //std::string temp = "";
    while(simulate) {
        // Prove that the simulation should still run
        simulate = false;

        // Run simulation for each satellite
        for(size_t i = 0; i < ehsatellites.size(); i++) {
            satsim::EHSatellite* ehsPtr = ehsatellites.at(i);
            double ehsPosn = ehsPtr->getOrbit().getPosn();
            size_t remainingTasks;
            //std::cout << "ENTERING HERE FOR SATELLITE " << std::to_string(i) << std::endl;
            // if posn < PI check to see if new jobs are added
            if(ehsPosn < PI) {

                simulate = true;
                std::vector<satsim::EnergyConsumer*> ecs = ehsPtr->getEnergyConsumers();
                satsim::CubeSat* cubePtr = dynamic_cast<satsim::CubeSat*>(ecs.at(0));

                // Here we take the job available at the radiant position in which the satellite is
                satsim::Job* jobPtr = jobs.at(std::floor(ehsPosn/radPerJob) + (cubePtr->getWorkerId() * numberOfJobs));

                // In this point I claim all the tasks of the job at the orbital position in which the current satellite is.
                // In this way, the next satellite that will reach this position, will not have the job available.
                // I claim the job only if some tasks are available and if the Jetson is not currently working
                if(jobPtr->getUnclaimedTaskCount() > 0 && cubePtr->getClaimedJobCount() == 0 && !jobPtr->isAcquired()) {

                    cubePtr->logEvent(
                            "cubesat-"+std::to_string(cubePtr->getWorkerId())+"-found-job",
                            ehsPosn
                    );

                    //std::cout << "ADD A JOB HERE FOR SATELLITE " << std::to_string(i) << std::endl;
                    // Acquiring job
                    jobPtr->acquiringJob();
                    // Save value to later loop to wait the end of all tasks
                    remainingTasks = jobPtr->getUnclaimedTaskCount();
                    tasksBackup = remainingTasks;
                    // For CSFP, all tasks are claimed
                    jobPtr->claimTasks(cubePtr->getWorkerId(), (jobPtr->getUnclaimedTaskCount()));

                    // Send command to execute the job to the satellite and wait all response of the tasks.
                    // Once the requested tasks have arrived, proceed with the simulation
                    try {
                        std::cout << "\nStart execution of a job for the instance: " << cubePtr->getWorkerId() << std::endl;

                        if (!multipleJobs) {
                            // For single job, we send to MQTT the instance of satellite we want to execute
                            mqtt::topic top_pub(cli_pub, TOPIC_PUB + std::to_string(publishPhSat) + "/" + std::to_string(i), QOS);
                            mqtt::token_ptr tok_pub;

                            tok_pub = top_pub.publish(PAYLOAD_EXECUTE);
                            tok_pub->wait();
                        } else {
                            // For multiple jobs, we send to MQTT the instance of satellite we want to execute and the job we want to execute
                            mqtt::topic top_pub(cli_pub, TOPIC_PUB + std::to_string(publishPhSat) + "/" + std::to_string(i) + "/" + std::to_string(jobPtr->getJobId()), QOS);
                            mqtt::token_ptr tok_pub;

                            tok_pub = top_pub.publish(PAYLOAD_EXECUTE);
                            tok_pub->wait();
                        }

                        //publishPhSat = (publishPhSat % phSat) + 1;

                    }
                    catch (const mqtt::exception& exc) {
                        std::cerr << exc << std::endl;
                        return 1;
                    }

                    int taskAddedCounter = 0;
                    std::cout << "WAITING FOR TASKS" << std::endl;
                    while(remainingTasks != 0) {
                        while (WAITING_DATA != 0) {
                            /*if (RECEIVE_NO_DATA) {
                                //remainingTasks = tasksBackup;
                                //taskAddedCounter = 0;
                                cubePtr->logEvent(
                                        "cubesat-"+std::to_string(cubePtr->getWorkerId())+"-error-found",
                                        jobPtr->getJobId()
                                );
                                break;
                            }*/
                        }
                        /*
                        if (!RECEIVE_NO_DATA) {

                        } else {
                            //jobPtr->noDataFound();
                            RECEIVE_NO_DATA = false;
                            WAITING_DATA = 4;
                            DURATION_DATA = 0;
                            APP_DATA = "";
                            NON_FUNC_DATA.clear();
                            PAYLOAD_DATA.clear();
                            NON_FUNC_TIMESTAMPS.clear();
                            PAYLOAD_TIMESTAMPS.clear();
                            std::cout << "NO DATA RECEIVED!" << std::endl;
                        }*/

                        /*if (APP_DATA.rfind(ERROR_MESSAGE, 0) == 0) {
                            jobPtr->logEvent(
                                    "event-cubesat-"+std::to_string(cubePtr->getWorkerId())+"-error-found",
                                    jobPtr->getJobId()
                            );
                            std::cout << "!RADIATION ERROR FOUND!" << std::endl;
                        }*/
                        if (APP_DATA.rfind(ERROR_MESSAGE, 0) == 0) {
                            cubePtr->logEvent(
                                    "cubesat-" + std::to_string(cubePtr->getWorkerId()) + "-error-found",
                                    jobPtr->getJobId()
                            );
                            std::cout << "!RADIATION ERROR FOUND!" << std::endl;
                        }

                        taskAddedCounter++;
                        WAITING_DATA = 4;
                        satsim::Task task(DURATION_DATA, APP_DATA, NON_FUNC_DATA, PAYLOAD_DATA,
                                          NON_FUNC_TIMESTAMPS, PAYLOAD_TIMESTAMPS);
                        //jobPtr->addTaskValues(task);
                        jobPtr->addTaskValuesInJob(task, taskAddedCounter);
                        DURATION_DATA = 0;
                        APP_DATA = "";
                        NON_FUNC_DATA.clear();
                        PAYLOAD_DATA.clear();
                        NON_FUNC_TIMESTAMPS.clear();
                        PAYLOAD_TIMESTAMPS.clear();
                        //std::cout << "Created task" << std::endl;
                        remainingTasks--;
                        std::cout << "Added a task for the job " << jobPtr->getJobId() << " of the satellite " << cubePtr->getWorkerId() << ". Remaining tasks: " << remainingTasks << std::endl;
                    }

                    cubePtr->addClaimedJob(jobPtr);
                    //RECEIVE_NO_DATA = false;
                }

                if (cubePtr->isWorking()) {
                    // If I'm working, I want to proceed the simulation by the duration of a task
                    satsim::Job* jobToWorkWith = cubePtr->getFirstClaimedJob();
                    //std::cout << "JOBPTR-TOT-TASKS -> " << jobToWorkWith->getTotalTasks(cubePtr->getWorkerId()) << std::endl;

                    /*if (jobToWorkWith->getNoData()) {
                        timeToUpdateTheSimulation = 2.0e-5;
                    } else {
                        satsim::Task taskOfWorkingJob = jobToWorkWith->getTaskToExecute(jobToWorkWith->getTotalTasks(cubePtr->getWorkerId()));
                        timeToUpdateTheSimulation = taskOfWorkingJob.getDurationSeconds();
                        //std::cout << "TASKPTR-S -> " << taskOfWorkingJob.getDurationSeconds() << std::endl;
                        //std::cout << "CUBEPTR -> " << cubePtr->getWorkerId() << std::endl;
                        //std::cout << "JOBPTR -> " << jobToWorkWith->getJobId() << std::endl;
                        //std::cout << "TASKPTR-MS -> " << taskOfWorkingJob.getDurationMilliseconds() << std::endl;
                        //std::cout << "WORKING SATELLITE " << std::to_string(i) << std::endl;
                    }*/
                    satsim::Task taskOfWorkingJob = jobToWorkWith->getTaskToExecute(jobToWorkWith->getTotalTasks(cubePtr->getWorkerId()));
                    timeToUpdateTheSimulation = taskOfWorkingJob.getDurationSeconds();
                } else {
                    if (print_value == 0) {
                        print_value = 10000000;
                        std::cout << "POSITION IN THE ORBIT " << std::to_string(ehsPosn) << ", TRYING TO ACCESS THE JOB " << std::to_string(ehsPosn/radPerJob) << ". THE SATELLITE IS IDLE" << std::endl;
                    }
                    print_value--;
                    // Proceed the simulation of 20 microseconds
                    //timeToUpdateTheSimulation = 2.0e-5;
                    timeToUpdateTheSimulation = timeStaticToUpdateTheSimulation;
                }

                // Clean up
                cubePtr  = NULL;
                jobPtr = NULL;
                for(size_t j = 0; j < ecs.size(); j++) {
                    ecs.at(j) = NULL;
                }
                ecs.clear();

                // Update
                ehsPtr->update(timeToUpdateTheSimulation);
            }
                // otherwise, continue updating if CubeSat is not idle
            else {
                std::vector<satsim::EnergyConsumer*> ecs = ehsPtr->getEnergyConsumers();
                satsim::CubeSat* cubePtr = dynamic_cast<satsim::CubeSat*>(ecs.at(0));
                // Update

                if(!cubePtr->isIdle()) {
                    simulate = true;

                    if (cubePtr->isWorking()) {
                        // If I'm working, I want to proceed the simulation by the duration of a task
                        satsim::Job* jobToWorkWith = cubePtr->getFirstClaimedJob();
                        //std::cout << "JOBPTR-TOT-TASKS -> " << jobToWorkWith->getTotalTasks(cubePtr->getWorkerId()) << std::endl;

                        /*if (jobToWorkWith->getNoData()) {
                            timeToUpdateTheSimulation = 2.0e-5;
                        } else {
                            satsim::Task taskOfWorkingJob = jobToWorkWith->getTaskToExecute(jobToWorkWith->getTotalTasks(cubePtr->getWorkerId()));
                            timeToUpdateTheSimulation = taskOfWorkingJob.getDurationSeconds();
                            //std::cout << "TASKPTR-S -> " << taskOfWorkingJob.getDurationSeconds() << std::endl;
                            //std::cout << "CUBEPTR -> " << cubePtr->getWorkerId() << std::endl;
                            //std::cout << "JOBPTR -> " << jobToWorkWith->getJobId() << std::endl;
                            //std::cout << "TASKPTR-MS -> " << taskOfWorkingJob.getDurationMilliseconds() << std::endl;
                            //std::cout << "WORKING SATELLITE " << std::to_string(i) << std::endl;
                        }*/
                        satsim::Task taskOfWorkingJob = jobToWorkWith->getTaskToExecute(jobToWorkWith->getTotalTasks(cubePtr->getWorkerId()));
                        timeToUpdateTheSimulation = taskOfWorkingJob.getDurationSeconds();
                    } else {
                        // Proceed the simulation of 20 microseconds
                        //timeToUpdateTheSimulation = 2.0e-5;
                        timeToUpdateTheSimulation = timeStaticToUpdateTheSimulation;
                    }

                    // Update
                    ehsPtr->update(timeToUpdateTheSimulation);
                }

                // Clean up
                cubePtr  = NULL;
                for(size_t j = 0; j < ecs.size(); j++) {
                    ecs.at(j) = NULL;
                }
                ecs.clear();
            }

            // Clean up
            ehsPtr = NULL;
        }
    }
    // Simulation is over, all Cubesats are in idle mode
    for(size_t i = 0; i < ehsatellites.size(); i++) {
        satsim::EHSatellite* ehsPtr = ehsatellites.at(i);
        std::vector<satsim::EnergyConsumer*> ecs = ehsPtr->getEnergyConsumers();
        satsim::CubeSat* cubePtr = dynamic_cast<satsim::CubeSat*>(ecs.at(0));
        cubePtr->logEvent(
                "cubesat-"+std::to_string(cubePtr->getWorkerId())+"-idle-stop",
                cubePtr->getSimTime()
        );
        // Clean up
        cubePtr  = NULL;
        for(size_t j = 0; j < ecs.size(); j++) {
            ecs.at(j) = NULL;
        }
        ecs.clear();
        ehsPtr = NULL;
    }

    // Disconnect publisher
    std::cout << "\nDisconnecting publisher..." << std::endl;
    cli_pub.disconnect()->wait();
    std::cout << "  ...Disconnected" << std::endl;

    //Disconnecting subscriber
    try {
        std::cout << "\nDisconnecting subscriber..." << std::endl;
        cli_sub.disconnect()->wait();
        std::cout << "...Disconnected" << std::endl;
    }
    catch (const mqtt::exception& exc) {
        std::cerr << exc << std::endl;
        return 1;
    }

    // Write out logs
    std::ostringstream oss;
    std::cout << "Writing logs" << std::endl;
    oss << "../logs/" << std::setfill('0') << std::setw(3)
        << std::atoi(argv[1]);
    logger.exportCsvs(oss.str());
    std::cout << "Logs written" << std::endl;
    // Clean up each satellite in the pipeline
    for(size_t i = 0; i < ehsatellites.size(); i++) {
        delete ehsatellites.at(i);
    }
    // Clean up jobs
    for(size_t i = 0; i < jobs.size(); i++) {
        delete jobs.at(i);
    }
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
        //std::cout << s.substr(start, end - start) << std::endl;
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

std::vector<size_t> innerSplitFirstValue(std::string s, std::string outerDel, std::string innerDel)
{
    int start, end = -1*outerDel.size();
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
        end = -1*innerDel.size();
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

bool containsString(std::string s, std::string substring)
{
    return s.rfind(substring, 0) == 0;
}

bool physicalSatellitesAreBusy(size_t phSat) {
    return satelliteUsed == (phSat + 1);
}