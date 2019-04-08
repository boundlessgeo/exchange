'use strict';

(function(){

  var module = angular.module('geonode_main_search', ['ngclipboard'], function($locationProvider) {
      if (window.navigator.userAgent.indexOf("MSIE") == -1){
          $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
          });

          // make sure that angular doesn't intercept the page links
          angular.element("a").prop("target", "_self");
      }
    });


    module.filter('friendlyScheme', function () {

        return function (text) {

            var mapping = {'AIMS--http-get-feature': 'FeatureServer', 'AIMS--http-get-map': 'MapServer',
                'AIMS--http-get-image': 'ImageServer'}

            if (text === undefined) {
                return text;

            } else {
                var friendlyParts = text.split(':');
                if (friendlyParts.length == 2) {
                    return mapping[friendlyParts[1]] || friendlyParts[1];
                } else if (friendlyParts.length == 3) {
		// if it's ESRI:ArcGIS:FeatureServer, just display FeatureServer		
		    return friendlyParts[2]; 		
		} else {
                    return text;
                }

            }
        }
    });

    module.filter('orderObjectBy', function() {
      return function(items, field, reverse) {
        var filtered = [];
        angular.forEach(items, function(item) {
          filtered.push(item);
        });
        filtered.sort(function (a, b) {
          return (a[field] > b[field] ? 1 : -1);
        });
        if(reverse) filtered.reverse();
        return filtered;
      };
    });

    // Used to set the class of the filters based on the url parameters
    module.set_initial_filters_from_query = function (data, url_query, filter_param){
        for(var i=0;i<data.length;i++){
            if( url_query == data[i][filter_param] || url_query.indexOf(data[i][filter_param] ) != -1){
                data[i].active = 'active';
            }else{
                data[i].active = '';
            }
        }
        return data;
    }

  // Load facets
  module.load_facets = function ($http, $rootScope, $location){
        var base_search_url = '/api/base/search/?q=&limit=0';
        $http.get(base_search_url).then(function(response){
          var facets = response.data.meta.facets;
          $rootScope.facets = facets;
    });
  }

  // Update facet counts
  module.haystack_facets = function($http, $rootScope, $location) {
      var data = $rootScope.query_data;
      $rootScope.facets = data.meta.facets;
  }

  /*
  * Load categories and keywords
  */
  module.run(function($http, $rootScope, $location){
    /*
    * Load categories and keywords if the filter is available in the page
    * and set active class if needed
    */
    module.load_facets($http, $rootScope, $location);

    // Activate the sort filter if in the url
    if($location.search().hasOwnProperty('order_by')){
      var sort = $location.search()['order_by'];
      $('body').find("[data-filter='order_by']").removeClass('selected');
      $('body').find("[data-filter='order_by'][data-value="+sort+"]").addClass('selected');
    }

    if ($location.search().hasOwnProperty('type__in')){
      var type = $location.search()['type__in'];
      var type_filter = $('body').find("[data-filter='type__in'][data-value="+type+"]");
      var element = $(type_filter[0]);
      element.parents('ul').find('a').removeClass('selected');
      element.addClass('selected');      
    }

  });

  /*
  * Main search controller
  * Load data from api and defines the multiple and single choice handlers
  * Syncs the browser url with the selections
  */
  module.controller('geonode_search_controller', function($injector, $scope, $location, $http, Configs){
    $scope.query = $location.search();
    $scope.query.limit = $scope.query.limit || CLIENT_RESULTS_LIMIT;
    $scope.query.offset = $scope.query.offset || 0;
    $scope.page = Math.round(($scope.query.offset / $scope.query.limit) + 1);
    $scope.location = $location.protocol() + '://'+ $location.host();

    $scope.onCopySuccess = function(e) {
    	$(e.trigger).trigger('copied', ['Copied!']);
     	e.clearSelection();
    };

    $scope.onCopyError = function(e) {
	    $(e.trigger).trigger('copied', ['Failed to Copy!']);
    }

    //Get data from apis and make them available to the page
    function query_api(data){
      $http.get(Configs.url, {params: data || {}}).then(function(response){
        $scope.results = response.data.objects;
        $scope.total_counts = response.data.meta.total_count;
        $scope.$root.query_data = response.data;

        if ($location.search().hasOwnProperty('q')){
          $scope.text_query = $location.search()['q'].replace(/\+/g," ");
        }
        module.haystack_facets($http, $scope.$root, $location);
      });
    };
    query_api($scope.query);


    /*
    * Pagination
    */
    // Control what happens when the total results change
    $scope.$watch('total_counts', function(){
      $scope.numpages = Math.round(
        ($scope.total_counts / $scope.query.limit) + 0.49
      );

      // In case the user is viewing a page > 1 and a
      // subsequent query returns less pages, then
      // reset the page to one and search again.
      if($scope.numpages < $scope.page){
        $scope.page = 1;
        $scope.query.offset = 0;
        query_api($scope.query);
      }

      // In case of no results, the number of pages is one.
      if($scope.numpages == 0){$scope.numpages = 1};
    });

    $scope.paginate_down = function(){
      if($scope.page > 1){
        $scope.page -= 1;
        $scope.query.offset =  $scope.query.limit * ($scope.page - 1);
        query_api($scope.query);
      }
    }

    $scope.paginate_up = function(){
      if($scope.numpages > $scope.page){
        $scope.page += 1;
        $scope.query.offset = $scope.query.limit * ($scope.page - 1);
        query_api($scope.query);
      }
    }
    /*
    * End pagination
    */


    if (!Configs.hasOwnProperty("disableQuerySync")) {
        // Keep in sync the page location with the query object
        $scope.$watch('query', function(){
          $location.search($scope.query);
        }, true);
    }


    /*
    * Add the selection behavior to the element, it adds/removes the 'active' class
    * and pushes/removes the value of the element from the query object
    */
    $scope.multiple_choice_listener = function($event){
      var element = $($event.target).closest("a");
      var query_entry = [];
      var data_filter = element.attr('data-filter');
      var value = element.attr('data-value');

      // If the query object has the record then grab it
      if ($scope.query.hasOwnProperty(data_filter)){

        // When in the location are passed two filters of the same
        // type then they are put in an array otherwise is a single string
        if ($scope.query[data_filter] instanceof Array){
          query_entry = $scope.query[data_filter];
        }else{
          query_entry.push($scope.query[data_filter]);
        }
      }

      // If the element is active active then deactivate it
      if(element.hasClass('active')){
        // clear the active class from it
        element.removeClass('active');

        // Remove the entry from the correct query in scope

        query_entry.splice(query_entry.indexOf(value), 1);
      }
      // if is not active then activate it
      else if(!element.hasClass('active')){
        // Add the entry in the correct query
        if (query_entry.indexOf(value) == -1){
          query_entry.push(value);
        }
        element.addClass('active');
      }

      //save back the new query entry to the scope query
      $scope.query[data_filter] = query_entry;

      //if the entry is empty then delete the property from the query
      if(query_entry.length == 0){
        delete($scope.query[data_filter]);
      }
      query_api($scope.query);
    }

    $scope.single_choice_listener = function($event){
      var element = $($event.target).closest("a");
      var query_entry = [];
      var data_filter = element.attr('data-filter');
      var value = element.attr('data-value');
      // Type of data being displayed, use 'content' instead of 'all'
      $scope.dataValue = (value == 'all') ? 'content' : value;

      // If the query object has the record then grab it
      if ($scope.query.hasOwnProperty(data_filter)){
        query_entry = $scope.query[data_filter];
      }

      if(!element.hasClass('selected')){
        // Add the entry in the correct query
        query_entry = value;

        // clear the active class from it
        element.parents('ul').find('a').removeClass('selected');

        element.addClass('selected');

        //save back the new query entry to the scope query
        $scope.query[data_filter] = query_entry;

        query_api($scope.query);
      }
    }

    $scope.clear_filters = function() {
      // reset query
      $scope.query = {};
      $scope.query.limit = $scope.query.limit || CLIENT_RESULTS_LIMIT;
      $scope.query.offset = $scope.query.offset || 0;
    }

    $scope.api_query = function(endpoint) {
      // expecting a django api endpoint i.e. /api/layers/
      $http.get(endpoint, {params: $scope.query || {}}).then(function(response){
        $scope.results = response.data.objects;
        $scope.total_counts = response.data.meta.total_count;
        $scope.$root.query_data = response.data;

        if ($location.search().hasOwnProperty('q')){
          $scope.text_query = $location.search()['q'].replace(/\+/g," ");
        }
        module.haystack_facets($http, $scope.$root, $location);
      });
    }

    $scope.tab_activation = function($event) {
      var element = $($event.target).closest("a");
      if(!element.hasClass('selected')){
        // clear the active class from it
        element.parents('ul').find('a').removeClass('selected');

        element.addClass('selected');
      }
    }

    $scope.navcontrol = function(e) {
      e.preventDefault();
      var element = $(e.target);
      if (element.parents("h4").siblings(".nav").is(":visible")) {
        element.parents("h4").siblings(".nav").slideUp();
        element.find("i").attr("class", "fa fa-chevron-right");
      } else {
        element.parents("h4").siblings(".nav").slideDown();
        element.find("i").attr("class", "fa fa-chevron-down");
      }
  };

    $scope.filterTime = function($event) {
        var element = $($event.target);
        var on = (element[0].checked === true);

        if(on) {
            $scope.query['has_time'] = 'true';
        } else {
            if($scope.query['has_time']) {
                delete $scope.query['has_time'];
            }
        }

        query_api($scope.query);
    }

    $('#text_search_btn').click(function(){
      $scope.query['q'] = $('#text_search_input').val();
      query_api($scope.query);
    });

    $('#text_search_input').keypress(function(e) {
      if(e.which == 13) {
        $('#text_search_btn').click();
      }
    });

    // This is a hotfix to conflicting CSS styles between
    // .nav .filter .active and .list-group-item .active
    // Can be removed if .list-group-item .active takes priority
    $scope.toggle_text_color = function($event) {
      var element = $($event.target);
      if (element.hasClass('active')) {
        element.css('color', '#fff');
      } else {
        element.css('color', '#333');
      }
    }


    $scope.feature_select = function($event){
      var element = $($event.target);
      var article = $(element.parents('article')[0]);
      if (article.hasClass('resource_selected')){
        element.html('Select');
        article.removeClass('resource_selected');
      }
      else{
        element.html('Deselect');
        article.addClass('resource_selected');
      }
    };

    /*
    * Date management
    */

    $scope.date_query = {
      'date__gte': '',
      'date__lte': ''
    };
    var init_date = true;
    $scope.$watch('date_query', function(){
      if($scope.date_query.date__gte != '' && $scope.date_query.date__lte != ''){
        $scope.query['date__range'] = $scope.date_query.date__gte + ',' + $scope.date_query.date__lte;
        delete $scope.query['date__gte'];
        delete $scope.query['date__lte'];
      }else if ($scope.date_query.date__gte != ''){
        $scope.query['date__gte'] = $scope.date_query.date__gte;
        delete $scope.query['date__range'];
        delete $scope.query['date__lte'];
      }else if ($scope.date_query.date__lte != ''){
        $scope.query['date__lte'] = $scope.date_query.date__lte;
        delete $scope.query['date__range'];
        delete $scope.query['date__gte'];
      }else{
        delete $scope.query['date__range'];
        delete $scope.query['date__gte'];
        delete $scope.query['date__lte'];
      }
      if (!init_date){
        query_api($scope.query);
      }else{
        init_date = false;
      }

    }, true);

    /*
    * Spatial search
    */
    if ($('#preview_map').length > 0) {
      document.addEventListener("DOMContentLoaded", function (event) {
        MoW.ready(function() {
            var map = new MoW.Map({
              target: 'preview_map',
            });
            
            var bounds = [-179,-89,179,89].join(', ');  // Whole world extent
            $scope.query['extent'] = bounds;
            query_api($scope.query);

            var eventQueue = map.events;
            eventQueue.subscribe(MoW.Events.ID.MAP_MOVE, function(event, data) {
              var bounds = data.boundingBox.join(', ');
              $scope.query['extent'] = bounds;
              query_api($scope.query);

              // var bounds = map.getBounds();
              // var bounds = map.boundingBox;
              // var new_bounds = [];
              // var changed = false;

              // if (
              //   (bounds.getWest() > 180 || bounds.getWest() < -180) ||
              //   (bounds.getNorth() > 90 || bounds.getNorth() < -90) ||
              //   (bounds.getEast() > 180 || bounds.getEast() < -180) ||
              //   (bounds.getSouth() > 90 || bounds.getSouth() < -90)
              //   ) {
              //   changed = true;
              // }

              // new_bounds[0] = Math.min(180, Math.max(-180, bounds.getWest()));
              // new_bounds[1] = Math.min(90, Math.max(-90, bounds.getSouth()));
              // new_bounds[2] = Math.max(-180, Math.min(180, bounds.getEast()));
              // new_bounds[3] = Math.max(-90, Math.min(90, bounds.getNorth()));

              // if (!skip_move_check && changed) {
              //   skip_move_check = true;
              //   var sw = L.latLng({lat: new_bounds[1], lon: new_bounds[0]});
              //   var ne = L.latLng({lat: new_bounds[3], lon: new_bounds[2]});
              //   map.panInsideBounds(L.latLngBounds(sw, ne));
              // } else {
                // $scope.query['extent'] = map.boundingBox.join(', ');
                // query_api($scope.query);
              //   skip_move_check = false;
              // }
            });
            // map.setBasemap(MoW.Basemap.ID.LOW_BW_CADRG);
        });
      });
    }
    // if ($('.leaflet_map').length > 0) {
    //   angular.extend($scope, {
    //     layers: {
    //       baselayers: {
    //         stamen: {
    //           name: 'Toner Lite',
    //           type: 'xyz',
    //           url: 'http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png',
    //           layerOptions: {
    //             subdomains: ['a', 'b', 'c'],
    //             attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>',
    //             continuousWorld: true
    //           }
    //         }
    //       }
    //     },
    //     map_center: {
    //       lat: 5.6,
    //       lng: 3.9,
    //       zoom: 0
    //     },
    //     defaults: {
    //       zoomControl: false
    //     }
    //   });


    //   var leafletData = $injector.get('leafletData'),
    //       map = leafletData.getMap('filter-map');

    //   map.then(function(map){
    //     /* prevent the user from wrapping around the world. */
    //     // map.setMaxBounds([[-180, -90], [180, 90]]);

    //     var skip_move_check = false;
    //     map.on('moveend', function(){
    //       var bounds = map.getBounds();
    //       var new_bounds = [];
    //       var changed = false;

    //       if (
    //          (bounds.getWest() > 180 || bounds.getWest() < -180) ||
    //          (bounds.getNorth() > 90 || bounds.getNorth() < -90) ||
    //          (bounds.getEast() > 180 || bounds.getEast() < -180) ||
    //          (bounds.getSouth() > 90 || bounds.getSouth() < -90)
    //         ) {
    //         changed = true;
    //       }

    //       new_bounds[0] = Math.min(180, Math.max(-180, bounds.getWest()));
    //       new_bounds[1] = Math.min(90, Math.max(-90, bounds.getSouth()));
    //       new_bounds[2] = Math.max(-180, Math.min(180, bounds.getEast()));
    //       new_bounds[3] = Math.max(-90, Math.min(90, bounds.getNorth()));

    //       if (!skip_move_check && changed) {
    //         skip_move_check = true;
    //         var sw = L.latLng({lat: new_bounds[1], lon: new_bounds[0]});
    //         var ne = L.latLng({lat: new_bounds[3], lon: new_bounds[2]});
    //         map.panInsideBounds(L.latLngBounds(sw, ne));
    //       } else {
    //         $scope.query['extent'] = map.getBounds().toBBoxString();
    //         query_api($scope.query);
    //         skip_move_check = false;
    //       }
    //     });
    //   });

    //   var showMap = false;
    //   $('#_extent_filter').click(function(evt) {
    //  	showMap = !showMap
    //     if (showMap){
    //       leafletData.getMap().then(function(map) {
    //         map.invalidateSize();
    //       });
    //     } else {
    //         /* clear the extent filter when the map is hidden */
    //         delete $scope.query['extent'];
    //         query_api($scope.query);
    //     }
    //   });
    // }
  });
})();
