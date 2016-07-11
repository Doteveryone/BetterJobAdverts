module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    copy: {
      target: {
        files: [
          {
            expand: true,
            cwd: 'jobcert/assets/javascript',
            src: ['*.js'], 
            dest: 'jobcert/static/javascript', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'jobcert/assets/vendor/foundation-sites/dist',
            src: ['**/*.js'], 
            dest: 'jobcert/static/vendor/foundation-sites', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'jobcert/assets/vendor/jquery/dist',
            src: ['**/*.js'], 
            dest: 'jobcert/static/vendor/jquery', 
            filter: 'isFile'
          },
          {
            expand: true,
            cwd: 'jobcert/assets/vendor/html5shiv/dist',
            src: ['**/*.js'], 
            dest: 'jobcert/static/vendor/html5shiv', 
            filter: 'isFile'
          }
        ]
      }
    },
    sass: {
      options: {
        loadPath: ['jobcert/assets/vendor/foundation-sites/scss']
      },
      dist: {
        files: {
          'jobcert/static/css/main.css' : 'jobcert/assets/sass/main.scss'
        }
      }
    },
    watch: {
      css: {
        files: '**/*.scss',
        tasks: ['sass']
      },
      scripts: {
        files: 'jobcert/assets/**/*.js',
        tasks: ['copy']
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.registerTask('default',['watch']);
}