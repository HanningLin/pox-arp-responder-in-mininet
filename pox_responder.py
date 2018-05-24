# Hanning Lin
# Zijing Mo
# The most of testing procedures were implemented in the KHKH 1-250 laboratory, UMTC.  

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.arp import arp
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet.ethernet import ethernet

# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

# Maximum Event ID
MAX_PRIORITY = 65535

class SelfLearingMethods (object):
    ARP_Table = {}
    def __init__ (self):
        core.openflow.addListeners(self)
        # We can assign the hosts sequentially
        # The h1 could be 00:00:00:00:00:01 and so on
        for i in range(1,9):
            mac = '00:00:00:00:00:0' + str(i)
            self.ARP_Table['10.0.0.' + str(i)] = mac
    # Set up this different switches
    def installing_rule(self, event, src_ip = None, src_mac = None, dst_ip = None, dst_mac = None,out_port=None):
        fentry = of.ofp_flow_mod()
        fentry.actions.append(of.ofp_action_output(port = out_port))
        fentry.match.dl_type = 0x800
        fentry.priority = MAX_PRIORITY
        if not src_ip==None:
            fentry.match.nw_src = IPAddr(src_ip)
        if not src_mac==None:
            fentry.match.dl_src = EthAddr(src_mac)
        if not dst_ip==None:
            fentry.match.nw_dst = IPAddr(dst_ip)
        if not dst_mac==None:
            fentry.match.dl_dst = EthAddr(dst_mac)
        if not out_port==None:
            event.connection.send(fentry)

    def installing_rules(self, event):
        ports = {"l1_link1":1, "l1_link2":2, "l1_link3":3, "l1_link4":4, "l2_link1":1, "l2_link2":2, "l2_link3":3, "l2_link4":4, "l3_link1":1, "l3_link2":2, "l3_link3":3, "l3_link4":4, "s4_link1":1, "s4_link2":2, "s4_link3":3, "s5_link1":1, "s5_link2":2, "s5_link3":3}
        #src_ip,  src_mac, dst_ip, dst_mac,  out_port):
        if event.dpid==1:
            self.installing_rule(event, None,None,"10.0.0.1","00:00:00:00:00:01",3)
            self.installing_rule(event, None,None,"10.0.0.2","00:00:00:00:00:02",4)
            self.installing_rule(event, "10.0.0.1","00:00:00:00:00:01",None,None,1)
            self.installing_rule(event, "10.0.0.2","00:00:00:00:00:02",None,None,2)
        if event.dpid==2:
            self.installing_rule(event, None,None,"10.0.0.3","00:00:00:00:00:03",3)
            self.installing_rule(event, None,None,"10.0.0.4","00:00:00:00:00:04",4)
            self.installing_rule(event, "10.0.0.3","00:00:00:00:00:03",None,None,1)
            self.installing_rule(event, "10.0.0.4","00:00:00:00:00:04",None,None,2)
        if event.dpid==3:
            self.installing_rule(event, None,None,"10.0.0.5","00:00:00:00:00:05",3)
            self.installing_rule(event, None,None,"10.0.0.6","00:00:00:00:00:06",4)
            self.installing_rule(event, "10.0.0.5","00:00:00:00:00:05",None,None,1)
            self.installing_rule(event, "10.0.0.6","00:00:00:00:00:06",None,None,2)
        if event.dpid==4:
            self.installing_rule(event, None,None,"10.0.0.1","00:00:00:00:00:01",1)
            self.installing_rule(event, None,None,"10.0.0.2","00:00:00:00:00:02",1)
            self.installing_rule(event, None,None,"10.0.0.3","00:00:00:00:00:03",2)
            self.installing_rule(event, None,None,"10.0.0.4","00:00:00:00:00:04",2)
            self.installing_rule(event, None,None,"10.0.0.5","00:00:00:00:00:05",3)
            self.installing_rule(event, None,None,"10.0.0.6","00:00:00:00:00:06",3)
        if event.dpid==5:
            self.installing_rule(event, None,None,"10.0.0.1","00:00:00:00:00:01",1)
            self.installing_rule(event, None,None,"10.0.0.2","00:00:00:00:00:02",1)
            self.installing_rule(event, None,None,"10.0.0.3","00:00:00:00:00:03",2)
            self.installing_rule(event, None,None,"10.0.0.4","00:00:00:00:00:04",2)
            self.installing_rule(event, None,None,"10.0.0.5","00:00:00:00:00:05",3)
            self.installing_rule(event, None,None,"10.0.0.6","00:00:00:00:00:06",3)

    def _handle_ConnectionUp (self, event):
    # The behaviors of switches
        for entry in event.connection.features.ports:
            # The behaviors of s-level switches
            if entry.name == 's4_link1':
                fentry = of.ofp_flow_mod()
                fentry.priority = 0x7777
                fentry.match.dl_type = ethernet.ARP_TYPE
                fentry.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
                event.connection.send(fentry)
            elif entry.name == 's5_link1':
                fentry = of.ofp_flow_mod()
                fentry.priority = 0x7777
                fentry.match.dl_type = ethernet.ARP_TYPE
                fentry.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
                event.connection.send(fentry)
            # The behaviors of L-level switches
            elif entry.name[0] == 'l':
                fentry = of.ofp_flow_mod()
                fentry.priority = 0x7777
                fentry.match.dl_type = ethernet.ARP_TYPE
                fentry.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
                event.connection.send(fentry)
        self.installing_rules(event)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        src_mac = packet.src
        match = of.ofp_match.from_packet(packet)
        info = packet.find('arp')
        if info:
            if(info.opcode == arp.REQUEST):
                src_ip = packet.find("arp").protosrc
                dst_ip = packet.find("arp").protodst
                    # We can put the our hardcode here
                packet = event.parsed
                find_event = event.parsed.find('arp')
                    # Inspired by a github example
                ARP_response = arp()
                ARP_response.hwtype = find_event.hwtype
                ARP_response.prototype = find_event.prototype
                ARP_response.hwlen = find_event.hwlen
                ARP_response.protolen = find_event.protolen
                ARP_response.opcode = ARP_response.REPLY # ARP reply status code (very important)                    ARP_response.hwdst = find_event.hwsrc
                ARP_response.protodst = find_event.protosrc
                ARP_response.protosrc = find_event.protodst
                ARP_response.hwsrc = EthAddr(self.ARP_Table[str(find_event.protodst)])
                Ethernet_Frame = ethernet(type = packet.type, src = ARP_response.hwsrc, dst = find_event.hwsrc)
                Ethernet_Frame.payload = ARP_response
                msg = of.ofp_packet_out()
                msg.data = Ethernet_Frame
                msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
                event.connection.send(msg)

    def _handle_PortStatus(self, event):#the function handles link failure
        if event.modified:
            port_down = event.port
            port_name = event.ofp.desc.name
            msg = of.ofp_flow_mod()
            msg.priority = MAX_PRIORITY
            msg.match.dl_type = 0x0800
            msg.command = of.OFPFC_MODIFY
            if port_name == "l1-eth1":
                msg.match.nw_src = IPAddr("10.0.0.1")
                msg.match.dl_src = EthAddr("00:00:00:00:00:01")
                msg.actions.append(of.ofp_action_output(port = 2))
                event.connection.send(msg)
            elif port_name == "l2-eth1":
                msg.match.nw_src = IPAddr("10.0.0.3")
                msg.match.dl_src = EthAddr("00:00:00:00:00:03")
                msg.actions.append(of.ofp_action_output(port = 2))
                event.connection.send(msg)
            elif port_name == "l3-eth1":
                msg.match.nw_src = IPAddr("10.0.0.5")
                msg.match.dl_src = EthAddr("00:00:00:00:00:05")
                msg.actions.append(of.ofp_action_output(port = 2))
                event.connection.send(msg)
            # Sending to S5
            elif port_name == "l1-eth2":
                msg.match.nw_src = IPAddr("10.0.0.2")
                msg.match.dl_src = EthAddr("00:00:00:00:00:02")
                msg.actions.append(of.ofp_action_output(port = 1))
                event.connection.send(msg)
            elif port_name == "l2-eth2":
                msg.match.nw_src = IPAddr("10.0.0.4")
                msg.match.dl_src = EthAddr("00:00:00:00:00:04")
                msg.actions.append(of.ofp_action_output(port = 1))
                event.connection.send(msg)
            elif port_name == "l3-eth2":
                msg.match.nw_src = IPAddr("10.0.0.6")
                msg.match.dl_src = EthAddr("00:00:00:00:00:06")
                msg.actions.append(of.ofp_action_output(port = 1))
                event.connection.send(msg)


def launch ():
    core.registerNew(SelfLearingMethods)
