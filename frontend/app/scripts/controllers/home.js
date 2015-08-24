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
    .controller('HomeController', HomeController);

  function HomeController() {
    var vm = this;

    vm.projects = [
      {
        'name': 'SmartAnthill 2.0',
        'travis': {
          'slug': 'smartanthill/smartanthill2_0',
        },
      },
      {
        'name': 'SmartAnthill 2.0 Dashboard',
        'travis': {
          'slug': 'smartanthill/smartanthill2_0-dashboard',
        },
      },
      {
        'name': 'SmartAnthill Communication Stack server',
        'travis': {
          'slug': 'smartanthill/smartanthill-commstack-server',
        },
        'appveyor': {
          'slug': 'ivankravets/smartanthill-commstack-server',
          'code': 'ntqx6hy0a8aoqatj'
        }
      },
      {
        'name': 'SmartAnthill 2.0 Embedded System',
        'travis': {
          'slug': 'smartanthill/smartanthill2_0-embedded',
        },
      },
      {
        'name': 'SmartAnthill Zepto Compiler',
        'travis': {
          'slug': 'smartanthill/smartanthill-zepto-compiler',
        },
      },
    ];

  }
})();
