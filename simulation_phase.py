from pycarmaker import CarMaker, Quantity
import time 
import math
import matplotlib.pyplot as plt

# 1 - Open CarMaker with option -cmdport
'''
    For example: on a Windows system with CarMaker 8.0.2 installed on the default
    folder send the command C:\IPG\carmaker\win64-11.1.2\bin\CM.exe -cmdport 16660
'''
# 3 - Initialize pyCarMaker


def main():
    IP_ADDRESS = "localhost"
    PORT = 16660
    cm = CarMaker(IP_ADDRESS, PORT)

    # 4 - Connect to CarMaker
    cm.connect()

    # 5 - Subscribe to vehicle speed
    # Create a Quantity instance for vehicle speed (vehicle speed is a float type variable)

    #建立感知数据字典
    sensed_data = {
        'CurrentRoute': {
            'Point_x':[],
            'Point_y':[],
            'Point_z':[]
        },
        'EgoPos': [],           #x,y,z
        'EgoSpeed': [],         #x,y
        'EgoAcc':[],            #x,y
        'ControStatus':{
            'SteeringAngle':[],     #Ang,AngVel,AngAcc,Trq
            'BrakePadel': -1,
            'GasPadel':-1
        },
        'LaneMarking':{
            'Time':-1,
            'L1':{
                'Type': -1,
                'Height': -1,
                'Width': -1,
                'ID': -1,
                'Point_x' : [],
                'Point_y' : [],
                'Point_z' : []
            },
            'L2':{
                'Type': -1,
                'Height': -1,
                'Width': -1,
                'ID': -1,
                'Point_x' : [],
                'Point_y' : [],
                'Point_z' : []
            },
            'R1':{
                'Type': -1,
                'Height': -1,
                'Width': -1,
                'ID': -1,
                'Point_x' : [],
                'Point_y' : [],
                'Point_z' : []
            },
            'R2':{
                'Type': -1,
                'Height': -1,
                'Width': -1,
                'ID': -1,
                'Point_x' : [],
                'Point_y' : [],
                'Point_z' : []
            },
            'Stopline': []
        },
        'TrafficLight':{
            'Existance': -1,
            'Color': -1,
            'IsValid': 1,
            'Position': []
        },
        'SpeedLimit':{
            'Value': -1,
            'Position': []
        },
        'VehicleObjects': {         #传感器仅检测自车当前车道最近车辆的质心相对于传感器的位置与速度
            'Position': [],
            'Velocity': []
        }           
    }

    #生成Quantities
    #road sensor
    roadsensor_num = 10
    roadsensor_x_quan = []
    roadsensor_y_quan = []
    roadsensor_z_quan = []

    for i in range(4,4+roadsensor_num):
        roadsensor_x_quan.append(Quantity('Sensor.Road.VehSensor_'+str(i)+'.Path.tx',Quantity.FLOAT))
        roadsensor_y_quan.append(Quantity('Sensor.Road.VehSensor_'+str(i)+'.Path.ty',Quantity.FLOAT))
        roadsensor_z_quan.append(Quantity('Sensor.Road.VehSensor_'+str(i)+'.Path.tz',Quantity.FLOAT))

    #ego car information
    egopos_x = Quantity('Car.tx',Quantity.FLOAT)
    egopos_y = Quantity('Car.ty',Quantity.FLOAT)
    egopos_z = Quantity('Car.tz',Quantity.FLOAT)

    egospeed_x =Quantity('Car.vx',Quantity.FLOAT)
    egospeed_y =Quantity('Car.vy',Quantity.FLOAT)

    egoacc_x = Quantity('Car.ax',Quantity.FLOAT)
    egoacc_y = Quantity('Car.ay',Quantity.FLOAT)

    steer_ang = Quantity('DM.Steer.Ang',Quantity.FLOAT)
    steer_angvel = Quantity('DM.Steer.AngVel',Quantity.FLOAT)
    steer_angacc = Quantity('DM.Steer.AngAcc',Quantity.FLOAT)
    steer_trq = Quantity('DM.Steer.Trq',Quantity.FLOAT)

    brake_padel = Quantity('DM.Brake',Quantity.FLOAT)
    gas_padel = Quantity('DM.Gas',Quantity.FLOAT)

    #line sensor
    timestamp = Quantity('Sensor.Line.VehSensor_0.TimeStamp',Quantity.FLOAT)
    #左一
    l1_type = Quantity('Sensor.Line.VehSensor_0.LLines.1.Type',Quantity.FLOAT)
    l1_height = Quantity('Sensor.Line.VehSensor_0.LLines.1.Height',Quantity.FLOAT)
    l1_width = Quantity('Sensor.Line.VehSensor_0.LLines.1.Width',Quantity.FLOAT)
    l1_id = Quantity('Sensor.Line.VehSensor_0.LLines.1.Id',Quantity.FLOAT)
    #左二
    l2_type = Quantity('Sensor.Line.VehSensor_0.LLines.2.Type',Quantity.FLOAT)
    l2_height = Quantity('Sensor.Line.VehSensor_0.LLines.2.Height',Quantity.FLOAT)
    l2_width = Quantity('Sensor.Line.VehSensor_0.LLines.2.Width',Quantity.FLOAT)
    l2_id = Quantity('Sensor.Line.VehSensor_0.LLines.2.Id',Quantity.FLOAT)
    #右一
    r1_type = Quantity('Sensor.Line.VehSensor_0.RLines.1.Type',Quantity.FLOAT)
    r1_height = Quantity('Sensor.Line.VehSensor_0.RLines.1.Height',Quantity.FLOAT)
    r1_width = Quantity('Sensor.Line.VehSensor_0.RLines.1.Width',Quantity.FLOAT)
    r1_id = Quantity('Sensor.Line.VehSensor_0.RLines.1.Id',Quantity.FLOAT)
    #右二
    r2_type = Quantity('Sensor.Line.VehSensor_0.RLines.2.Type',Quantity.FLOAT)
    r2_height = Quantity('Sensor.Line.VehSensor_0.RLines.2.Height',Quantity.FLOAT)
    r2_width = Quantity('Sensor.Line.VehSensor_0.RLines.2.Width',Quantity.FLOAT)
    r2_id = Quantity('Sensor.Line.VehSensor_0.RLines.2.Id',Quantity.FLOAT)
    #车道线 点信息
    point_num = 100

    Lline1_x_quan = []
    Lline1_y_quan = []
    Lline1_z_quan = []

    Lline2_x_quan = []
    Lline2_y_quan = []
    Lline2_z_quan = []

    Rline1_x_quan = []
    Rline1_y_quan = []
    Rline1_z_quan = []

    Rline2_x_quan = []
    Rline2_y_quan = []
    Rline2_z_quan = []

    for i in range(point_num):
        Lline1_x_quan.append(Quantity('LineL1_p'+str(i+1)+'_x',Quantity.FLOAT))
        Lline1_y_quan.append(Quantity('LineL1_p'+str(i+1)+'_y',Quantity.FLOAT))
        Lline1_z_quan.append(Quantity('LineL1_p'+str(i+1)+'_z',Quantity.FLOAT))

        Lline2_x_quan.append(Quantity('LineL2_p'+str(i+1)+'_x',Quantity.FLOAT))
        Lline2_y_quan.append(Quantity('LineL2_p'+str(i+1)+'_y',Quantity.FLOAT))
        Lline2_z_quan.append(Quantity('LineL2_p'+str(i+1)+'_z',Quantity.FLOAT))

        Rline1_x_quan.append(Quantity('LineR1_p'+str(i+1)+'_x',Quantity.FLOAT))
        Rline1_y_quan.append(Quantity('LineR1_p'+str(i+1)+'_y',Quantity.FLOAT))
        Rline1_z_quan.append(Quantity('LineR1_p'+str(i+1)+'_z',Quantity.FLOAT))

        Rline2_x_quan.append(Quantity('LineR2_p'+str(i+1)+'_x',Quantity.FLOAT))
        Rline2_y_quan.append(Quantity('LineR2_p'+str(i+1)+'_y',Quantity.FLOAT))
        Rline2_z_quan.append(Quantity('LineR2_p'+str(i+1)+'_z',Quantity.FLOAT))

    #camera sensor for trafficlight
    obj_num = 10
    light_state = []
    for i in range(obj_num):
        light_state.append(Quantity('Sensor.Camera.VehSensor_1.Obj.'+str(i)+'.LightState',Quantity.FLOAT))

    #traffic sign sensor for trafficlight
    trafficlight_d_x = Quantity('Sensor.TSign.VehSensor_2.TrafficLight.0.ds.x',Quantity.FLOAT)
    trafficlight_d_y = Quantity('Sensor.TSign.VehSensor_2.TrafficLight.0.ds.y',Quantity.FLOAT)
    trafficlight_d_z = Quantity('Sensor.TSign.VehSensor_2.TrafficLight.0.ds.z',Quantity.FLOAT)

    #traffic sign sensor for speedlimit
    speedlimit_d_x = Quantity('Sensor.TSign.VehSensor_2.SpeedLimit.0.ds.x',Quantity.FLOAT)
    speedlimit_d_y = Quantity('Sensor.TSign.VehSensor_2.SpeedLimit.0.ds.y',Quantity.FLOAT)
    speedlimit_d_z = Quantity('Sensor.TSign.VehSensor_2.SpeedLimit.0.ds.z',Quantity.FLOAT)
    speedlimit_val = Quantity('Sensor.TSign.VehSensor_2.SpeedLimit.0.Main.val0',Quantity.FLOAT)

    #object sensor
    vehicleob_d_x = Quantity('Sensor.Object.VehSensor_3.relvTgt.RefPnt.ds.x',Quantity.FLOAT)
    vehicleob_d_y = Quantity('Sensor.Object.VehSensor_3.relvTgt.RefPnt.ds.y',Quantity.FLOAT)
    vehicleob_d_z = Quantity('Sensor.Object.VehSensor_3.relvTgt.RefPnt.ds.z',Quantity.FLOAT)

    vehicleob_v_x = Quantity('Sensor.Object.VehSensor_3.relvTgt.RefPnt.dv.x',Quantity.FLOAT)
    vehicleob_v_y = Quantity('Sensor.Object.VehSensor_3.relvTgt.RefPnt.dv.y',Quantity.FLOAT)
    vehicleob_v_z = Quantity('Sensor.Object.VehSensor_3.relvTgt.RefPnt.dv.z',Quantity.FLOAT)

    #traffic sign sensor for stopline
    stopline_x = Quantity('Sensor.TSign.VehSensor_2.Stop.0.ds.x',Quantity.FLOAT)
    stopline_y = Quantity('Sensor.TSign.VehSensor_2.Stop.0.ds.y',Quantity.FLOAT)
    stopline_z = Quantity('Sensor.TSign.VehSensor_2.Stop.0.ds.z',Quantity.FLOAT)


    #初始化quantities
    #road sensor
    for i in range(roadsensor_num):
        roadsensor_x_quan[i].data = -1
        roadsensor_y_quan[i].data = -1
        roadsensor_z_quan[i].data = -1

    #ego car information
    egopos_x.data = -1
    egopos_y.data = -1
    egopos_z.data = -1

    egospeed_x.data = -1
    egospeed_y.data = -1 

    egoacc_x.data = -1
    egoacc_y.data = -1

    steer_ang.data = -1
    steer_angvel.data = -1
    steer_angacc.data = -1
    steer_trq.data = -1

    brake_padel.data = -1
    gas_padel.data = -1

    #line sensor
    timestamp.data = -1 
    #左一
    l1_type.data = -1 
    l1_height.data = -1 
    l1_width.data = -1 
    l1_id.data = -1 
    #左二
    l2_type.data = -1 
    l2_height.data = -1 
    l2_width.data = -1 
    l2_id.data = -1 
    #右一
    r1_type.data = -1 
    r1_height.data = -1 
    r1_width.data = -1 
    r1_id.data = -1 
    #右二
    r2_type.data = -1 
    r2_height.data = -1 
    r2_width.data = -1 
    r2_id.data = -1 

    for i in range(point_num):
        Lline1_x_quan[i].data = -1
        Lline1_y_quan[i].data = -1
        Lline1_z_quan[i].data = -1

        Lline2_x_quan[i].data = -1
        Lline2_y_quan[i].data = -1
        Lline2_z_quan[i].data = -1

        Rline1_x_quan[i].data = -1
        Rline1_y_quan[i].data = -1
        Rline1_z_quan[i].data = -1

        Rline2_x_quan[i].data = -1
        Rline2_y_quan[i].data = -1
        Rline2_z_quan[i].data = -1

    #camera sensor for trafficlight
    for i in range(obj_num):
        light_state[i].data = -1

    #traffic sign sensor for trafficlight
    trafficlight_d_x.data = -1
    trafficlight_d_y.data = -1
    trafficlight_d_z.data = -1

    #traffic sign sensor for speedlimit
    speedlimit_d_x.data = -1
    speedlimit_d_y.data = -1
    speedlimit_d_z.data = -1
    speedlimit_val.data = -1

    #object sensor
    vehicleob_d_x.data = -1
    vehicleob_d_y.data = -1 
    vehicleob_d_z.data = -1

    vehicleob_v_x.data = -1
    vehicleob_v_y.data = -1
    vehicleob_v_z.data = -1

    #traffic sign sensor for stopline
    stopline_x.data = -1
    stopline_y.data = -1
    stopline_z.data = -1



    #订阅quantities
    #road sensor
    for i in range(roadsensor_num):
        cm.subscribe(roadsensor_x_quan[i])
        cm.subscribe(roadsensor_y_quan[i])
        cm.subscribe(roadsensor_z_quan[i])

    #ego car information
    cm.subscribe(egopos_x)
    cm.subscribe(egopos_y)
    cm.subscribe(egopos_z)

    cm.subscribe(egospeed_x)
    cm.subscribe(egospeed_y)

    cm.subscribe(egoacc_x)
    cm.subscribe(egoacc_x)

    cm.subscribe(steer_ang)
    cm.subscribe(steer_angvel)
    cm.subscribe(steer_angacc)
    cm.subscribe(steer_trq)

    cm.subscribe(brake_padel)
    cm.subscribe(gas_padel)

    #line sensor
    cm.subscribe(timestamp)
    #左一
    cm.subscribe(l1_type)
    cm.subscribe(l1_height)
    cm.subscribe(l1_width)
    cm.subscribe(l1_id)
    #左二
    cm.subscribe(l2_type)
    cm.subscribe(l2_height)
    cm.subscribe(l2_width)
    cm.subscribe(l2_id)
    #右一
    cm.subscribe(r1_type)
    cm.subscribe(r1_height)
    cm.subscribe(r1_width)
    cm.subscribe(r1_id)
    #右二
    cm.subscribe(r2_type)
    cm.subscribe(r2_height)
    cm.subscribe(r2_width)
    cm.subscribe(r2_id)

    for i in range(point_num):
        cm.subscribe(Lline1_x_quan[i])
        cm.subscribe(Lline1_y_quan[i])
        cm.subscribe(Lline1_z_quan[i])

        cm.subscribe(Lline2_x_quan[i])
        cm.subscribe(Lline2_y_quan[i])
        cm.subscribe(Lline2_z_quan[i])

        cm.subscribe(Rline1_x_quan[i])
        cm.subscribe(Rline1_y_quan[i])
        cm.subscribe(Rline1_z_quan[i])

        cm.subscribe(Rline2_x_quan[i])
        cm.subscribe(Rline2_y_quan[i])
        cm.subscribe(Rline2_z_quan[i])

    #camera sensor
    for i in range(obj_num):
        cm.subscribe(light_state[i])

    #traffic sign sensor for trafficlight
    cm.subscribe(trafficlight_d_x)
    cm.subscribe(trafficlight_d_y)
    cm.subscribe(trafficlight_d_z)

    #traffic sign sensor for speedlimit
    cm.subscribe(speedlimit_d_x)
    cm.subscribe(speedlimit_d_y)
    cm.subscribe(speedlimit_d_z)
    cm.subscribe(speedlimit_val)

    #object sensor
    cm.subscribe(vehicleob_d_x)
    cm.subscribe(vehicleob_d_y)
    cm.subscribe(vehicleob_d_z)

    cm.subscribe(vehicleob_v_x)
    cm.subscribe(vehicleob_v_y)
    cm.subscribe(vehicleob_v_z)

    #traffic sign sensor for stopline
    cm.subscribe(stopline_x)
    cm.subscribe(stopline_y)
    cm.subscribe(stopline_z)


    # 6 - Read all subscribed quantities. In this example, vehicle speed and simulation status
    # For some reason, the first two reads will be incomplete and must be ignored
    # You will see 2 log errors like this: [ ERROR]   CarMaker: Wrong read
    cm.read()
    cm.read()
    time.sleep(0.1)
    c=0
    while(1):
        cm.read()

        for i in range(roadsensor_num):
            sensed_data['CurrentRoute']['Point_x'].append(roadsensor_x_quan[i].data)
            sensed_data['CurrentRoute']['Point_y'].append(roadsensor_y_quan[i].data)
            sensed_data['CurrentRoute']['Point_z'].append(roadsensor_z_quan[i].data)

        sensed_data['EgoPos'].append(egopos_x.data)
        sensed_data['EgoPos'].append(egopos_y.data)
        sensed_data['EgoPos'].append(egopos_z.data)

        sensed_data['EgoSpeed'].append(egospeed_x.data)
        sensed_data['EgoSpeed'].append(egospeed_y.data)

        sensed_data['EgoAcc'].append(egoacc_x.data)
        sensed_data['EgoAcc'].append(egoacc_y.data)

        sensed_data['ControStatus']['SteeringAngle'].append(steer_ang.data)
        sensed_data['ControStatus']['SteeringAngle'].append(steer_angvel.data)
        sensed_data['ControStatus']['SteeringAngle'].append(steer_angacc.data)
        sensed_data['ControStatus']['SteeringAngle'].append(steer_trq.data)

        sensed_data['ControStatus']['BrakePadel'] = brake_padel.data
        sensed_data['ControStatus']['GasPadel'] = gas_padel.data

        sensed_data['LaneMarking']['Time'] = timestamp.data
        sensed_data['LaneMarking']['L1']['Type'] = l1_type.data
        sensed_data['LaneMarking']['L1']['Height'] = l1_height.data
        sensed_data['LaneMarking']['L1']['Width'] = l1_width.data
        sensed_data['LaneMarking']['L1']['ID'] = l1_id.data

        sensed_data['LaneMarking']['L2']['Type'] = l2_type.data
        sensed_data['LaneMarking']['L2']['Height'] = l2_height.data
        sensed_data['LaneMarking']['L2']['Width'] = l2_width.data
        sensed_data['LaneMarking']['L2']['ID'] = l2_id.data

        sensed_data['LaneMarking']['R1']['Type'] = r1_type.data
        sensed_data['LaneMarking']['R1']['Height'] = r1_height.data
        sensed_data['LaneMarking']['R1']['Width'] = r1_width.data
        sensed_data['LaneMarking']['R1']['ID'] = r1_id.data

        sensed_data['LaneMarking']['R2']['Type'] = r2_type.data
        sensed_data['LaneMarking']['R2']['Height'] = r2_height.data
        sensed_data['LaneMarking']['R2']['Width'] = r2_width.data
        sensed_data['LaneMarking']['R2']['ID'] = r2_id.data

        for i in range(point_num):
            sensed_data['LaneMarking']['L1']['Point_x'].append(Lline1_x_quan[i].data)
            sensed_data['LaneMarking']['L1']['Point_y'].append(Lline1_y_quan[i].data)
            sensed_data['LaneMarking']['L1']['Point_z'].append(Lline1_z_quan[i].data)
            
            sensed_data['LaneMarking']['L2']['Point_x'].append(Lline2_x_quan[i].data)
            sensed_data['LaneMarking']['L2']['Point_y'].append(Lline2_y_quan[i].data)
            sensed_data['LaneMarking']['L2']['Point_z'].append(Lline2_z_quan[i].data)

            sensed_data['LaneMarking']['R1']['Point_x'].append(Rline1_x_quan[i].data)
            sensed_data['LaneMarking']['R1']['Point_y'].append(Rline1_y_quan[i].data)
            sensed_data['LaneMarking']['R1']['Point_z'].append(Rline1_z_quan[i].data)

            sensed_data['LaneMarking']['R2']['Point_x'].append(Rline2_x_quan[i].data)
            sensed_data['LaneMarking']['R2']['Point_y'].append(Rline2_y_quan[i].data)
            sensed_data['LaneMarking']['R2']['Point_z'].append(Rline2_z_quan[i].data)

        sensed_data['LaneMarking']['Stopline'].append(stopline_x.data)
        sensed_data['LaneMarking']['Stopline'].append(stopline_y.data)
        sensed_data['LaneMarking']['Stopline'].append(stopline_z.data)
    
        sensed_data['TrafficLight']['Existance'] = 0
        sensed_data['TrafficLight']['Color'] = 0
        for i in range(obj_num):
            if light_state[i].data > 0:
                sensed_data['TrafficLight']['Existance'] = 1
                if light_state[i].data == 1:
                    sensed_data['TrafficLight']['Color'] = 1
                elif light_state[i].data > 1:
                    sensed_data['TrafficLight']['Color'] = 0
                break

        sensed_data['TrafficLight']['IsValid'] = 1

        sensed_data['TrafficLight']['Position'].append(trafficlight_d_x.data)
        sensed_data['TrafficLight']['Position'].append(trafficlight_d_y.data)
        sensed_data['TrafficLight']['Position'].append(trafficlight_d_z.data)

        sensed_data['SpeedLimit']['Position'].append(speedlimit_d_x.data)
        sensed_data['SpeedLimit']['Position'].append(speedlimit_d_y.data)
        sensed_data['SpeedLimit']['Position'].append(speedlimit_d_z.data)
        sensed_data['SpeedLimit']['Value'] = speedlimit_val.data

        sensed_data['VehicleObjects']['Position'].append(vehicleob_d_x.data)
        sensed_data['VehicleObjects']['Position'].append(vehicleob_d_y.data)
        sensed_data['VehicleObjects']['Position'].append(vehicleob_d_z.data)

        sensed_data['VehicleObjects']['Velocity'].append(vehicleob_v_x.data)
        sensed_data['VehicleObjects']['Velocity'].append(vehicleob_v_y.data)
        sensed_data['VehicleObjects']['Velocity'].append(vehicleob_v_z.data)

        time.sleep(0.01)
        
    return sensed_data

if __name__ == '__main__':
    sensed_data = {}
    sensed_data = main()

