from abc import ABC, abstractmethod
from typing import List, Any, Optional
from dataclasses import dataclass, field

class NeuralSignal:
    """Represents a signal passing through the nervous system"""
    def __init__(self, signal_type: str, strength: float, data: Any = None):
        self.signal_type = signal_type
        self.strength = strength
        self.data = data

class NervousSystemComponent(ABC):
    """Abstract base class for all nervous system components"""
    
    def __init__(self, name: str, parent: Optional['NervousSystemComponent'] = None):
        self.name = name
        self.parent = parent
        self.children: List['NervousSystemComponent'] = []
        self.connections: List['NervousSystemComponent'] = []
        self.active = True
        
    def add_child(self, child: 'NervousSystemComponent'):
        """Add a child component"""
        child.parent = self
        self.children.append(child)
        
    def add_connection(self, target: 'NervousSystemComponent'):
        """Add a connection to another component"""
        self.connections.append(target)
        
    def get_path(self) -> str:
        """Get the full hierarchical path of this component"""
        if self.parent:
            return f"{self.parent.get_path()}/{self.name}"
        return self.name
    
    @abstractmethod
    def process_signal(self, signal: NeuralSignal) -> List[NeuralSignal]:
        """Process an incoming signal and return output signals"""
        # TODO: IMPLEMENT THIS
        pass
    
    def send_signal(self, signal: NeuralSignal):
        """Send a signal to all connected components"""
        for connection in self.connections:
            if connection.active:
                output_signals = connection.process_signal(signal)
                for output_signal in output_signals:
                    connection.send_signal(output_signal)

class BasicNervousSystemComponent(NervousSystemComponent):
    """Concrete implementation for basic nervous system components"""
    
    def process_signal(self, signal) -> List:
        """Basic signal processing - just passes through with slight decay"""
        if hasattr(signal, 'strength'):
            # Create a new signal with reduced strength
            output_signal = type(signal)(
                signal.signal_type if hasattr(signal, 'signal_type') else "processed",
                signal.strength * 0.9 if hasattr(signal, 'strength') else 0.5,
                signal.data if hasattr(signal, 'data') else None
            )
            return [output_signal]
        return []

class BrainRegion(NervousSystemComponent):
    """Base class for brain regions"""
    
    def __init__(self, name: str, function: str, parent=None):
        super().__init__(name, parent)
        self.function = function
        self.activity_level = 0.0
        
    def process_signal(self, signal: NeuralSignal) -> List[NeuralSignal]:
        """Default signal processing for brain regions"""
        self.activity_level = min(1.0, self.activity_level + signal.strength * 0.1)
        
        # Create output signal based on region's function
        output_signal = NeuralSignal(
            signal_type=f"{self.function}_processed",
            strength=signal.strength * 0.8,  # Some signal decay
            data=f"Processed by {self.name}"
        )
        return [output_signal]

class CorticalArea(BrainRegion):
    """Specialized class for cortical areas"""
    
    def __init__(self, name: str, function: str, area_type: str, parent=None):
        super().__init__(name, function, parent)
        self.area_type = area_type  # 'motor', 'sensory', 'association'
        self.layers = 6  # Cortical areas typically have 6 layers
        
    def process_signal(self, signal: NeuralSignal) -> List[NeuralSignal]:
        # Cortical areas have more complex processing
        processed_signals = super().process_signal(signal)
        
        # Add cortical-specific processing
        if self.area_type == 'motor' and signal.signal_type == 'motor_command':
            processed_signals[0].strength *= 1.2  # Amplify motor signals
        elif self.area_type == 'sensory':
            processed_signals[0].strength *= 0.9  # Slight filtering
            
        return processed_signals

class NervousSystemBuilder:
    """Builder class to construct the complete nervous system hierarchy"""
    
    def __init__(self):
        self.root = None
        
    def build_complete_system(self) -> NervousSystemComponent:
        """Build the complete nervous system hierarchy"""
        
        # Root system
        self.root = BasicNervousSystemComponent("NervousSystem")
        
        # Central Nervous System
        cns = BasicNervousSystemComponent("CentralNervousSystem")
        self.root.add_child(cns)
        
        # Build Brain
        brain = self._build_brain()
        cns.add_child(brain)
        
        # Build Spinal Cord
        spinal_cord = self._build_spinal_cord()
        cns.add_child(spinal_cord)
        
        # Peripheral Nervous System
        pns = BasicNervousSystemComponent("PeripheralNervousSystem")
        self.root.add_child(pns)
        
        # Build PNS components
        somatic = self._build_somatic_system()
        autonomic = self._build_autonomic_system()
        pns.add_child(somatic)
        pns.add_child(autonomic)
        
        return self.root
    
    def _build_brain(self) -> NervousSystemComponent:
        """Build the brain hierarchy"""
        brain = BasicNervousSystemComponent("Brain")
        
        # Cerebrum
        cerebrum = self._build_cerebrum()
        brain.add_child(cerebrum)
        
        # Cerebellum
        cerebellum = BrainRegion("Cerebellum", "motor_coordination")
        purkinje_layer = BrainRegion("PurkinjeLayer", "integration", cerebellum)
        granule_layer = BrainRegion("GranuleLayer", "input_processing", cerebellum)
        molecular_layer = BrainRegion("MolecularLayer", "output_processing", cerebellum)
        cerebellum.add_child(purkinje_layer)
        cerebellum.add_child(granule_layer)
        cerebellum.add_child(molecular_layer)
        brain.add_child(cerebellum)
        
        # Brainstem
        brainstem = self._build_brainstem()
        brain.add_child(brainstem)
        
        # Diencephalon
        diencephalon = self._build_diencephalon()
        brain.add_child(diencephalon)
        
        # Limbic System
        limbic = self._build_limbic_system()
        brain.add_child(limbic)
        
        return brain
    
    def _build_cerebrum(self) -> NervousSystemComponent:
        """Build cerebrum with cortical areas"""
        cerebrum = BasicNervousSystemComponent("Cerebrum")
        
        # Cerebral Cortex
        cortex = BasicNervousSystemComponent("CerebralCortex")
        
        # Frontal Lobe
        frontal = BasicNervousSystemComponent("FrontalLobe")
        motor_cortex = CorticalArea("PrimaryMotorCortex", "motor_control", "motor", frontal)
        prefrontal = CorticalArea("PrefrontalCortex", "executive_function", "association", frontal)
        brocas = CorticalArea("BrocasArea", "speech_production", "association", frontal)
        frontal.add_child(motor_cortex)
        frontal.add_child(prefrontal)
        frontal.add_child(brocas)
        cortex.add_child(frontal)
        
        # Parietal Lobe
        parietal = BasicNervousSystemComponent("ParietalLobe")
        somatosensory = CorticalArea("PrimarySomatosensoryCortex", "touch_processing", "sensory", parietal)
        posterior_parietal = CorticalArea("PosteriorParietalCortex", "spatial_processing", "association", parietal)
        parietal.add_child(somatosensory)
        parietal.add_child(posterior_parietal)
        cortex.add_child(parietal)
        
        # Temporal Lobe
        temporal = BasicNervousSystemComponent("TemporalLobe")
        auditory = CorticalArea("PrimaryAuditoryCortex", "hearing", "sensory", temporal)
        wernickes = CorticalArea("WernickesArea", "language_comprehension", "association", temporal)
        hippocampus = BrainRegion("Hippocampus", "memory_formation", temporal)
        temporal.add_child(auditory)
        temporal.add_child(wernickes)
        temporal.add_child(hippocampus)
        cortex.add_child(temporal)
        
        # Occipital Lobe
        occipital = BasicNervousSystemComponent("OccipitalLobe")
        visual = CorticalArea("PrimaryVisualCortex", "vision", "sensory", occipital)
        visual_assoc = CorticalArea("VisualAssociationAreas", "visual_processing", "association", occipital)
        occipital.add_child(visual)
        occipital.add_child(visual_assoc)
        cortex.add_child(occipital)
        
        cerebrum.add_child(cortex)
        
        # White Matter
        white_matter = BasicNervousSystemComponent("WhiteMatter")
        corpus_callosum = BrainRegion("CorpusCallosum", "interhemispheric_communication", white_matter)
        internal_capsule = BrainRegion("InternalCapsule", "projection_fibers", white_matter)
        white_matter.add_child(corpus_callosum)
        white_matter.add_child(internal_capsule)
        cerebrum.add_child(white_matter)
        
        return cerebrum
    
    def _build_brainstem(self) -> NervousSystemComponent:
        """Build brainstem components"""
        brainstem = BasicNervousSystemComponent("Brainstem")
        
        # Medulla
        medulla = BrainRegion("Medulla", "vital_functions")
        respiratory = BrainRegion("RespiratoryCenter", "breathing_control", medulla)
        cardiac = BrainRegion("CardiacCenter", "heart_rate_control", medulla)
        medulla.add_child(respiratory)
        medulla.add_child(cardiac)
        brainstem.add_child(medulla)
        
        # Pons
        pons = BrainRegion("Pons", "relay_sleep")
        pontine_nuclei = BrainRegion("PontineNuclei", "motor_relay", pons)
        sleep_centers = BrainRegion("SleepWakeCenters", "sleep_regulation", pons)
        pons.add_child(pontine_nuclei)
        pons.add_child(sleep_centers)
        brainstem.add_child(pons)
        
        # Midbrain
        midbrain = BrainRegion("Midbrain", "reflexes_reward")
        superior_coll = BrainRegion("SuperiorColliculus", "visual_reflexes", midbrain)
        substantia_nigra = BrainRegion("SubstantiaNigra", "dopamine_production", midbrain)
        midbrain.add_child(superior_coll)
        midbrain.add_child(substantia_nigra)
        brainstem.add_child(midbrain)
        
        return brainstem
    
    def _build_diencephalon(self) -> NervousSystemComponent:
        """Build diencephalon components"""
        diencephalon = BasicNervousSystemComponent("Diencephalon")
        
        # Thalamus
        thalamus = BrainRegion("Thalamus", "sensory_relay")
        sensory_relay = BrainRegion("SensoryRelayNuclei", "sensory_processing", thalamus)
        motor_relay = BrainRegion("MotorRelayNuclei", "motor_processing", thalamus)
        thalamus.add_child(sensory_relay)
        thalamus.add_child(motor_relay)
        diencephalon.add_child(thalamus)
        
        # Hypothalamus
        hypothalamus = BrainRegion("Hypothalamus", "homeostasis")
        paraventricular = BrainRegion("ParaventricularNucleus", "hormone_regulation", hypothalamus)
        suprachiasmatic = BrainRegion("SuprachiasmaticNucleus", "circadian_rhythm", hypothalamus)
        hypothalamus.add_child(paraventricular)
        hypothalamus.add_child(suprachiasmatic)
        diencephalon.add_child(hypothalamus)
        
        return diencephalon
    
    def _build_limbic_system(self) -> NervousSystemComponent:
        """Build limbic system components"""
        limbic = BasicNervousSystemComponent("LimbicSystem")
        
        # Hippocampus (more detailed)
        hippocampus = BrainRegion("Hippocampus", "memory_formation")
        dentate_gyrus = BrainRegion("DentateGyrus", "pattern_separation", hippocampus)
        ca1 = BrainRegion("CA1_Field", "memory_output", hippocampus)
        ca3 = BrainRegion("CA3_Field", "pattern_completion", hippocampus)
        hippocampus.add_child(dentate_gyrus)
        hippocampus.add_child(ca1)
        hippocampus.add_child(ca3)
        limbic.add_child(hippocampus)
        
        # Amygdala
        amygdala = BrainRegion("Amygdala", "fear_emotion")
        central_nucleus = BrainRegion("CentralNucleus", "fear_response", amygdala)
        basolateral = BrainRegion("BasolateralComplex", "fear_learning", amygdala)
        amygdala.add_child(central_nucleus)
        amygdala.add_child(basolateral)
        limbic.add_child(amygdala)
        
        return limbic
    
    def _build_spinal_cord(self) -> NervousSystemComponent:
        """Build spinal cord regions"""
        spinal_cord = BasicNervousSystemComponent("SpinalCord")
        
        regions = ["CervicalRegion", "ThoracicRegion", "LumbarRegion", "SacralRegion"]
        for region_name in regions:
            region = BrainRegion(region_name, "spinal_processing")
            spinal_cord.add_child(region)
            
        return spinal_cord
    
    def _build_somatic_system(self) -> NervousSystemComponent:
        """Build somatic nervous system"""
        somatic = BasicNervousSystemComponent("SomaticNervousSystem")
        
        # Cranial nerves
        cranial = BasicNervousSystemComponent("CranialNerves")
        cranial_names = ["Olfactory_I", "Optic_II", "Oculomotor_III", "Trigeminal_V", 
                        "Facial_VII", "Vestibulocochlear_VIII", "Vagus_X"]
        for nerve_name in cranial_names:
            nerve = BrainRegion(nerve_name, "peripheral_relay")
            cranial.add_child(nerve)
        somatic.add_child(cranial)
        
        return somatic
    
    def _build_autonomic_system(self) -> NervousSystemComponent:
        """Build autonomic nervous system"""
        autonomic = BasicNervousSystemComponent("AutonomicNervousSystem")
        
        # Sympathetic
        sympathetic = BrainRegion("SympatheticNervousSystem", "fight_flight")
        autonomic.add_child(sympathetic)
        
        # Parasympathetic
        parasympathetic = BrainRegion("ParasympatheticNervousSystem", "rest_digest")
        autonomic.add_child(parasympathetic)
        
        return autonomic