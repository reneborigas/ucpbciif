angular
    .module('app')
    .directive('includeReplace', includeReplace)
    .directive('a', preventClickDirective)
    .directive('a', bootstrapCollapseDirective)
    .directive('a', navigationDirective)
    .directive('button', layoutToggleDirective)
    .directive('a', layoutToggleDirective)
    .directive('button', collapseMenuTogglerDirective)
    .directive('div', bootstrapCarouselDirective)
    .directive('toggle', bootstrapTooltipsPopoversDirective)
    .directive('tab', bootstrapTabsDirective)
    .directive('button', cardCollapseDirective)
    .directive('button', minimizeMenuTogglerDirective)
    .directive('selectNgFiles', selectNgFiles)
    .directive('price', price)
    .directive('pagination', pagination);

function includeReplace() {
    var directive = {
        require: 'ngInclude',
        restrict: 'A',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        element.replaceWith(element.children());
    }
}

//Prevent click if href="#"
function preventClickDirective() {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        if (attrs.href === '#') {
            element.on('click', function (event) {
                event.preventDefault();
            });
        }
    }
}

//Bootstrap Collapse
function bootstrapCollapseDirective() {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        if (attrs.toggle == 'collapse') {
            element.attr('href', 'javascript;;').attr('data-target', attrs.href.replace('base.html', ''));
        }
    }
}

/**
 * @desc Genesis main navigation - Siedebar menu
 * @example <li class="nav-item nav-dropdown"></li>
 */
function navigationDirective() {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        if (element.hasClass('nav-dropdown-toggle') && angular.element('body').width() > 782) {
            element.on('click', function () {
                if (!angular.element('body').hasClass('compact-nav')) {
                    element.parent().toggleClass('open').find('.open').removeClass('open');
                }
            });
        } else if (element.hasClass('nav-dropdown-toggle') && angular.element('body').width() < 783) {
            element.on('click', function () {
                element.parent().toggleClass('open').find('.open').removeClass('open');
            });
        }
    }
}

//Dynamic resize .sidebar-nav
sidebarNavDynamicResizeDirective.$inject = ['$window', '$timeout'];
function sidebarNavDynamicResizeDirective($window, $timeout) {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        if (element.hasClass('sidebar-nav') && angular.element('body').hasClass('fixed-nav')) {
            var bodyHeight = angular.element(window).height();
            scope.$watch(function () {
                var headerHeight = angular.element('header').outerHeight();

                if (angular.element('body').hasClass('sidebar-off-canvas')) {
                    element.css('height', bodyHeight);
                } else {
                    element.css('height', bodyHeight - headerHeight);
                }
            });

            angular.element($window).bind('resize', function () {
                var bodyHeight = angular.element(window).height();
                var headerHeight = angular.element('header').outerHeight();
                var sidebarHeaderHeight = angular.element('.sidebar-header').outerHeight();
                var sidebarFooterHeight = angular.element('.sidebar-footer').outerHeight();

                if (angular.element('body').hasClass('sidebar-off-canvas')) {
                    element.css('height', bodyHeight - sidebarHeaderHeight - sidebarFooterHeight);
                } else {
                    element.css('height', bodyHeight - headerHeight - sidebarHeaderHeight - sidebarFooterHeight);
                }
            });
        }
    }
}

//LayoutToggle
layoutToggleDirective.$inject = ['$interval'];
function layoutToggleDirective($interval) {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        element.on('click', function () {
            if (element.hasClass('sidebar-toggler')) {
                angular.element('body').toggleClass('sidebar-hidden');
            }

            if (element.hasClass('aside-menu-toggler')) {
                angular.element('body').toggleClass('aside-menu-hidden');
            }
        });
    }
}

//Collapse menu toggler
function collapseMenuTogglerDirective() {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        element.on('click', function () {
            if (element.hasClass('navbar-toggler') && !element.hasClass('layout-toggler')) {
                angular.element('body').toggleClass('sidebar-mobile-show');
            }
        });
    }
}

//Collapse menu toggler
function minimizeMenuTogglerDirective() {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        element.on('click', function () {
            if (element.hasClass('navbar-toggler') && element.hasClass('sidebar-minimizer')) {
                angular.element('body').toggleClass('sidebar-minimized brand-minimized');
            }
        });
    }
}

//Bootstrap Carousel
function bootstrapCarouselDirective() {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        if (attrs.ride == 'carousel') {
            element.find('a').each(function () {
                $(this).attr('data-target', $(this).attr('href').replace('base.html', '')).attr('href', 'javascript;;');
            });
        }
    }
}

//Bootstrap Tooltips & Popovers
function bootstrapTooltipsPopoversDirective() {
    var directive = {
        restrict: 'A',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        if (attrs.toggle == 'tooltip') {
            angular.element(element).tooltip();
        }
        if (attrs.toggle == 'popover') {
            angular.element(element).popover();
        }
    }
}

//Bootstrap Tabs
function bootstrapTabsDirective() {
    var directive = {
        restrict: 'A',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        element.click(function (e) {
            e.preventDefault();
            angular.element(element).tab('show');
        });
    }
}

//Card Collapse
function cardCollapseDirective() {
    var directive = {
        restrict: 'E',
        link: link,
    };
    return directive;

    function link(scope, element, attrs) {
        if (attrs.toggle == 'collapse' && element.parent().hasClass('card-actions')) {
            if (element.parent().parent().parent().find('.card-body').hasClass('in')) {
                element.find('i').addClass('r180');
            }

            var id = 'collapse-' + Math.floor(Math.random() * 1000000000 + 1);
            element.attr('data-target', '#' + id);
            element.parent().parent().parent().find('.card-body').attr('id', id);

            element.on('click', function () {
                element.find('i').toggleClass('r180');
            });
        }
    }
}

//Card Collapse
function selectNgFiles($parse) {
    var directive = {
        require: 'ngModel',
        link: link,
    };
    return directive;

    function link(scope, elem, attrs, ngModel) {
        elem.on('change', function (e) {
            var files = elem[0].files;
            ngModel.$setViewValue(files);
        });
    }
}

price.$inject = ['$filter'];
function price($filter) {
    var directive = {
        require: 'ngModel',
        link: link,
    };
    return directive;

    function link(scope, elem, attrs, ngModelCtrl) {
        ngModelCtrl.$formatters.push(function (modelValue) {
            return setDisplayNumber(modelValue, true);
        });

        ngModelCtrl.$parsers.push(function (viewValue) {
            setDisplayNumber(viewValue);
            return setModelNumber(viewValue);
        });

        elem.bind('keyup focus', function () {
            setDisplayNumber(elem.val());
        });

        function setDisplayNumber(val, formatter) {
            var valStr, displayValue;

            if (typeof val === 'undefined') {
                return 0;
            }

            valStr = val.toString();
            displayValue = valStr.replace(/,/g, '').replace(/[A-Za-z]/g, '');
            displayValue = parseFloat(displayValue);
            displayValue = !isNaN(displayValue) ? displayValue.toString() : '';

            // handle leading character -/0
            if (valStr.length === 1 && valStr[0] === '-') {
                displayValue = valStr[0];
            } else if (valStr.length === 1 && valStr[0] === '0') {
                displayValue = '';
            } else {
                displayValue = $filter('number')(displayValue);
            }

            // handle decimal
            if (!attrs.integer) {
                if (displayValue.indexOf('.') === -1) {
                    if (valStr.slice(-1) === '.') {
                        displayValue += '.';
                    } else if (valStr.slice(-2) === '.0') {
                        displayValue += '.0';
                    } else if (valStr.slice(-3) === '.00') {
                        displayValue += '.00';
                    }
                } // handle last character 0 after decimal and another number
                else {
                    if (valStr.slice(-1) === '0') {
                        displayValue += '0';
                    }
                }
            }

            if (attrs.positive && displayValue[0] === '-') {
                displayValue = displayValue.substring(1);
            }

            if (typeof formatter !== 'undefined') {
                return displayValue === '' ? 0 : displayValue;
            } else {
                elem.val(displayValue === '0' ? '' : displayValue);
            }
        }

        function setModelNumber(val) {
            var modelNum = val
                .toString()
                .replace(/,/g, '')
                .replace(/[A-Za-z]/g, '');
            modelNum = parseFloat(modelNum);
            modelNum = !isNaN(modelNum) ? modelNum : 0;
            if (modelNum.toString().indexOf('.') !== -1) {
                modelNum = Math.round((modelNum + 0.00001) * 100) / 100;
            }
            if (attrs.positive) {
                modelNum = Math.abs(modelNum);
            }
            return modelNum;
        }
    }
}

function pagination() {
    var directive = {
        restrict: 'E',
        transclude: 'true',
        link: link,
        templateUrl: 'statics/partials/customs/pagination-directive.html',
        scope: {
            data: '=',
            pageSize: '=',
            currentPage: '=currentpage',
        },
    };
    return directive;

    function link(scope, element, attrs) {
        scope.currentPage = 0;

        scope.pageRange = function () {
            var pages = [];
            var range = Math.ceil(scope.data.length / scope.pageSize);
            for (var i = 1; i <= range; i++) {
                pages.push(i);
            }
            return pages;
        };

        scope.gotoPrev = function () {
            scope.currentPage--;
        };

        scope.gotoNext = function () {
            scope.currentPage++;
        };

        scope.jumpToPage = function (n) {
            scope.currentPage = n - 1;
        };

        scope.atStart = function () {
            return scope.currentPage === 0;
        };

        scope.atEnd = function () {
            return scope.currentPage >= scope.data.length / scope.pageSize - 1;
        };
    }
}
