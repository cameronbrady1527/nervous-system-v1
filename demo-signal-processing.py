############################## BASIC USAGE ##############################

from v1_builder import NervousSystemBuilder, NeuralSignal

builder = NervousSystemBuilder()
nervous_system = builder.build_complete_system()

# Find a specific brain region
def find_component(root, name):
    if root.name == name:
        return root
    for child in root.children:
        result = find_component(child, name)
        if result:
            return result
    return None

# Get the primary motor cortex
motor_cortex = find_component(nervous_system, "PrimaryMotorCortex")
print(f"Found: {motor_cortex.get_path()}")

########################### SIGNAL PROCESSING ###########################

# Create a neural signal
signal = NeuralSignal(
    signal_type="motor_command",
    strength=0.8,
    data="move_right_hand"
)

# Process the signal
output_signals = motor_cortex.process_signal(signal)
print(f"Input: {signal.signal_type}")
print(f"Output: {[s.signal_type for s in output_signals]}")
print(f"Activity Level: {motor_cortex.activity_level}")
