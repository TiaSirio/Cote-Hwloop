// Receive.cpp
// Receive class implementation file
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
#include <algorithm>     // max
#include <array>         // array
#include <cstddef>       // NULL
#include <utility>       // move

// comsim
#include <DateTime.hpp>  // DateTime
#include <Log.hpp>       // Log
#include <Receive.hpp>   // Receive
#include <Vertex.hpp>    // Vertex
#include <utilities.hpp> // utilities

namespace comsim {
  Receive::Receive(
   const std::array<double,3>& posn, const double& gainDB,
   const DateTime* const globalTime, const uint32_t& id, Log* const log
  ) : Vertex(), posn(posn), globalTime(globalTime), id(id), log(log) {
    this->setGain(gainDB);
  }

  Receive::Receive(const Receive& receive) : Vertex(receive),
   posn(receive.getPosn()), gainFactor(receive.getGain()),
   globalTime(receive.getGlobalTime()), id(receive.getID()),
   log(receive.getLog()) {}

  Receive::Receive(Receive&& receive) : Vertex(std::move(receive)),
   posn(receive.posn), gainFactor(receive.gainFactor),
   globalTime(receive.globalTime), id(receive.id), log(receive.log) {
    receive.globalTime = NULL;
    receive.log = NULL;
  }

  Receive::~Receive() {
    this->globalTime = NULL;
    this->log = NULL;
  }

  Receive& Receive::operator=(const Receive& receive) {
    Receive temp(receive);
    *this = std::move(temp);
    return *this;
  }

  Receive& Receive::operator=(Receive&& receive) {
    this->Vertex::operator=(std::move(receive));
    this->posn = receive.posn;
    this->gainFactor = receive.gainFactor;
    this->globalTime = receive.globalTime;
    this->id = receive.id;
    this->log = receive.log;
    receive.globalTime = NULL;
    receive.log = NULL;
    return *this;
  }

  Receive* Receive::clone() const {
    return new Receive(*this);
  }

  std::array<double,3> Receive::getPosn() const {
    return this->posn;
  }

  double Receive::getGain() const {
    return this->gainFactor;
  }

  const DateTime* Receive::getGlobalTime() const {
    return this->globalTime;
  }

  uint32_t Receive::getID() const {
    return this->id;
  }

  Log* Receive::getLog() const {
    return this->log;
  }

  void Receive::setPosn(const std::array<double,3>& posn) {
    this->posn = posn;
  }

  void Receive::setGain(const double& gainDB) {
    this->gainFactor = std::max(1.0,util::dB2Dec(gainDB));
  }

  void Receive::update(const uint32_t& nanosecond) {
    // **It is expected that this->globalTime has already been updated**
    // Perform (possibly custom) update for localTime
    //this->localTime.update(nanosecond);
  }

  void Receive::update(const uint8_t& second, const uint32_t& nanosecond) {
    // **It is expected that this->globalTime has already been updated**
    // Perform (possibly custom) update for localTime
    //this->localTime.update(second,nanosecond);
  }

  void Receive::update(
   const uint8_t& minute, const uint8_t& second, const uint32_t& nanosecond
  ) {
    // **It is expected that this->globalTime has already been updated**
    // Perform (possibly custom) update for localTime
    //this->localTime.update(minute,second,nanosecond);
  }

  void Receive::update(
   const uint8_t& hour, const uint8_t& minute, const uint8_t& second,
   const uint32_t& nanosecond
  ) {
    // **It is expected that this->globalTime has already been updated**
    // Perform (possibly custom) update for localTime
    //this->localTime.update(hour,minute,second,nanosecond);
  }
}
