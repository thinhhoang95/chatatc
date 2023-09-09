from aircraft import Aircraft
from converter import *
import utm 

import numpy as np
from paho.mqtt import client as mqtt_client
from fabrics_mqtt import connect_mqtt, topic, topic_control

from multiprocessing import Process, Queue
import time

import json
from command_parser import parse_command

# The simulator's main loop
def indie_sim(q):
    print('IndieSim Process Started')
    # Create an aircraft object
    vvts = (10.8188, 106.652)
    vvts_utm = utm.from_latlon(vvts[0], vvts[1], force_zone_number=48, force_zone_letter='P')

    sim_time = 0
    sim_max_time = 1000 # s

    # VN19: found 60km to the West and 80km to the North of VVTS, at 210 knots
    # flying heading 180 (South) and altitude 5,000 ft, with no wind
    # c approximates g
    # feedback control parameters khe = kmu = kV = 0.1
    # noise parameters sigma_he = sigma_mu = sigma_V = 0.1
    vn19 = Aircraft('vietnam 19', x=vvts_utm[0] - 60_000, y=vvts_utm[1] - 80_000, z=ft_to_m(5_000),
                    Vs=ms_to_fpm(0),
                    khi=deg_to_rad(0), mu=deg_to_rad(0), r_phi = 0, V=knots_to_ms(210),
                    eta_z=0, eta_khi=0, eta_mu=0, eta_V=0, # integrated error
                    c=9.8, # approx g
                    kpz=5, kdz=10, kiz=1e-3, # altitude reference control
                    kpvs=10, # FPA control
                    kpkhi=240.0, kdkhi=1600.0, kikhi=1.0, # heading control 
                    kpmu=0.25, kdmu=0.75, kimu=0.01, # roll reference control
                    kpV=0.1, kiV=0. # speed control
    )
    
    client = connect_mqtt()

    while sim_time < sim_max_time:
        print('t =', sim_time)
        vn19.get_response((0, 3), dt=0.05)
        vn19.commit_state_update()
        # Update to MQTT server
        
        #print('Connexion')
        message = {"sender": "indie", "planes": [], "t": sim_time}
        message['planes'].append(vn19.get_state())
        message_json = json.dumps(message)
        client.publish(topic, message_json)
        if q.empty():
            pass
        else:
            queue_item = q.get()
            # if api_call contains many commands separated by commas, split them
            api_calls = queue_item.split('),')
            api_calls = [api_call.strip() for api_call in api_calls]
            for api_call in api_calls:
                # Process LLM commands here
                api_command, api_params = parse_command(api_call)
                print(api_params)
                if api_command == "heading":
                    # Set target heading
                    # First param is callsign, second param is heading in degrees
                    vn19.heading_to(psi_to_khi(deg_to_rad(float(api_params[1]))))
                elif api_command == "altitude":
                    vn19.altitude_to(ft_to_m(float(api_params[1])))
                elif api_command == "speed":
                    vn19.speed_to(knots_to_ms(float(api_params[1])))
                print('API call: ', api_call)
        # Step time forward
        sim_time += 3
        time.sleep(3)
        
        
def mqtt_receiver_loop(q):
    def on_message(client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Message received: `{payload}`")
        q.put(payload)
        
    print('Fabrics IndieR Process Started')
    client = connect_mqtt()
    client.subscribe(topic_control) # control topic published by the LLM
    client.on_message = on_message
    client.loop_forever()
    
if __name__ == '__main__':
    q = Queue()
    indie_sim_process = Process(target=indie_sim, args=(q,))
    indie_sim_process.start()
    mqtt_receiver_process = Process(target=mqtt_receiver_loop, args=(q,))
    mqtt_receiver_process.start()
    indie_sim_process.join()
    mqtt_receiver_process.join()