var _aws = require('aws-sdk');
var _awsIoTData = require('aws-iot-device-sdk');
var _awsConfiguration = require('./aws-configuration.js');

var Mqtt = function(){
   var _connectHandler;
   var _reconnectHandler;
   var _messageHandler;

   var _clientId = 'mqtt-explorer-' + (Math.floor((Math.random() * 100000) + 1));

   _aws.config.region = _awsConfiguration.region;

   _aws.config.credentials = new _aws.CognitoIdentityCredentials({
      IdentityPoolId: _awsConfiguration.poolId
   });

   const _mqttClient = _awsIoTData.device({
      region: _aws.config.region,
      host: _awsConfiguration.host,
      clientId: _clientId,
      protocol: 'wss',
      maximumReconnectTimeMs: 8000,
      debug: true,
      // The following 3 have to be initialied with empty strings
      accessKeyId: '',
      secretKey: '',
      sessionToken: ''
   });

   var log = function(message){
      console.log(message);
   }

   var connectHandler = function() {
      log('Connnected');
      if(_connectHandler != null)
         _connectHandler();
   };

   var reconnectHandler = function() {
      log('Reconnected')
      if(_reconnectHandler != null)
         _reconnectHandler();
   };

   var messageHandler = function(topic, payload) {
      var message = topic + ':' + payload.toString();
      log(message);
      if(_messageHandler != null)
         _messageHandler(message);
   };

   _mqttClient.on('connect', connectHandler);
   _mqttClient.on('reconnect', reconnectHandler);
   _mqttClient.on('message', messageHandler);  

   this.connect = function(connectHandler, reconnectHandler, messageHandler){
      _connectHandler = connectHandler;
      _reconnectHandler = reconnectHandler;
      _messageHandler = messageHandler;

      var cognitoIdentity = new _aws.CognitoIdentity();
      _aws.config.credentials.get(function(error, data) {
         if (!error) {
            log('Retrieved identity: ' + _aws.config.credentials.identityId);
            var params = {
               IdentityId: _aws.config.credentials.identityId
            };
            
            cognitoIdentity.getCredentialsForIdentity(params, function(error, data) {
               if (!error) {
                  _mqttClient.updateWebSocketCredentials(
                        data.Credentials.AccessKeyId,
                        data.Credentials.SecretKey,
                        data.Credentials.SessionToken);
               } else {
                  log('Error retrieving credentials: ' + error);            
               }
            });
         } else {
            log('Error retrieving identity: ' + error);
         }
      });
   }

   this.subscribe = function(topic){
      _mqttClient.subscribe(topic);   
   }

   this.unsubscribe = function(topic){
      _mqttClient.unsubscribe(topic);   
   }

   this.publish = function(topic, message){
      _mqttClient.publish(topic, message);   
   }
};

module.exports = Mqtt;