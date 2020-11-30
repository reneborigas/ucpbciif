define(function () {
    'use strict';

    var app = angular.module('app');

    app.factory('appFactory', function ($http, toastr, $filter) {
        return {
            getBranches: function () {
                return $http.get('/api/borrowers/branches/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Branch List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getTitleType: function () {
                return $http.get('/api/settings/titletype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Title Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getGenderType: function () {
                return $http.get('/api/settings/gendertype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Gender Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCountryList: function () {
                return $http.get('/api/settings/countries/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Countries List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCivilStatusType: function () {
                return $http.get('/api/settings/civilstatustype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve CivilStatus Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getIdentificationType: function () {
                return $http.get('/api/settings/identificationtype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Identification Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getIDType: function () {
                return $http.get('/api/settings/idtype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve ID Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getOwnerLesseeType: function () {
                return $http.get('/api/settings/houseownerlessee/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Owner Lessee Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getAddressType: function () {
                return $http.get('/api/settings/addresstype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Address Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getContactType: function () {
                return $http.get('/api/settings/contacttype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Contact Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getPSICType: function () {
                return $http.get('/api/settings/psic/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve PSIC Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getPSOCType: function () {
                return $http.get('/api/settings/psoc/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve PSOC Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getIncomePeriodType: function () {
                return $http.get('/api/settings/incomeperiod/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Income Period Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCurrencyList: function () {
                return $http.get('/api/settings/currencies/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Currency List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getOccupationStatusType: function () {
                return $http.get('/api/settings/occupationstatustype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Occupation Status Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getLegalFormType: function () {
                return $http.get('/api/settings/legalformtype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Legal Form Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getFirmSizeType: function () {
                return $http.get('/api/settings/firmsizetype/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Firm Size Type List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getNotifications: function (userId, committeeId) {
                return $http.get('/api/notifications/notifications/', { params: { userId: userId, committeeId: committeeId } }).then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Notifications. Please contact System Administrator.'
                        );
                    }
                );
            },
            getNotes: function (object_id, content_type) {
                return $http.get('/api/committees/notes/', { params: { object_id: object_id, content_type: content_type } }).then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Borrower Name. Please contact System Administrator.'
                        );
                    }
                );
            },
            getBorrowerName: function (borrowerId) {
                return $http.get('/api/borrowers/borrowers/', { params: { borrowerId: borrowerId } }).then(
                    function (response) {
                        return response.data[0].borrowerName;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Borrower Name. Please contact System Administrator.'
                        );
                    }
                );
            },
            checkPermissions: function (subProcessId) {
                return $http.post('/api/processes/checkpermission/', { subProcessId: subProcessId }).then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not checking permissions Please contact System Administrator.'
                        );
                    }
                );
            },
            getLoanNumber: function (documentId) {
                return $http.get('/api/documents/documents/', { params: { documentId: documentId } }).then(
                    function (response) {
                        return response.data[0].name;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Borrower Name. Please contact System Administrator.'
                        );
                    }
                );
            },
            getDocumentName: function (documentId) {
                return $http.get('/api/documents/documents/', { params: { documentId: documentId } }).then(
                    function (response) {
                        return response.data[0].name;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Borrower Name. Please contact System Administrator.'
                        );
                    }
                );
            },
            getOfficeId: function (officeName) {
                return $http.get('/api/committees/offices/', { params: { officeName: officeName } }).then(
                    function (response) {
                        return response.data[0].id;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Office ID. Please contact System Administrator.'
                        );
                    }
                );
            },
            getSubProcessId: function (subProcessName) {
                return $http.get('/api/processes/subprocesses/', { params: { subProcessName: subProcessName } }).then(
                    function (response) {
                        return response.data[0].id;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Document Sub Process ID. Please contact System Administrator.'
                        );
                    }
                );
            },
            getSubProcessByName: function (subProcessName) {
                return $http.get('/api/processes/subprocesses/', { params: { subProcessName: subProcessName } }).then(
                    function (response) {
                        return response.data[0];
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Document Sub Process ID. Please contact System Administrator.'
                        );
                    }
                );
            },
            getSubProcess: function (subProcessId) {
                return $http.get('/api/processes/subprocesses/', { params: { subProcessId: subProcessId } }).then(
                    function (response) {
                        return response.data[0];
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Sub Process. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCreditLine: function (creditLineId) {
                return $http.get('/api/loans/creditlines/', { params: { creditLineId: creditLineId } }).then(
                    function (response) {
                        return response.data[0];
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Credit Line. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCreditLineStatus: function () {
                return $http.get('/api/loans/status/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Credit Line Status list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCheckStatuses: function () {
                return $http.get('/api/payments/checkstatuses/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Check Status list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getLoan: function (loanId) {
                return $http.get('/api/loans/loans/', { params: { loanId: loanId } }).then(
                    function (response) {
                        return response.data[0];
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Loan. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCurrentUser: function () {
                var values = JSON.parse(localStorage.getItem('currentUser'));
                return values['id'];
            },
            getCurrentUserInfo: function () {
                var values = JSON.parse(localStorage.getItem('currentUser'));
                return $http.get('/api/users/users/', { params: { id: values['id'] } }).then(
                    function (response) {
                        return response.data[0];
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve current user information. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCurrentUserApps: function () {
                var values = JSON.parse(localStorage.getItem('currentUser'));
                return $http.get('/api/users/userapps/', { params: { user: values['id'] } }).then(
                    function (response) {
                        return response.data[0].installedApps;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve App List. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCurrentUserAppPermission: function (app) {
                var values = JSON.parse(localStorage.getItem('currentUser'));
                return $http.get('/api/users/userapps/', { params: { user: values['id'] } }).then(
                    function (response) {
                        return $filter('filter')(response.data[0].installedApps, { name: app });
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve App List Permitted. Please contact System Administrator.'
                        );
                    }
                );
            },
            getUserAccountTypeID: function (accountType) {
                return $http.get('/api/users/accounttype/', { params: { account_type: accountType } }).then(
                    function (response) {
                        return response.data[0].id;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve User Account types. Please contact System Administrator.'
                        );
                    }
                );
            },
            getContentTypeId: function (model) {
                return $http.get('/api/users/contenttype/', { params: { model: model } }).then(
                    function (response) {
                        return response.data[0].id;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Content Type Id. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCommittee: function () {
                return $http.get('/api/committees/committees/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Committee list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getPaymentStatus: function () {
                return $http.get('/api/payments/paymentstatus/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Payment Status list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getPaymentType: function () {
                return $http.get('/api/payments/paymenttypes/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Payment Type list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getAmortizationStatus: function () {
                return $http.get('/api/loans/amortizationstatus/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Amortization Status list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getTermName: function (termId) {
                return $http.get('/api/loans/terms/', { params: { termId: termId } }).then(
                    function (response) {
                        return response.data[0].name;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Term Information. Please contact System Administrator.'
                        );
                    }
                );
            },
            getCommitteeName: function (committeeId) {
                return $http.get('/api/committees/committees/', { params: { committeeId: committeeId } }).then(
                    function (response) {
                        return response.data[0].committeeName;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Committee Information. Please contact System Administrator.'
                        );
                    }
                );
            },
            getLoanTerms: function () {
                return $http.get('/api/loans/terms/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Term list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getInterestRates: function () {
                return $http.get('/api/loans/interestrates/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Interest Rate list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getLoanProgramsByid: function (borrowerId) {
                return $http.get('/api/loans/loanprograms/', { params: { borrowerId: borrowerId } }).then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Loan Program list. Please contact System Administrator.'
                        );
                    }
                );
            },

            getDocumenFileName: function (code) {
                return $http.post('/api/documents/getdocumentfilename/', { code: code }).then(
                    function (response) {
                        return response.data.fileName;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Documents list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getLoanPrograms: function (borrowerId) {
                return $http.get('/api/loans/loanprograms/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Loan Program list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getLoanStatus: function () {
                return $http.get('/api/loans/loanstatus/').then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Loan Status list. Please contact System Administrator.'
                        );
                    }
                );
            },
            recalculatePMT: function (params) {
                console.log(params);
                return $http.get('/api/loans/loanprograms/', { params: { borrowerId: borrowerId } }).then(
                    function (response) {
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Loan Program list. Please contact System Administrator.'
                        );
                    }
                );
            },

            getLastActivity: function (documentId) {
                return $http.get('/api/documents/documentmovements/', { params: { process: 'last', documentId: documentId } }).then(
                    function (response) {
                        console.log(response.data);
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Last Activity list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getActivities: function (documentId) {
                return $http.get('/api/documents/documentmovements/', { params: { documentId: documentId } }).then(
                    function (response) {
                        console.log(response.data);
                        return response.data;
                    },
                    function (error) {
                        toastr.error(
                            'Error ' + error.status + ' ' + error.statusText,
                            'Could not retrieve Last Activity list. Please contact System Administrator.'
                        );
                    }
                );
            },
            getTimeRemaining: function (endtime, starttime) {
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
                    wholedays: wholedays,
                };
            },
            trimString: function (string, length) {
                return string.length > length ? string.substring(0, length) + '...' : string;
            },
            trimStringWithExtension: function (string, length) {
                var ext = string.split('.').pop();
                return string.length > length ? string.substring(0, length) + '...' + ext : string;
            },
            dateWithoutTime: function (date, format) {
                return $filter('date')(date, format);
            },
            flattenJSON: function (array) {
                var flatten = function (object) {
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

                var flattenArray = function (array) {
                    var newArray = [];
                    array.forEach(function (object) {
                        newArray.push(flatten(object));
                    });
                    return newArray;
                };

                return flattenArray(array);
            },
            convertCamelCase: function (camelCase) {
                return camelCase
                    .replace(/([A-Z])/g, function ($1) {
                        return ' ' + $1.toUpperCase();
                    })
                    .replace(/^./, function (str) {
                        return str.toUpperCase();
                    });
            },
            convertSnakeCase: function (snakeCase) {
                return snakeCase
                    .replace(/([_])/g, function ($1) {
                        return ' ';
                    })
                    .replace(/\s[a-z]/g, function ($1) {
                        return $1.toUpperCase();
                    })
                    .replace(/^./, function (str) {
                        return str.toUpperCase();
                    });
            },
            normalizeString: function (string) {
                return string
                    .replace(/([A-Z])/g, function ($1) {
                        return ' ' + $1.toUpperCase();
                    })
                    .replace(/([_])/g, function ($1) {
                        return ' ';
                    })
                    .replace(/\s[a-z]/g, function ($1) {
                        return $1.toUpperCase();
                    })
                    .replace(/^./, function (str) {
                        return str.toUpperCase();
                    });
            },
            slugify: function (text) {
                var slug = text.toLowerCase().trim();
                slug = slug.replace(/[^a-z0-9\s-]/g, ' ');
                slug = slug.replace(/[\s-]+/g, '-');
                return slug;
            },
            unSlugify: function (text) {
                var unslug = text.toLowerCase();
                unslug = unslug.split('-');
                unslug = unslug.map((i) => i[0].toUpperCase() + i.substr(1));
                unslug = unslug.join(' ');
                return unslug;
            },
            generateUniqueID: function (length, quantity) {
                var charSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
                t;
                var charSetSize = charSet.length;
                var idCount = quantity;
                var charCount = length;
                var generatedIds = [];

                var generateRandomId = function () {
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
            },
            convertAmountToWords: function (s) {
                var myappthos = ['', 'Thousand', 'Million', 'Billion', 'Trillion'];
                var myappdang = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'];
                var myapptenth = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
                var myapptvew = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];

                s = s.toString();
                s = s.replace(/[\, ]/g, '');
                if (s != parseFloat(s)) return 'not a number';
                var query = s.indexOf('.');
                if (query == -1) query = s.length;
                if (query > 15) return 'too big';
                var n = s.split('');
                var str = '';
                var mjk = 0;
                for (var ld = 0; ld < query; ld++) {
                    if ((query - ld) % 3 == 2) {
                        if (n[ld] == '1') {
                            str += myapptenth[Number(n[ld + 1])] + ' ';
                            ld++;
                            mjk = 1;
                        } else if (n[ld] != 0) {
                            str += myapptvew[n[ld] - 2] + ' ';
                            mjk = 1;
                        }
                    } else if (n[ld] != 0) {
                        str += myappdang[n[ld]] + ' ';
                        if ((query - ld) % 3 == 0) str += 'hundred ';
                        mjk = 1;
                    }
                    if ((query - ld) % 3 == 1) {
                        if (mjk) str += myappthos[(query - ld - 1) / 3] + ' ';
                        mjk = 0;
                    }
                }
                if (query != s.length) {
                    var dv = s.length;
                    str += 'and ';
                    for (var ld = query + 1; ld < dv; ld++) str += myappdang[n[ld]] + ' ';
                }
                return str.replace(/\s+/g, ' ');
            },
        };
    });

    app.factory('Excel', function ($window) {
        var uri = 'data:application/vnd.ms-excel;base64;,',
            template =
                '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><meta http-equiv="content-type" content="application/vnd.ms-excel; charset=UTF-8"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>',
            base64 = function (s) {
                return $window.btoa(unescape(encodeURIComponent(s)));
            },
            format = function (s, c) {
                return s.replace(/{(\w+)}/g, function (m, p) {
                    return c[p];
                });
            };
        return {
            tableToExcel: function (tableId, worksheetName) {
                var table = $(tableId),
                    ctx = { worksheet: worksheetName || 'Worksheet', table: table.html() },
                    href = uri + base64(format(template, ctx));
                return href;
            },
        };
    });
});
