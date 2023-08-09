In macOS, `bridge100`, `bridge101`, and similar interfaces are typically associated with the built-in virtualization framework used by services like Parallels Desktop, VMware Fusion, Docker for Mac, and other virtualization or containerization solutions.

Here's a breakdown:

### **Bridged Networking**:

- **Purpose**: Bridged networking allows a virtual machine (VM) or container to have a network connection that looks and behaves like a direct connection to the physical network, even getting its own IP address from the DHCP server on the network.
  
- **How It Works**: The bridge interface acts as a virtual switch, and the VM's or container's virtual network adapter is connected to this switch. The bridge then connects this virtual switch to the physical network interface on the host, allowing the VM or container to communicate with other devices on the network as if it were a physical device itself.

### **bridge100, bridge101, etc. on macOS**:

- These are virtual bridge interfaces created by macOS. Each bridge interface can be associated with one or more virtual network interfaces from VMs or containers.
  
- For example, if you're running two VMs on your Mac using software like VMware Fusion or Parallels Desktop, each VM might have its virtual network adapter connected to one of these bridge interfaces. This allows the VM to communicate with the external network through the host's physical network adapter.
  
- The numbering (`bridge100`, `bridge101`, etc.) is automatically assigned by macOS and can vary. The exact number doesn't have a specific significance other than distinguishing between different bridge interfaces.

### **Why Use Bridged Networking?**:

- **Isolation**: Each VM or container gets its own IP address on the external network, isolating its network traffic from other VMs or containers.
  
- **Direct Network Access**: VMs or containers can directly access network resources without relying on the host's network configuration. This is useful for applications or services in the VM or container that need to be accessible from other devices on the network.

- **Network Compatibility**: Some applications or services might expect to be running on a device with a direct network connection. Bridged networking can satisfy these expectations even when the application or service is running inside a VM or container.

### **Conclusion**:

If you see `bridge100`, `bridge101`, etc., on your Mac and you're using virtualization or containerization software, it's likely these interfaces are facilitating the network connections for your VMs or containers. If you're not actively using such software, these interfaces might be remnants from previous installations or configurations.