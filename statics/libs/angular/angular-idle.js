/*** Directives and services for responding to idle users in AngularJS
 * @author Mike Grabski <me@mikegrabski.com>
 * @version v1.3.2
 * @link https://github.com/HackedByChinese/ng-idle.git
 * @license MIT
 */

!(function (a, b, c) {
    'use strict';
    b.module('ngIdle', ['ngIdle.keepalive', 'ngIdle.idle', 'ngIdle.countdown', 'ngIdle.title', 'ngIdle.localStorage']),
        b.module('ngIdle.keepalive', []).provider('Keepalive', function () {
            var a = { http: null, interval: 600 };
            this.http = function (c) {
                if (!c)
                    throw new Error(
                        'Argument must be a string containing a URL, or an object containing the HTTP request configuration.'
                    );
                b.isString(c) && (c = { url: c, method: 'GET' }), (c.cache = !1), (a.http = c);
            };
            var c = (this.interval = function (b) {
                if (((b = parseInt(b)), isNaN(b) || 0 >= b))
                    throw new Error('Interval must be expressed in seconds and be greater than 0.');
                a.interval = b;
            });
            this.$get = [
                '$rootScope',
                '$log',
                '$interval',
                '$http',
                function (d, e, f, g) {
                    function h(a) {
                        d.$broadcast('KeepaliveResponse', a.data, a.status);
                    }
                    function i() {
                        d.$broadcast('Keepalive'), b.isObject(a.http) && g(a.http).then(h)['catch'](h);
                    }
                    var j = { ping: null };
                    return {
                        _options: function () {
                            return a;
                        },
                        setInterval: c,
                        start: function () {
                            return f.cancel(j.ping), (j.ping = f(i, 1e3 * a.interval)), j.ping;
                        },
                        stop: function () {
                            f.cancel(j.ping);
                        },
                        ping: function () {
                            i();
                        },
                    };
                },
            ];
        }),
        b.module('ngIdle.idle', ['ngIdle.keepalive', 'ngIdle.localStorage']).provider('Idle', function () {
            var a = {
                    idle: 1200,
                    timeout: 30,
                    autoResume: 'idle',
                    interrupt: 'mousemove keydown DOMMouseScroll mousewheel mousedown touchstart touchmove scroll',
                    windowInterrupt: null,
                    keepalive: !0,
                },
                c = (this.timeout = function (c) {
                    if (c === !1) a.timeout = 0;
                    else {
                        if (!(b.isNumber(c) && c >= 0))
                            throw new Error(
                                'Timeout must be zero or false to disable the feature, or a positive integer (in seconds) to enable it.'
                            );
                        a.timeout = c;
                    }
                });
            (this.interrupt = function (b) {
                a.interrupt = b;
            }),
                (this.windowInterrupt = function (b) {
                    a.windowInterrupt = b;
                });
            var d = (this.idle = function (b) {
                if (0 >= b) throw new Error('Idle must be a value in seconds, greater than 0.');
                a.idle = b;
            });
            (this.autoResume = function (b) {
                b === !0 ? (a.autoResume = 'idle') : b === !1 ? (a.autoResume = 'off') : (a.autoResume = b);
            }),
                (this.keepalive = function (b) {
                    a.keepalive = b === !0;
                }),
                (this.$get = [
                    '$interval',
                    '$log',
                    '$rootScope',
                    '$document',
                    'Keepalive',
                    'IdleLocalStorage',
                    '$window',
                    function (e, f, g, h, i, j, k) {
                        function l() {
                            a.keepalive && (u.running && i.ping(), i.start());
                        }
                        function m() {
                            a.keepalive && i.stop();
                        }
                        function n() {
                            u.idling = !u.idling;
                            var b = u.idling ? 'IdleStart' : 'IdleEnd';
                            u.idling
                                ? (g.$broadcast(b),
                                  m(),
                                  a.timeout && ((u.countdown = a.timeout), o(), (u.timeout = e(o, 1e3, a.timeout, !1))))
                                : (l(), g.$broadcast(b)),
                                e.cancel(u.idle);
                        }
                        function o() {
                            if (u.idling) {
                                if (u.countdown <= 0) return void q();
                                g.$broadcast('IdleWarn', u.countdown), u.countdown--;
                            }
                        }
                        function p(a) {
                            g.$broadcast('IdleInterrupt', a);
                        }
                        function q() {
                            m(),
                                e.cancel(u.idle),
                                e.cancel(u.timeout),
                                (u.idling = !0),
                                (u.running = !1),
                                (u.countdown = 0),
                                g.$broadcast('IdleTimeout');
                        }
                        function r(a, b, c) {
                            var d = a.running();
                            a.unwatch(), b(c), d && a.watch();
                        }
                        function s() {
                            var a = j.get('expiry');
                            return a && a.time ? new Date(a.time) : null;
                        }
                        function t(a) {
                            a ? j.set('expiry', { id: v, time: a }) : j.remove('expiry');
                        }
                        var u = { idle: null, timeout: null, idling: !1, running: !1, countdown: null },
                            v = new Date().getTime(),
                            w = {
                                _options: function () {
                                    return a;
                                },
                                _getNow: function () {
                                    return new Date();
                                },
                                getIdle: function () {
                                    return a.idle;
                                },
                                getTimeout: function () {
                                    return a.timeout;
                                },
                                setIdle: function (a) {
                                    r(this, d, a);
                                },
                                setTimeout: function (a) {
                                    r(this, c, a);
                                },
                                isExpired: function () {
                                    var a = s();
                                    return null !== a && a <= this._getNow();
                                },
                                running: function () {
                                    return u.running;
                                },
                                idling: function () {
                                    return u.idling;
                                },
                                watch: function (b) {
                                    e.cancel(u.idle), e.cancel(u.timeout);
                                    var c = a.timeout ? a.timeout : 0;
                                    b || t(new Date(new Date().getTime() + 1e3 * (a.idle + c))),
                                        u.idling ? n() : u.running || l(),
                                        (u.running = !0),
                                        (u.idle = e(n, 1e3 * a.idle, 0, !1));
                                },
                                unwatch: function () {
                                    e.cancel(u.idle),
                                        e.cancel(u.timeout),
                                        (u.idling = !1),
                                        (u.running = !1),
                                        t(null),
                                        m();
                                },
                                interrupt: function (b) {
                                    if (u.running) {
                                        if (a.timeout && this.isExpired()) return void q();
                                        p(b),
                                            (b ||
                                                'idle' === a.autoResume ||
                                                ('notIdle' === a.autoResume && !u.idling)) &&
                                                this.watch(b);
                                    }
                                },
                            },
                            x = {
                                clientX: null,
                                clientY: null,
                                swap: function (a) {
                                    var b = { clientX: this.clientX, clientY: this.clientY };
                                    return (this.clientX = a.clientX), (this.clientY = a.clientY), b;
                                },
                                hasMoved: function (a) {
                                    var b = this.swap(a);
                                    return null === this.clientX || a.movementX || a.movementY
                                        ? !0
                                        : b.clientX != a.clientX || b.clientY != a.clientY
                                        ? !0
                                        : !1;
                                },
                            };
                        if (
                            (h.find('html').on(a.interrupt, function (a) {
                                ('mousemove' === a.type &&
                                    a.originalEvent &&
                                    0 === a.originalEvent.movementX &&
                                    0 === a.originalEvent.movementY) ||
                                    (('mousemove' !== a.type || x.hasMoved(a)) && w.interrupt());
                            }),
                            a.windowInterrupt)
                        )
                            for (
                                var y = a.windowInterrupt.split(' '),
                                    z = function () {
                                        w.interrupt();
                                    },
                                    A = 0;
                                A < y.length;
                                A++
                            )
                                k.addEventListener
                                    ? (k.addEventListener(y[A], z, !1),
                                      g.$on('$destroy', function () {
                                          k.removeEventListener(y[A], z, !1);
                                      }))
                                    : (k.attachEvent(y[A], z),
                                      g.$on('$destroy', function () {
                                          k.detachEvent(y[A], z);
                                      }));
                        var B = function (a) {
                            if ('ngIdle.expiry' === a.key && a.newValue && a.newValue !== a.oldValue) {
                                var c = b.fromJson(a.newValue);
                                if (c.id === v) return;
                                w.interrupt(!0);
                            }
                        };
                        return (
                            k.addEventListener
                                ? (k.addEventListener('storage', B, !1),
                                  g.$on('$destroy', function () {
                                      k.removeEventListener('storage', B, !1);
                                  }))
                                : k.attachEvent &&
                                  (k.attachEvent('onstorage', B),
                                  g.$on('$destroy', function () {
                                      k.detachEvent('onstorage', B);
                                  })),
                            w
                        );
                    },
                ]);
        }),
        b.module('ngIdle.countdown', ['ngIdle.idle']).directive('idleCountdown', [
            'Idle',
            function (a) {
                return {
                    restrict: 'A',
                    scope: { value: '=idleCountdown' },
                    link: function (b) {
                        (b.value = a.getTimeout()),
                            b.$on('IdleWarn', function (a, c) {
                                b.$evalAsync(function () {
                                    b.value = c;
                                });
                            }),
                            b.$on('IdleTimeout', function () {
                                b.$evalAsync(function () {
                                    b.value = 0;
                                });
                            });
                    },
                };
            },
        ]),
        b
            .module('ngIdle.title', [])
            .provider('Title', function () {
                function a(a, b, c) {
                    return new Array(b - String(a).length + 1).join(c || '0') + a;
                }
                var c = { enabled: !0 },
                    d = (this.enabled = function (a) {
                        c.enabled = a === !0;
                    });
                this.$get = [
                    '$document',
                    '$interpolate',
                    function (e, f) {
                        var g = {
                            original: null,
                            idle: '{{minutes}}:{{seconds}} until your session times out!',
                            timedout: 'Your session has expired.',
                        };
                        return {
                            setEnabled: d,
                            isEnabled: function () {
                                return c.enabled;
                            },
                            original: function (a) {
                                return b.isUndefined(a) ? g.original : void (g.original = a);
                            },
                            store: function (a) {
                                (a || !g.original) && (g.original = this.value());
                            },
                            value: function (a) {
                                return b.isUndefined(a) ? e[0].title : void (e[0].title = a);
                            },
                            idleMessage: function (a) {
                                return b.isUndefined(a) ? g.idle : void (g.idle = a);
                            },
                            timedOutMessage: function (a) {
                                return b.isUndefined(a) ? g.timedout : void (g.timedout = a);
                            },
                            setAsIdle: function (b) {
                                this.store();
                                var c = { totalSeconds: b };
                                (c.minutes = Math.floor(b / 60)),
                                    (c.seconds = a(b - 60 * c.minutes, 2)),
                                    this.value(f(this.idleMessage())(c));
                            },
                            setAsTimedOut: function () {
                                this.store(), this.value(this.timedOutMessage());
                            },
                            restore: function () {
                                this.original() && this.value(this.original());
                            },
                        };
                    },
                ];
            })
            .directive('title', [
                'Title',
                function (a) {
                    return {
                        restrict: 'E',
                        link: function (b, c, d) {
                            a.isEnabled() &&
                                !d.idleDisabled &&
                                (a.store(!0),
                                b.$on('IdleStart', function () {
                                    a.original(c[0].innerText);
                                }),
                                b.$on('IdleWarn', function (b, c) {
                                    a.setAsIdle(c);
                                }),
                                b.$on('IdleEnd', function () {
                                    a.restore();
                                }),
                                b.$on('IdleTimeout', function () {
                                    a.setAsTimedOut();
                                }));
                        },
                    };
                },
            ]),
        b
            .module('ngIdle.localStorage', [])
            .service('IdleStorageAccessor', [
                '$window',
                function (a) {
                    return {
                        get: function () {
                            return a.localStorage;
                        },
                    };
                },
            ])
            .service('IdleLocalStorage', [
                'IdleStorageAccessor',
                function (a) {
                    function d() {
                        var a = {};
                        (this.setItem = function (b, c) {
                            a[b] = c;
                        }),
                            (this.getItem = function (b) {
                                return 'undefined' != typeof a[b] ? a[b] : null;
                            }),
                            (this.removeItem = function (b) {
                                a[b] = c;
                            });
                    }
                    function e() {
                        try {
                            var b = a.get();
                            return b.setItem('ngIdleStorage', ''), b.removeItem('ngIdleStorage'), b;
                        } catch (c) {
                            return new d();
                        }
                    }
                    var f = e();
                    return {
                        set: function (a, c) {
                            f.setItem('ngIdle.' + a, b.toJson(c));
                        },
                        get: function (a) {
                            return b.fromJson(f.getItem('ngIdle.' + a));
                        },
                        remove: function (a) {
                            f.removeItem('ngIdle.' + a);
                        },
                        _wrapped: function () {
                            return f;
                        },
                    };
                },
            ]);
})(window, window.angular);
//# sourceMappingURL=angular-idle.map
