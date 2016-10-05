'use strict';

module.exports = function(grunt) {
    require('load-grunt-tasks')(grunt);
    grunt.file.defaultEncoding = 'utf-8';
    var frontend = {
        src: './source',
        target: 'app'
    };
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        frontend: frontend,
        sass: {
            dist: {
                options: {
                    require: ['<%= frontend.src %>/sass/checkversion.rb'],
                  //  style: 'compressed'
                },
                files: {
                    '<%= frontend.target %>/style.css': '<%= frontend.src %>/sass/style.sass',
                }
            }
        },
        spritepacker: {
            options: {
                baseUrl: '',
                evenPixels: true
            },
            default_options: {
                options: {
                  template: '<%= frontend.src %>/sass/sprite/tpl/sprite.tpl',
                  destCss: '<%= frontend.src %>/sass/sprite/sprite.sass',
                  padding: 10
                },
                files: {
                  '<%= frontend.target %>/assets/efx/sprite.png': ['<%= frontend.src %>/sprite/*.png']
                }
            }
        },
        jade: {
            options: {
                pretty: true,
                data: function(dest, src) {
                    return require('./config.json');
                }
            },
            compile: {
                files: [{
                    expand: true,
                    cwd: '<%= frontend.src %>/jade/',
                    src: ['index.jade'],
                    dest: '<%= frontend.target %>',
                    ext: '.html'
                }]
            }
        },
        clean: {
            release: [
                '<%= frontend.target %>/*.css',
                '<%= frontend.target %>/assets/js/*.js',
                '<%= frontend.target %>/*.html',
                '<%= frontend.target %>/assets/efx/*.png',
                '<%= frontend.target %>/assets/img/*'
            ]
        },
        copy: {
            app: {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        src: ['<%= frontend.src %>/js/*.js',
                            '<%= frontend.src %>/js/controllers/*.js', '<%= frontend.src %>/js/services/*.js'],
                        dest: '<%= frontend.target %>/raw_assets/js/'
                    },
                    {
                        expand: true,
                        flatten: true,
                        src: ['<%= frontend.src %>/img/*'],
                        dest: '<%= frontend.target %>/assets/img/'
                    },
                    {
                        expand: true,
                        flatten: true,
                        src: ['<%= frontend.src %>/js/vendor/*.js'],
                        dest: '<%= frontend.target %>/raw_assets/js/vendor'
                    }
                ]
            },
            minjs: {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        src: ['<%= frontend.src %>/vendor/**/*.min.js*'],
                        dest: '<%= frontend.target %>/raw_assets/js/vendor/'
                    }
                ]
            },
            devjs: {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        src: ['<%= frontend.src %>/vendor/**/*.js*'],
                        dest: '<%= frontend.target %>/raw_assets/js/vendor/'
                    }
                ]
            }
        },
        replace: {
            javascript: {
                options: {
                    patterns: [
                        {
                            json: grunt.file.readJSON('./config.json')
                        }
                    ]
                },
                files: [
                    {src: '<%= frontend.src %>/js/app.js', dest: '<%= frontend.target %>/raw_assets/js/app.js'}
                ]
            }
        },
        autoprefixer: {
            dist: {
                files: {
                    '<%= frontend.target %>/style.css': ['<%= frontend.target %>/style.css'],
                }
            }
        },
        useminPrepare: {
            html: [
                '<%= frontend.target %>/index.html'
            ],
            css: ['<%= frontend.target %>/style.css'],
            options: {
                dest: '<%= frontend.target %>',
            }
        },
        filerev: {
            options: {
                encoding: 'utf8',
                algorithm: 'md5',
                length: 8
            },
            dist: {
                files: [{
                    src: [
                        '<%= frontend.target %>/assets/js/*.js',
                        '<%= frontend.target %>/*.css',
                        '<%= frontend.target %>/assets/efx/*.png'
                    ]
                }]
            }
        },
        usemin: {
            html: [
                '<%= frontend.target %>/index.html'
            ],
            css: ['<%= frontend.target %>/style.*.css']
        },
        watch: {
            sass: {
                files: ['<%= frontend.src %>/sass/**/*.sass'],
                tasks: ['sass:dist', 'autoprefixer']
            },
            jade: {
                files: ['<%= frontend.src %>/jade/**/*.jade'],
                tasks: ['jade']
            },
            javascript: {
                files: ['<%= frontend.src %>/js/**/*.js', '<%= frontend.src %>/img/**/*'],
                tasks: ['copy:wake', 'replace']
            },
            vendor: {
                files: ['<%= frontend.src %>/vendor/**/*'],
                tasks: ['copy:vendorjs']
            },
            sprites: {
                files: ['<%= frontend.src %>/efx/**/*'],
                tasks: ['spritepacker']
            },
            options: {
                livereload: true,
                livereloadOnError: false
            }
        }
    });
    grunt.registerTask('dev', [
        'spritepacker', 'jade', 'sass', 'autoprefixer', 'copy', 'replace'
    ]);
    grunt.registerTask('sprite', ['spritepacker']);
    grunt.registerTask('build', [
        'clean', 'spritepacker', 'jade', 'sass', 'autoprefixer', 'useminPrepare', 'copy', 'replace', 'concat', 'uglify', 'filerev', 'usemin'
    ]);

};
