angular
    .module('app')
    .config(['$stateProvider', '$urlRouterProvider', '$ocLazyLoadProvider', '$breadcrumbProvider', function ($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $breadcrumbProvider) {
        $stateProvider
            .state('app.icons', {
                url: "/icons",
                abstract: true,
                template: '<ui-view></ui-view>',
                ncyBreadcrumb: {
                    label: 'Icons'
                }
            })
            .state('app.icons.flags', {
                url: '/flags',
                templateUrl: '/statics/html/views/icons/flags.html',
                ncyBreadcrumb: {
                    label: 'Flags'
                }
            })
            .state('app.icons.fontawesome', {
                url: '/font-awesome',
                templateUrl: '/statics/html/views/icons/font-awesome.html',
                ncyBreadcrumb: {
                    label: 'Font Awesome'
                }
            })
            .state('app.icons.simplelineicons', {
                url: '/simple-line-icons',
                templateUrl: '/statics/html/views/icons/simple-line-icons.html',
                ncyBreadcrumb: {
                    label: 'Simple Line Icons'
                }
            })
            .state('app.components', {
                url: "/components",
                abstract: true,
                template: '<ui-view></ui-view>',
                ncyBreadcrumb: {
                    label: 'Components'
                }
            })
            .state('app.components.buttons', {
                url: '/buttons',
                templateUrl: '/statics/html/views/components/buttons.html',
                ncyBreadcrumb: {
                    label: 'Buttons'
                }
            })
            .state('app.components.social-buttons', {
                url: '/social-buttons',
                templateUrl: '/statics/html/views/components/social-buttons.html',
                ncyBreadcrumb: {
                    label: 'Social Buttons'
                }
            })
            .state('app.components.cards', {
                url: '/cards',
                templateUrl: '/statics/html/views/components/cards.html',
                ncyBreadcrumb: {
                    label: 'Cards'
                }
            })
            .state('app.components.forms', {
                url: '/forms',
                templateUrl: '/statics/html/views/components/forms.html',
                ncyBreadcrumb: {
                    label: 'Forms'
                }
            })
            .state('app.components.switches', {
                url: '/switches',
                templateUrl: '/statics/html/views/components/switches.html',
                ncyBreadcrumb: {
                    label: 'Switches'
                }
            })
            .state('app.components.tables', {
                url: '/tables',
                templateUrl: '/statics/html/views/components/tables.html',
                ncyBreadcrumb: {
                    label: 'Tables'
                }
            })
            .state('app.widgets', {
                url: '/widgets',
                templateUrl: '/statics/html/views/widgets.html',
                ncyBreadcrumb: {
                    label: 'Widgets'
                },
                resolve: {
                    loadMyCtrl: ['$ocLazyLoad', function ($ocLazyLoad) {
                        // you can lazy load controllers
                        return $ocLazyLoad.load({
                            files: ['js/controllers/widgets.js']
                        });
                    }]
                }
            })
            .state('app.charts', {
                url: '/charts',
                templateUrl: '/statics/html/views/charts.html',
                ncyBreadcrumb: {
                    label: 'Charts'
                },
                resolve: {
                    // Plugins loaded before
                    // loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
                    //     return $ocLazyLoad.load([
                    //         {
                    //             serial: true,
                    //             files: ['js/libs/Chart.min.js', 'js/libs/angular-chart.min.js']
                    //         }
                    //     ]);
                    // }],
                    loadMyCtrl: ['$ocLazyLoad', function ($ocLazyLoad) {
                        // you can lazy load files for an existing module
                        return $ocLazyLoad.load({
                            files: ['js/controllers/charts.js']
                        });
                    }]
                }
            })
            .state('app.borrowers', {
                url: '/borrowers',
                templateUrl: '/statics/html/views/widgets.html',
                ncyBreadcrumb: {
                    label: 'Widgets'
                },
                resolve: {
                    loadMyCtrl: ['$ocLazyLoad', function ($ocLazyLoad) {
                        // you can lazy load controllers
                        return $ocLazyLoad.load({
                            files: ['js/controllers/widgets.js']
                        });
                    }]
                }
            })
    }]);
