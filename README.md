# POX RESPONDER
- We did the project in Python.

- Group Members: Hanning Lin  and Zijing Mo 

In this file, we will illustrate the basic Im-plementation and design detail of our code.
The object of this program is bringing about the data structure of leaf-spine. The whole project contains three parts. The first part is the ARP Responder. In this part, the host does not know the other host's MAC address in the network initially. After receiveing the ARP request packet, the ARP responder responds to the ARP queries sent from the hosts. This ARP responder resides at the controller, which means our code. The second part is the Installing Rules. We have hardcoded a dictionary. With the help of installing rules, the switches in the topology can know where to forward packets. The last part is regarding special scenario -- link failures. We will apply a command to close partial connections in the topology. After that, our controller still can find a path to create the connections among different hosts.  
The design details of this project are as follows. The whole controller algorithm is named "SelfLearingMethods()". In this class, we have six sub-functions: __init__(), installing_rule(), installing_rules(), _handle_ConnectionUp(), _handle_PacketIn() and _handle_PortStatus(). Different functions possess different features. The first function, which is __init__(), will set the default value of MAC addresses and IP addresses in the ARP table. The second function will set up the different switches for the IP addresses and MAC addresses we installed before. For the third function, we had hardcoded the specific rules in our controller. The various event IDs will trigger different events. That means that the entities in our topology, which are switches or hosts, can gain different types of source IP address, source MAC address, destination IP address and destination MAC address. The last three functions fit in with the mechanism of POX control applications. In the "ConnectionUp" case, the code implements the behaviors of switches: S4, S5, and all named lx. Based on different names, the entities in our topology will enforce the functionality of controller or flood. In the next, the "PacketIn" case is most important part of our project. In this function, the controller can implement what the response it should do when it receives the information from the remote entities, such as l-level switches or hosts. The last function is "PortStatus". This one can determine which spine path the hosts can choose. In our policy of choosing the spine switch, traffic source from h1, h3, and h5 should traverse through spine switch s4 and traffic source from h2, h4 and h6 should traverse through spine switch s5. Moreover, this function also controls the link failure event. We can implement "link some hosts down" or "link some hosts up" to close or open the connection.

There are some details for running the project:
1. Putting the "pox_responder.py" into the correct pox directory.
2. Running the pox command in the directory which we put the "pox_responder.py" file. A recommendatory input should be "./pox.py samples.pox_responder" when you locate at the ~/pox directory.
3. Opening another terminal. You should locate your present work directory in the directory where you store the topology.py file.
4. Inputting "sudo mn --controller=remote --custom topology.py --topo mytopo --mac".


Work Breakdown:
Hanning and Zijing both are responsible for the all parts of the code file, README file and session file.

If you have any interesting question, please feel free to let us know. We are glad to hear your feedback!
