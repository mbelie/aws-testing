// Run npm install for both aws libraries
// Run browserify on this file (eg: browserify index.js -o bundle.js)
// TODO MB 02/03/20: Minimize the bundle size

var Mqtt = require('./mqtt.js');
var _mqtt = new Mqtt();

// Arbitrary topic name
const Topic = "3669";

var log = function(app, message){
    app.messages.unshift(message.trim());
}

var app = new Vue({
  el: '#vueApp',
  data: {
    messages: [],
    isConnected: false,
    duration: 5000
  },
  mounted: function(){
    this.connect();
  },
  methods: {
    connect: function(){
         log(this, "Connecting...");
        _mqtt.connect(
            () => {
                log(this, "Connected");
                this.isConnected = true;
                _mqtt.subscribe(Topic);
            }, 
            () => 
            {
                log(this, "Reconnected");
                this.isConnected = true;
                _mqtt.subscribe(Topic);
            },
            (message) => log(this, message));
    },
    publish: function(seconds){
        if(!this.isConnected)
            return;

        if(seconds != null)
          this.duration = seconds;

        _mqtt.publish(Topic, "{\"duration\": " + this.duration + "}");
    }
  }
});