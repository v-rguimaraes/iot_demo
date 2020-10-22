module.exports = async function (context, req) {
    context.log('Demo criada pelo CTA team para simulação de dispositivos');

    let qtde=0;

    if(req.query.meupedelaranjalima) {
       qtde = parseInt(req.query.meupedelaranjalima);
        if (qtde > 1000){
            qtde = 100
        }
    }



    const azure = require("azure");

    let responseMessage = "";

    const serviceBusService = azure.createServiceBusService();

    var sensors = [];
    var messageShadow;
    var sensorId = await genSensorId();
    

    for(j=0;j<qtde;j++){
        messageShadow = {body: 'leitura shadow',customProperties: {id: sensorId,temperatura: tempRandom()}};
        sensors.push(messageShadow)
        serviceBusService.sendQueueMessage('from_devices', sensors[j], function(error){
            if(!error){
                // message sent
            }
        });
    }
   
    context.res = {
        status: 200, 
        body: `Serão geradas ${qtde} mensagens para o Sensor ID [${sensorId}] - Verifique a Fila`
    };
}

function tempRandom() {
    const min = Math.ceil(18);
    const max = Math.floor(40);
    let temperatura = Math.floor(Math.random() * (max - min + 1)) + min;
    return temperatura;
}

async function genSensorId(){
  const crypto = require("crypto");
  const strSensor = 'id-'+crypto.randomBytes(10).toString('hex');
  return strSensor;
}