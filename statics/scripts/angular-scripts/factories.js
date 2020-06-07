define(function() {
	'use strict';
	
    var app =  angular.module('app');
    
    app.factory('appFactory', function($http, toastr, $filter) {
		return {
			getBorrowerName: function(borrowerId){
                return $http.get('/api/borrowers/borrowers/', {params:{ borrowerId : borrowerId }}).then(
                    function(response){   
                    return response.data[0].cooperativeName  
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Borrower Name. Please contact System Administrator.'); 
                });
			},
			getDocumentName: function(documentId){
                return $http.get('/api/documents/documents/', {params:{ documentId : documentId }}).then(
                    function(response){   
                    return response.data[0].name  
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Borrower Name. Please contact System Administrator.'); 
                });
			},
			getDocumentIdBySubProcess: function(subProcessName){
                return $http.get('/api/documents/documents/', {params:{ subProcessName : subProcessName }}).then(
                    function(response){   
                    return response.data[0].documentType
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Document Type. Please contact System Administrator.'); 
                });
            },
			getCurrentUser: function() {
				var values = JSON.parse(localStorage.getItem('currentUser'));
				return values['id'];
			},
			getCurrentUserInfo: function() {
				var values = JSON.parse(localStorage.getItem('currentUser'));
				return $http.get('/api/users/users/', { params: { id : values['id'] } }).then(
					function(response) {
						return response.data[0];
					},
					function(error) {
						toastr.error(
							'Error ' + error.status + error.statusText,
							'Could not retrieve current user information. Please contact System Administrator.'
						);
					}
				);
			},
			getContentTypeId: function(model) {
				return $http.get('/api/users/contenttype/', { params: { model: model } }).then(
					function(response) {
						return response.data[0].id;
					},
					function(error) {
						toastr.error(
							'Error ' + error.status + error.statusText,
							'Could not retrieve Content Type Id. Please contact System Administrator.'
						);
					}
				);
			},
			getGenders: function(){
                return $http.get('/api/settings/gendertype/').then(
                    function(response){   
                    return response.data;     
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Gender list. Please contact System Administrator.'); 
                });     
			},
			getCooperativeType: function(){
                return $http.get('/api/settings/cooperativetype/').then(
                    function(response){   
                    return response.data;     
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Cooperative Type list. Please contact System Administrator.'); 
                });     
			},
			getCommittee: function(){
                return $http.get('/api/committees/committees/').then(
                    function(response){   
                    return response.data;     
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Committee list. Please contact System Administrator.'); 
                });     
			},
			getLastActivity: function(documentId){
                return $http.get('/api/documents/documentmovements/',{params:{ process : 'last', documentId: documentId }}).then(
                    function(response){
					console.log(response.data);
                    return response.data;     
                },
                function(error){
                    toastr.error('Error '+ error.status + error.statusText, 'Could not retrieve Last Activity list. Please contact System Administrator.'); 
                });     
            },
			getTimeRemaining: function(endtime, starttime) {
				var t = Date.parse(endtime) - Date.parse(starttime);
				var seconds = Math.floor((t / 1000) % 60);
				var minutes = Math.floor((t / 1000 / 60) % 60);
				var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
				var days = Math.floor(t / (1000 * 60 * 60 * 24));
				var wholedays = Math.ceil(t / (1000 * 60 * 60 * 24));
				return {
					total: t,
					days: days,
					hours: hours,
					minutes: minutes,
					seconds: seconds,
					wholedays: wholedays
				};
			},
			dateWithoutTime: function(date, format) {
				return $filter('date')(date, format);
			},
			flattenJSON: function(array) {
				var flatten = function(object) {
					var newObj = {};
					for (var key in object) {
						var item = object[key];
						if (typeof item !== 'object') {
							newObj[key] = item;
						} else {
							var flattened = flatten(item);
							for (var k in flattened) {
								newObj[k] = flattened[k];
							}
						}
					}
					return newObj;
				};

				var flattenArray = function(array) {
					var newArray = [];
					array.forEach(function(object) {
						newArray.push(flatten(object));
					});
					return newArray;
				};

				return flattenArray(array);
			},
			convertCamelCase: function(camelCase) {
				return camelCase
					.replace(/([A-Z])/g, function($1) {
						return ' ' + $1.toUpperCase();
					})
					.replace(/^./, function(str) {
						return str.toUpperCase();
					});
			},
			slugify: function(text) {
				var slug = text.toLowerCase().trim();
				slug = slug.replace(/[^a-z0-9\s-]/g, ' ');
				slug = slug.replace(/[\s-]+/g, '-');
				return slug;
			},
			unSlugify: function(text) {
				var unslug = text.toLowerCase();
				unslug = unslug.split('-');
				unslug = unslug.map((i) => i[0].toUpperCase() + i.substr(1));
				unslug = unslug.join(' ');
				return unslug;
			},
			generateUniqueID: function(length, quantity) {
				var charSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
				var charSetSize = charSet.length;
				var idCount = quantity;
				var charCount = length;
				var generatedIds = [];

				var generateRandomId = function() {
					var id = '';
					for (var i = 1; i <= charCount; i++) {
						var randPos = Math.floor(Math.random() * charSetSize);
						id += charSet[randPos];
					}
					return id;
				};

				while (generatedIds.length < idCount) {
					var id = generateRandomId();
					if ($.inArray(id, generatedIds) == -1) {
						generatedIds.push(id);
					}
				}

				return generatedIds;
			}
		};
	});

});
