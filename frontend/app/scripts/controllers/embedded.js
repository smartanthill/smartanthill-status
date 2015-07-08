/**
  Copyright (C) 2015 OLogN Technologies AG

  This source file is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License version 2
  as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

(function() {
  'use strict';

  angular
    .module('siteApp')
    .controller('EmbeddedController', EmbeddedController);

  function EmbeddedController($route, embeddedEnvironmentsList, buildStatistics) {
    var vm = this;

    vm.envs = embeddedEnvironmentsList;
    vm.chartConfig = {
      'series': [],
      'data': [],
    }

    vm.envName = $route.current.params.envName;
    vm.singleEnv = buildStatistics.length == 1;
    if (vm.singleEnv){
      vm.tableData = buildStatistics[0];
    }

    var builds = [], build_id;
    for (var env in buildStatistics){
      for (var i = 0; i < buildStatistics[env].length; i++){
        build_id = buildStatistics[env][i].build_id;
        if (!_arrayContains(builds, build_id)){
          builds.push(build_id);
        }
      }
    }
    builds.sort();

    var envName, ram_usage, rom_usage, record;
    angular.forEach(buildStatistics, function(envStatistics){
      envName = envStatistics[0]['env']
      ram_usage = _initArray(builds.length);
      rom_usage = _initArray(builds.length);
      for (var i in envStatistics){
        record = envStatistics[i];
        ram_usage[builds.indexOf(record.build_id)] = record.ram;
        rom_usage[builds.indexOf(record.build_id)] = record.rom;
      }
      vm.chartConfig['series'].push(envName + ' RAM usage')
      vm.chartConfig['data'].push(ram_usage)
      vm.chartConfig['series'].push(envName + ' ROM usage')
      vm.chartConfig['data'].push(rom_usage)
    });
    vm.chartConfig['labels'] = builds

    ////////////

    function _initArray(size){
      var arr = [];
      for (var i = 0; i < size; i++){
        arr[i] = 0;
      }
      return arr;
    }

    function _arrayContains(arr, value){
      return arr.indexOf(value) != -1;
    }
  }
})();
