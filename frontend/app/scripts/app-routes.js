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
    .factory('httpErrorInterceptor', httpErrorInterceptor)
    .config(routeConfig);

  function httpErrorInterceptor($q, $window) {
    return {
      'responseError': function(rejection) {
        if (rejection.status === 404) {
          $window.location.href = '#!/404';
        }
        return $q.reject(rejection);
      }
    };
  }

  function routeConfig($locationProvider, $routeProvider, $httpProvider) {
    $locationProvider.hashPrefix('!');

    $httpProvider.interceptors.push('httpErrorInterceptor');

    $routeProvider
      .when('/', {
        templateUrl: 'views/home.html',
        controller: 'HomeController',
        controllerAs: 'vm',
      })
      .when('/embedded/:envName?', {
        templateUrl: 'views/embedded.html',
        controller: 'EmbeddedController',
        controllerAs: 'vm',
        resolve: {
          embeddedEnvironmentsList: ['dataService', function(dataService){
            return dataService.getEmbeddedEnvironmentsList().$promise;
          }],
          buildStatistics: ['$route', '$q', 'dataService', function($route, $q, dataService){
            function queryBuildStatistics(env){
              return dataService.getEmbeddedBuildStatistics(env).$promise;
            }
            if (typeof($route.current.params.envName) != 'undefined'){
              return $q.all([queryBuildStatistics($route.current.params.envName)]);
            } else {
              return dataService.getEmbeddedEnvironmentsList().$promise
                .then(function(envNames){
                  return $q.all(envNames.reduce(function(obj, envName){
                    obj[envName] = queryBuildStatistics(envName);
                    return obj;
                  }, {}));
                });
            }

          }]
        }
      })
      .when('/404', {
        templateUrl: 'views/404.html'
      })
      .otherwise({
        redirectTo: '/404'
      });
  }

})();
