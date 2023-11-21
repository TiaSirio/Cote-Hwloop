#!/bin/bash

source simulation.conf

if [ "$singleJob" -eq 1 ]; then
    mapperType="s"
else
    mapperType="m"
fi

numberOfSatellite=$1
satVal="satellite${numberOfSatellite}"

sshToSat=$(grep "^$satVal=" phSatToUse.conf | cut -d'=' -f2)

if [ -z "$sshToSat" ]; then
    sshToSat=$sshFakeSatellite
fi

mapperFilePositionToSCPFakeSat="${execDir}${mapperFileName}"

#checkIfRealOrFalse=$(grep "^$sshToSat=" checkAddressSatellite.conf | cut -d'=' -f2)
#datasetsDir=$(grep "^$sshToSat=" datasetsDirPhysicalSatellite.conf | cut -d'=' -f2)

if [[ $sshToSat == $sshFakeSatellite ]]; then

    fakeSatDirPosition="${reachingHomeInFakeSatellites}${dirOnFakeSatellite}"

    echo "Start configuring fake nanosatellites..."

    attempt=0
    while [ $attempt -lt "$maxNumberOfAttempts" ]; do
      if scp "$mapperFilePositionToSCPFakeSat" "$sshToSat:$fakeSatDirPosition"
      then
        break
      else
        echo "SCP operation failed! Retrying in 2 seconds..."
        sleep 2
        attempt=$((attempt + 1))
      fi
    done
    if [ $attempt -eq "$maxNumberOfAttempts" ]; then
      echo "SCP operation failed after $attempt attempts. Couldn't configure fake nanosatellites. Exiting with code 1."
      exit 1
    fi

    # Compile programs and execute satellite programs
    attemptSSH=0
    while [ $attemptSSH -lt "$maxNumberOfAttempts" ]; do
      if ssh "$sshToSat" "cd $dirOnFakeSatellite && ./$startFakeSatelliteScriptsFromSim $physicalInstances $numberOfSatellite $mapperType $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $radiationErrorRatio $errorMessage"
      then
        echo "Configured fake satellites!"
        break
      else
        echo "SSH connection or remote command failed! Retrying in 2 seconds..."
        sleep 2
        attemptSSH=$((attemptSSH + 1))
      fi
    done

    if [ $attemptSSH -eq "$maxNumberOfAttempts" ]; then
      echo "SSH connection failed after $attemptSSH attempts. Couldn't configure fake nanosatellites. Exiting with code 1."
      exit 1
    fi

    echo "Fake Cubesatsims ready!"
    exit 2
else
    echo "Start configuring $sshToSat..."

    phSatDir=$(grep "^$sshToSat=" execDirPhysicalSatellite.conf | cut -d'=' -f2)
    nonFuncDataOnPhSat=$(grep "^$sshToSat=" nonFuncOnPhysicalSatellite.conf | cut -d'=' -f2)
    payloadOnPhSat=$(grep "^$sshToSat=" payloadOnPhysicalSatellite.conf | cut -d'=' -f2)

    # Rsync
    attemptReal=0
    while [ $attemptReal -lt "$maxNumberOfAttempts" ]; do
      if rsync -avh --delete --exclude "/c_tasks/" "$execDir" "$sshToSat":"$phSatDir"
      # if rsync -avh --delete "$execDir" "$sshToSat":"$phSatDir"
      then
        echo "RSYNC operation succeeded."
        break
      else
        echo "RSYNC operation failed! Retrying in 2 seconds..."
        sleep 2
        attemptReal=$((attemptReal + 1))
      fi
    done

    if [ $attemptReal -eq "$maxNumberOfAttempts" ]; then
      echo "RSYNC operation failed after $attemptReal attempts. Couldn't configure $sshToSat. Exiting with code 1."
      exit 1
    fi

    # if ! rsync -avh --delete cexec/ "$sshToSat":/home/pi/CubeSatSim/simulationFiles/cexec/
    # if ! rsync -avh --delete cexec/ "$sshToSat":"$phSatDir"
    # if ! rsync -avh --delete "$execDir" "$sshToSat":"$phSatDir"
    # then
    #   echo "rsync operation failed!"
    #   exit 1
    # fi

    evaluationToCompare="commandReceiverRadiationEvaluation.py"

    attemptRealSSH=0
    while [ $attemptRealSSH -lt "$maxNumberOfAttempts" ]; do
      if [ "$evaluationToCompare" = "$typeOfCommandReceiverUsed" ]; then
        if ssh "$sshToSat" "cd $phSatDir && ./$makeForEveryTask && ./$startScriptsOnTheSatellite $mapperType $numberOfSatellite $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $nonFuncDataOnPhSat $payloadOnPhSat $phSatDir $radiationErrorRatio $errorMessage $tasksExecutablesConf $tasksDatasetsConf $tasksResultsConf $tasksTypeOfFileConf $typeOfCommandReceiverUsed $typeOfRadiationFault $outputCleanerBash $faultCreatorBash $executeFaultedTaskBash $executeFaultedTaskAllInputsBash $executeFaultedTaskSequentialInputsBash $executeTaskAllInputsBash $executeTaskSequentialInputsBash $maxTimeBeforeStopRadiatedProgram $repeatProgramsConf $executeTaskMultipleTimesBash"
        then
          echo "Configured $sshToSat evaluation!"
          break
        else
          echo "SSH connection or remote command failed! Retrying in 2 seconds..."
          sleep 2
          attemptRealSSH=$((attemptRealSSH + 1))
        fi
      else
        if ssh "$sshToSat" "cd $phSatDir && ./$makeForEveryTask && ./$startScriptsOnTheSatellite $mapperType $numberOfSatellite $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $nonFuncDataOnPhSat $payloadOnPhSat $phSatDir $radiationErrorRatio $errorMessage $tasksExecutablesConf $tasksDatasetsConf $tasksResultsConf $tasksTypeOfFileConf $typeOfCommandReceiverUsed $typeOfRadiationFault $outputCleanerBash $faultCreatorBash $executeFaultedTaskBash $executeFaultedTaskAllInputsBash $executeFaultedTaskSequentialInputsBash $executeTaskAllInputsBash $executeTaskSequentialInputsBash $maxTimeBeforeStopRadiatedProgram"
        then
          echo "Configured $sshToSat!"
          break
        else
          echo "SSH connection or remote command failed! Retrying in 2 seconds..."
          sleep 2
          attemptRealSSH=$((attemptRealSSH + 1))
        fi
      fi
    done

    if [ $attemptRealSSH -eq "$maxNumberOfAttempts" ]; then
      echo "SSH operation failed after $attemptRealSSH attempts. Couldn't configure $sshToSat. Exiting with code 1."
      exit 1
    fi

    # Compile programs and execute satellite programs
    # if ! ssh "$sshToSat" "cd $phSatDir && ./$makeForEveryTask && ./$startScriptsOnTheSatellite $mapperType $numberOfSatellite $serverMQTT $portMQTT $topicCommands $topicDuration $topicNonFuncData $topicPayload $topicAppData $mapperFileName $satelliteID $commandExecute $noDataMessage $nonFuncDataOnPhSat $payloadOnPhSat $phSatDir $radiationErrorRatio $errorMessage $tasksExecutablesConf $tasksDatasetsConf $tasksResultsConf $tasksTypeOfFileConf $typeOfCommandReceiverUsed $typeOfRadiationFault $outputCleanerBash $faultCreatorBash $executeFaultedTaskBash $executeFaultedTaskAllInputsBash $executeFaultedTaskSequentialInputsBash $executeTaskAllInputsBash $executeTaskSequentialInputsBash"
    # then
    #   echo "SSH connection or remote command failed!"
    #  exit 1
    # fi
fi

echo "All satellites configured!"
exit 0

