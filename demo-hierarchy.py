from v1_builder import *

def demo_system():
    """Demonstrate the nervous system hierarchy"""
    
    # Build the complete system
    builder = NervousSystemBuilder()
    nervous_system = builder.build_complete_system()
    
    # Print hierarchy
    def print_hierarchy(component, indent=0):
        print("  " * indent + f"├── {component.name}")
        for child in component.children:
            print_hierarchy(child, indent + 1)
    
    print("NERVOUS SYSTEM HIERARCHY:")
    print_hierarchy(nervous_system)
    
    # Find specific components
    def find_component(root, name):
        if root.name == name:
            return root
        for child in root.children:
            result = find_component(child, name)
            if result:
                return result
        return None
    
    # Example: Find and demonstrate signal processing
    motor_cortex = find_component(nervous_system, "PrimaryMotorCortex")
    if motor_cortex:
        print(f"\nFound: {motor_cortex.get_path()}")
        
        # Create and process a signal
        signal = NeuralSignal("motor_command", 0.8, "move_right_hand")
        output_signals = motor_cortex.process_signal(signal)
        
        print(f"Processing signal: {signal.signal_type}")
        print(f"Output signals: {[s.signal_type for s in output_signals]}")
        print(f"Motor cortex activity level: {motor_cortex.activity_level}")

if __name__ == "__main__":
    demo_system()