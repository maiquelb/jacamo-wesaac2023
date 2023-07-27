package devices;

import cartago.*;

public class HVAC extends Artifact {

	private TemperatureSensorPanel sensorPanel;

	private double temperature;
	//private double preferredTemperature;

	void init(int temp) {
		this.temperature = temp; // initial simulated value
		//this.preferredTemperature = prefTemp;
		defineObsProperty("state","idle");
		defineObsProperty("temperature",temperature);
 		//defineObsProperty("preferred_temperature",preferredTemperature);

		//sensorPanel = new TemperatureSensorPanel(this,temp);
		//sensorPanel.setVisible(true);
	}

	@OPERATION void startHeating(){
		if (!getObsProperty("state").stringValue().equals("heating")) {
			System.out.println("heating...");
			getObsProperty("state").updateValue("heating");
			this.execInternalOp("updateTemperatureProc",1);
	  }
	}

	@OPERATION void startCooling(){
		if (!getObsProperty("state").stringValue().equals("cooling")) {
			System.out.println("cooling...");
			getObsProperty("state").updateValue("cooling");
			this.execInternalOp("updateTemperatureProc",-1);
		}
	}

	@OPERATION void stopAirConditioner() {
		System.out.println("stop!");
		getObsProperty("state").updateValue("idle");
	}

	@INTERNAL_OPERATION void updateTemperatureProc(int step){
		ObsProperty prop = getObsProperty("temperature");
		while (!getObsProperty("state").stringValue().equals("idle")){
			double temp = prop.doubleValue();
			prop.updateValue(temp+step);
			//sensorPanel.setTempValue((int)(Math.round(temp+step)));
			System.out.println("temp = "+(int)(Math.round(temp+step)));
			this.await_time(100);
		}
	}

	void notifyNewTemperature(double value){
		ObsProperty prop = getObsProperty("temperature");
		prop.updateValue(value);
	}


	// allows to change the value using REST
	@OPERATION public void doUpdateObsProperty(String obName, Object arg) {
        ObsProperty op = getObsProperty(obName);
        if (op == null) {
            defineObsProperty(obName, arg);
        } else {
            op.updateValues(arg);
        }
        System.out.println("update ob "+obName+"("+arg+")");
    }

}
