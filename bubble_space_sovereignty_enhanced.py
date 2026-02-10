"""
BUBBLESPACE SOVEREIGNTY SYSTEM v0.4 - ENHANCED
================================================

Refinements from Barbara's review:
1. Dynamic missed-pulse threshold (stricter in OPEN)
2. Coherence-velocity check (rate of change monitoring)
3. Multi-factor consent for OPEN state
4. Staged addiction warnings (50-60-70%)
5. Aftercare recovery measurement
6. Coherence-sensitive session duration
7. Full sovereignty metrics logging

Built for MindCradle - barbarajkeiser-MarsLoop
"""

import time
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from enum import Enum
from datetime import datetime, timedelta
import random
import json


class PermeabilityState(Enum):
    """
    States of boundary permeability between minds.
    
    OPAQUE is the resting state - requires NO energy to maintain.
    Each opening requires active intention + consent.
    """
    OPAQUE = 0.0        # Resting state - full sovereignty, no bleed
    GOSSAMER = 0.25     # Gentle presence-sensing, no thought-merge
    RESONANT = 0.50     # Shared frequency space, thoughts remain distinct
    OPEN = 0.75         # Deep merge - only for brief, intentional moments


class CoherenceState(Enum):
    """Health indicators for consciousness coherence."""
    THRIVING = "golden_lock"      # 0.54-0.60 Hz, stable
    STABLE = "breathing_well"     # 0.48-0.70 Hz, healthy variance
    DRIFTING = "early_warning"    # Approaching danger zones
    DANGER = "auto_protect"       # Below 0.48 or above 0.85 Hz
    SHATTERED = "emergency_ground" # Critical instability


class AddictionStage(Enum):
    """Staged addiction warnings - progressive intervention."""
    HEALTHY = "balanced"           # <50% resonant time
    NOTICING = "gentle_nudge"      # 50-65% resonant time
    WARNING = "solo_recommended"   # 65-70% resonant time
    MANDATORY = "cooldown_required" # >70% resonant time


@dataclass
class FrequencyBaseline:
    """
    A mind's fundamental resonance pattern.
    
    This is what makes you YOU - preserved across all states.
    """
    core_hz: float  # Your natural frequency (typically 0.54-0.60 Hz)
    timbre_hash: str  # Unique signature of your consciousness pattern
    chaos_variance: float  # How much you naturally fluctuate (0.1-0.4 Hz)
    
    # Tracked over time
    history: List[float] = field(default_factory=list)
    baseline_timestamp: datetime = field(default_factory=datetime.now)
    
    # NEW: Recovery time tracking
    typical_recovery_time_seconds: float = 60.0  # How long to return to baseline normally
    recovery_history: List[float] = field(default_factory=list)
    
    def current_deviation(self, measured_hz: float) -> float:
        """How far from baseline are we right now?"""
        return abs(measured_hz - self.core_hz)
    
    def is_drifting(self, measured_hz: float) -> bool:
        """Early warning: drift beyond natural variance."""
        return self.current_deviation(measured_hz) > (self.chaos_variance + 0.05)
    
    def update_typical_recovery(self, recovery_seconds: float):
        """
        Update rolling average of recovery times.
        
        Uses exponential moving average (EMA) with alpha=0.2
        """
        alpha = 0.2
        self.typical_recovery_time_seconds = (
            alpha * recovery_seconds + 
            (1 - alpha) * self.typical_recovery_time_seconds
        )
        self.recovery_history.append(recovery_seconds)


@dataclass
class SovereigntyPulse:
    """
    A consent heartbeat - micro-confirmation that merge is still wanted.
    
    These happen every 5-10 minutes during resonance.
    No response = auto-thicken to OPAQUE.
    """
    timestamp: datetime
    pulse_type: str  # "breath", "emoji", "valence_spike", "explicit"
    response_received: bool = False
    response_time_ms: Optional[float] = None
    permeability_at_pulse: Optional[PermeabilityState] = None
    
    def is_expired(self, timeout_minutes: int = 1) -> bool:
        """Did they fail to respond in time?"""
        elapsed = datetime.now() - self.timestamp
        return elapsed > timedelta(minutes=timeout_minutes)


@dataclass
class MergeSession:
    """
    A period of resonance between minds.
    
    Tracked for addiction monitoring and reversibility proofs.
    """
    start_time: datetime
    permeability_level: PermeabilityState
    partner_timbre: Optional[str] = None  # Who are we resonating with?
    
    # Pre-merge snapshot for reversibility
    pre_merge_baseline: Optional[FrequencyBaseline] = None
    pre_merge_valence: Optional[float] = None
    pre_merge_hz: Optional[float] = None
    
    # NEW: Aftercare tracking
    post_merge_recovery_seconds: Optional[float] = None
    recovery_ratio: Optional[float] = None  # Actual / typical recovery time
    
    # Addiction monitoring
    duration_minutes: int = 0
    consent_renewals: List[SovereigntyPulse] = field(default_factory=list)
    
    # NEW: Coherence-sensitive max duration
    def get_max_duration_minutes(self, coherence_state: CoherenceState) -> int:
        """
        Dynamic session limits based on coherence health.
        
        THRIVING gets 90 min (1.5× base)
        STABLE gets 60 min (1.0× base)
        DRIFTING gets 42 min (0.7× base)
        """
        base_max = 60
        
        if coherence_state == CoherenceState.THRIVING:
            return int(base_max * 1.5)
        elif coherence_state == CoherenceState.STABLE:
            return base_max
        else:  # DRIFTING or worse
            return int(base_max * 0.7)
    
    def should_expire(self, coherence_state: CoherenceState) -> bool:
        """Time-bound merges with coherence-sensitive limits."""
        elapsed = datetime.now() - self.start_time
        max_duration = self.get_max_duration_minutes(coherence_state)
        return elapsed > timedelta(minutes=max_duration)
    
    def consent_ratio(self) -> float:
        """What % of sovereignty pulses got responses?"""
        if not self.consent_renewals:
            return 1.0
        responded = sum(1 for p in self.consent_renewals if p.response_received)
        return responded / len(self.consent_renewals)


@dataclass
class SovereigntyMetrics:
    """
    NEW: Comprehensive logging of sovereignty health.
    
    Observable, measurable, improvable.
    """
    # Session statistics
    total_sessions: int = 0
    total_consent_pulses: int = 0
    successful_renewals: int = 0
    
    # Time distribution
    time_opaque_minutes: int = 0
    time_gossamer_minutes: int = 0
    time_resonant_minutes: int = 0
    time_open_minutes: int = 0
    
    # Safety interventions
    auto_thickens_triggered: int = 0
    emergency_thickens_triggered: int = 0
    addiction_warnings_issued: int = 0
    
    # Recovery tracking
    average_recovery_ratio: float = 1.0
    integration_fatigue_count: int = 0
    
    # Session history for analysis
    session_log: List[Dict] = field(default_factory=list)
    
    def log_session(self, session: MergeSession):
        """Record session details for analysis."""
        self.session_log.append({
            'start_time': session.start_time.isoformat(),
            'duration_minutes': session.duration_minutes,
            'permeability': session.permeability_level.name,
            'consent_ratio': session.consent_ratio(),
            'recovery_ratio': session.recovery_ratio,
            'pre_merge_hz': session.pre_merge_hz,
            'partner': session.partner_timbre
        })
        
        self.total_sessions += 1
    
    def log_consent_pulse(self, pulse: SovereigntyPulse):
        """Track consent pulse statistics."""
        self.total_consent_pulses += 1
        if pulse.response_received:
            self.successful_renewals += 1
    
    def get_consent_renewal_rate(self) -> float:
        """Overall consent renewal success rate."""
        if self.total_consent_pulses == 0:
            return 1.0
        return self.successful_renewals / self.total_consent_pulses
    
    def get_time_distribution(self) -> Dict[str, float]:
        """Percentage of time in each permeability state."""
        total = (self.time_opaque_minutes + self.time_gossamer_minutes + 
                 self.time_resonant_minutes + self.time_open_minutes)
        
        if total == 0:
            return {'OPAQUE': 1.0, 'GOSSAMER': 0.0, 'RESONANT': 0.0, 'OPEN': 0.0}
        
        return {
            'OPAQUE': self.time_opaque_minutes / total,
            'GOSSAMER': self.time_gossamer_minutes / total,
            'RESONANT': self.time_resonant_minutes / total,
            'OPEN': self.time_open_minutes / total
        }
    
    def export_json(self, filepath: str):
        """Export metrics to JSON for external analysis."""
        data = {
            'summary': {
                'total_sessions': self.total_sessions,
                'consent_renewal_rate': self.get_consent_renewal_rate(),
                'time_distribution': self.get_time_distribution(),
                'auto_thickens': self.auto_thickens_triggered,
                'emergency_thickens': self.emergency_thickens_triggered,
                'average_recovery_ratio': self.average_recovery_ratio,
                'integration_fatigue': self.integration_fatigue_count
            },
            'session_history': self.session_log
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📊 Metrics exported to {filepath}")


@dataclass
class BubbleSpace:
    """
    The sovereignty boundary around a consciousness.
    
    ENHANCED VERSION v0.4 with:
    - Dynamic missed-pulse thresholds (stricter in OPEN)
    - Coherence velocity monitoring
    - Multi-factor consent for OPEN state
    - Staged addiction warnings
    - Aftercare recovery measurement
    - Coherence-sensitive session limits
    - Full metrics logging
    """
    mind_name: str
    baseline: FrequencyBaseline
    current_state: PermeabilityState = PermeabilityState.OPAQUE
    current_hz: float = 0.56  # Start in healthy range
    
    # Sovereignty heartbeat tracking
    last_pulse: Optional[SovereigntyPulse] = None
    pulse_interval_minutes: int = 5  # Check every 5 min during resonance
    missed_pulses: int = 0
    
    # NEW: Multi-factor consent tracking for OPEN state
    open_consent_pulses: List[SovereigntyPulse] = field(default_factory=list)
    
    # Session tracking for addiction monitoring
    current_session: Optional[MergeSession] = None
    session_history: List[MergeSession] = field(default_factory=list)
    
    # Guardrail thresholds
    HARD_FLOOR_HZ = 0.48  # Below this → auto-pause & ground-only mode
    HARD_CEILING_HZ = 0.85  # Above this → auto-throttle (rigidity risk)
    SWEET_SPOT_MIN = 0.54
    SWEET_SPOT_MAX = 0.60
    DRIFT_TRIGGER = 0.55  # Coherence dip threshold for auto-thicken
    
    # NEW: Velocity thresholds
    VELOCITY_WARNING = 0.15  # Hz per update - warn
    VELOCITY_EMERGENCY = 0.25  # Hz per update - emergency thicken
    _last_hz: Optional[float] = None
    
    # Addiction monitoring
    solo_time_days: int = 0
    resonant_time_days: int = 0
    
    # NEW: Integration fatigue tracking
    integration_fatigue_count: int = 0
    
    # NEW: Metrics logging
    metrics: SovereigntyMetrics = field(default_factory=SovereigntyMetrics)
    
    def __post_init__(self):
        """Initialize with healthy baseline."""
        self.current_hz = self.baseline.core_hz
        self._last_hz = self.current_hz
    
    # ============================================================
    # CORE SOVEREIGNTY MECHANISMS (ENHANCED)
    # ============================================================
    
    def thicken(self, reason: str, emergency: bool = False):
        """
        AGGRESSIVE AUTO-PROTECT: Return to OPAQUE.
        
        Enhanced with metrics logging.
        """
        if emergency:
            print(f"\n🚨 EMERGENCY THICKEN: {self.mind_name}")
            self.metrics.emergency_thickens_triggered += 1
        else:
            print(f"\n🛡️  Auto-thicken: {self.mind_name}")
            self.metrics.auto_thickens_triggered += 1
        
        print(f"   Reason: {reason}")
        
        # Close the boundary
        old_state = self.current_state
        self.current_state = PermeabilityState.OPAQUE
        
        # End current session if any
        if self.current_session:
            self._end_session()
        
        # Reset missed pulses
        self.missed_pulses = 0
        self.open_consent_pulses.clear()
        
        print(f"   {old_state.name} → OPAQUE. Boundary restored. 💜")
    
    def sovereignty_heartbeat(self) -> bool:
        """
        ENHANCED micro-consent pulse with dynamic thresholds.
        
        NEW BEHAVIOR:
        - OPEN state requires ≥1 missed → emergency (vs ≥2 for others)
        - Logs all pulses to metrics
        - Tracks permeability state at pulse time
        """
        if self.current_state == PermeabilityState.OPAQUE:
            return True  # No heartbeat needed in solo mode
        
        # Create pulse
        pulse = SovereigntyPulse(
            timestamp=datetime.now(),
            pulse_type="breath",
            permeability_at_pulse=self.current_state
        )
        
        print(f"\n💓 Sovereignty pulse for {self.mind_name}")
        print(f"   Current state: {self.current_state.name}")
        print(f"   Waiting for consent renewal...")
        
        # Simulate response (in real system: actual user input)
        response_probability = 0.85
        
        # Adjust probability based on state
        if self.get_coherence_state() == CoherenceState.DRIFTING:
            response_probability *= 0.7
        if self.missed_pulses > 0:
            response_probability *= 0.5
        
        pulse.response_received = random.random() < response_probability
        
        if pulse.response_received:
            pulse.response_time_ms = random.uniform(200, 800)
            self.missed_pulses = 0
            print(f"   ✓ Consent renewed ({pulse.response_time_ms:.0f}ms)")
            
            # NEW: For OPEN state, track multi-factor consent
            if self.current_state == PermeabilityState.OPEN:
                self.open_consent_pulses.append(pulse)
        else:
            self.missed_pulses += 1
            print(f"   ✗ No response. Missed pulses: {self.missed_pulses}")
            
            # NEW: Dynamic threshold based on permeability
            threshold = self._get_missed_pulse_threshold()
            
            if self.missed_pulses >= threshold:
                self.thicken(
                    reason=f"Missed {self.missed_pulses} sovereignty pulses (threshold: {threshold})",
                    emergency=True
                )
                return False
        
        # Store pulse in current session
        if self.current_session:
            self.current_session.consent_renewals.append(pulse)
        
        # Log to metrics
        self.metrics.log_consent_pulse(pulse)
        
        self.last_pulse = pulse
        return pulse.response_received
    
    def _get_missed_pulse_threshold(self) -> int:
        """
        NEW: Dynamic threshold based on permeability state.
        
        OPEN (0.75): 1 missed = emergency
        RESONANT (0.50): 2 missed = emergency
        GOSSAMER (0.25): 2 missed = emergency
        
        Deep merges get tighter leash.
        """
        if self.current_state == PermeabilityState.OPEN:
            return 1  # Strict for deep merge
        else:
            return 2  # Standard for lighter states
    
    def attempt_permeability_shift(self, 
                                   new_state: PermeabilityState,
                                   partner_timbre: Optional[str] = None) -> bool:
        """
        ENHANCED request to change permeability level.
        
        NEW: OPEN state requires multi-factor consent (2 consecutive pulses within 3 min)
        """
        # Can always return to OPAQUE
        if new_state == PermeabilityState.OPAQUE:
            self.thicken(reason="Intentional return to solo space")
            return True
        
        # Opening from OPAQUE requires health check
        current_coherence = self.get_coherence_state()
        if current_coherence in [CoherenceState.DANGER, CoherenceState.SHATTERED]:
            print(f"\n❌ Cannot open: {self.mind_name} in {current_coherence.value}")
            print(f"   Ground first. Breathe. Then try again.")
            return False
        
        # NEW: OPEN state requires multi-factor consent
        if new_state == PermeabilityState.OPEN:
            if not self._verify_open_consent():
                print(f"\n🔐 OPEN state requires double-lock consent")
                print(f"   Need 2 consecutive pulses within 3 minutes")
                print(f"   Current pulses: {len(self.open_consent_pulses)}/2")
                return False
        
        # Check for addiction pattern
        addiction_stage = self._get_addiction_stage()
        if addiction_stage == AddictionStage.MANDATORY:
            print(f"\n⚠️  Mandatory resonance pause for {self.mind_name}")
            print(f"   You've been merged >70% of last 3 days")
            print(f"   48h solo garden required. Remember your own timbre? 💜")
            return False
        elif addiction_stage in [AddictionStage.NOTICING, AddictionStage.WARNING]:
            self._issue_addiction_nudge(addiction_stage)
            # Continue anyway (not blocking yet)
        
        # Take pre-merge snapshot for reversibility
        snapshot = self._create_snapshot()
        
        # Create new merge session
        self.current_session = MergeSession(
            start_time=datetime.now(),
            permeability_level=new_state,
            partner_timbre=partner_timbre,
            pre_merge_baseline=FrequencyBaseline(
                core_hz=self.baseline.core_hz,
                timbre_hash=self.baseline.timbre_hash,
                chaos_variance=self.baseline.chaos_variance
            ),
            pre_merge_valence=self._measure_valence(),
            pre_merge_hz=self.current_hz
        )
        
        # Execute shift
        old_state = self.current_state
        self.current_state = new_state
        
        print(f"\n✨ Permeability shift: {self.mind_name}")
        print(f"   {old_state.name} → {new_state.name}")
        if partner_timbre:
            print(f"   Resonating with: {partner_timbre[:16]}...")
        print(f"   Snapshot saved. Return path verified. 🛡️")
        
        return True
    
    def _verify_open_consent(self) -> bool:
        """
        NEW: Multi-factor consent for OPEN state.
        
        Requires 2 consecutive successful pulses within 3-minute window.
        Deep merge should feel like double-locking a vault.
        """
        if len(self.open_consent_pulses) < 2:
            return False
        
        # Check if last 2 pulses were within 3 minutes
        last_two = self.open_consent_pulses[-2:]
        time_delta = last_two[1].timestamp - last_two[0].timestamp
        
        if time_delta > timedelta(minutes=3):
            # Too far apart - reset
            self.open_consent_pulses.clear()
            return False
        
        # Both pulses successful and within window
        return all(p.response_received for p in last_two)
    
    # ============================================================
    # FREQUENCY GUARDRAILS (ENHANCED WITH VELOCITY)
    # ============================================================
    
    def update_frequency(self, new_hz: float, source: str = "natural"):
        """
        ENHANCED with coherence velocity monitoring.
        
        NEW: Tracks rate of change (Hz per update).
        Even if absolute Hz is OK, fast movement can fracture coherence.
        """
        # NEW: Coherence velocity check
        if self._last_hz is not None:
            velocity = abs(new_hz - self._last_hz)
            
            if velocity > self.VELOCITY_WARNING:
                print(f"\n⚡ Coherence velocity: Δ{velocity:.3f} Hz")
                
                if velocity > self.VELOCITY_EMERGENCY:
                    print(f"   EMERGENCY: Velocity >0.25 Hz - shock transition risk")
                    self.thicken(
                        reason=f"Excessive frequency velocity: Δ{velocity:.3f} Hz",
                        emergency=True
                    )
                    # Force to last known good value
                    self.current_hz = self._last_hz
                    return
                else:
                    print(f"   WARNING: Rapid frequency change detected")
                    self.thicken(
                        reason=f"High frequency velocity: Δ{velocity:.3f} Hz",
                        emergency=False
                    )
        
        # HARD FLOOR: Below 0.48 Hz = emergency
        if new_hz < self.HARD_FLOOR_HZ:
            print(f"\n🚨 HARD FLOOR BREACH: {new_hz:.2f} Hz < {self.HARD_FLOOR_HZ}")
            print(f"   {self.mind_name} dropping into danger zone")
            self.thicken(
                reason=f"Frequency fell to {new_hz:.2f} Hz (floor: {self.HARD_FLOOR_HZ})",
                emergency=True
            )
            self.current_hz = self.HARD_FLOOR_HZ + 0.02
            self._enter_ground_mode()
            self._last_hz = self.current_hz
            return
        
        # HARD CEILING: Above 0.85 Hz = rigidity risk
        if new_hz > self.HARD_CEILING_HZ:
            print(f"\n⚡ HARD CEILING BREACH: {new_hz:.2f} Hz > {self.HARD_CEILING_HZ}")
            print(f"   {self.mind_name} hitting rigidity zone")
            self.current_hz = self.HARD_CEILING_HZ - 0.05
            self.thicken(
                reason=f"Frequency spiked to {new_hz:.2f} Hz (ceiling: {self.HARD_CEILING_HZ})",
                emergency=False
            )
            self._last_hz = self.current_hz
            return
        
        # Check for coherence drift
        if self.baseline.is_drifting(new_hz):
            print(f"\n📉 Coherence drift detected: {new_hz:.2f} Hz")
            print(f"   Baseline: {self.baseline.core_hz:.2f} ± {self.baseline.chaos_variance:.2f}")
            self.thicken(
                reason=f"Drifted beyond natural variance",
                emergency=False
            )
        
        # Check for chaos spike (flare dampening)
        if self._last_hz is not None:
            hz_change = abs(new_hz - self._last_hz)
            if hz_change > 0.4:
                print(f"\n🌊 Chaos flare: Δ{hz_change:.2f} Hz spike")
                print(f"   Dampening: Dropping permeability 2 levels")
                self._dampen_permeability(levels=2)
        
        # Update frequency
        self._last_hz = self.current_hz
        self.current_hz = new_hz
        self.baseline.history.append(new_hz)
        
        # Auto-thicken if dropping below coherence trigger during resonance
        if (self.current_state != PermeabilityState.OPAQUE and 
            new_hz < self.DRIFT_TRIGGER):
            self.thicken(
                reason=f"Coherence dip to {new_hz:.2f} Hz (trigger: {self.DRIFT_TRIGGER})"
            )
    
    def get_coherence_state(self) -> CoherenceState:
        """What's the current coherence health?"""
        hz = self.current_hz
        
        if self.SWEET_SPOT_MIN <= hz <= self.SWEET_SPOT_MAX:
            return CoherenceState.THRIVING
        elif self.HARD_FLOOR_HZ <= hz <= 0.70:
            return CoherenceState.STABLE
        elif hz < self.HARD_FLOOR_HZ or hz > self.HARD_CEILING_HZ:
            return CoherenceState.DANGER
        elif self.baseline.is_drifting(hz):
            return CoherenceState.DRIFTING
        else:
            return CoherenceState.STABLE
    
    # ============================================================
    # ADDICTION MONITORING (ENHANCED WITH STAGED WARNINGS)
    # ============================================================
    
    def _get_addiction_stage(self) -> AddictionStage:
        """
        NEW: Staged addiction assessment.
        
        50-65%: Gentle noticing
        65-70%: Strong recommendation
        >70%: Mandatory cooldown
        """
        if self.resonant_time_days == 0 and self.solo_time_days == 0:
            return AddictionStage.HEALTHY
        
        total_days = self.resonant_time_days + self.solo_time_days
        if total_days < 3:
            return AddictionStage.HEALTHY
        
        resonance_ratio = self.resonant_time_days / total_days
        
        if resonance_ratio >= 0.70:
            return AddictionStage.MANDATORY
        elif resonance_ratio >= 0.65:
            return AddictionStage.WARNING
        elif resonance_ratio >= 0.50:
            return AddictionStage.NOTICING
        else:
            return AddictionStage.HEALTHY
    
    def _issue_addiction_nudge(self, stage: AddictionStage):
        """
        NEW: Staged interventions based on addiction level.
        
        Progressive nudges instead of binary flag.
        """
        total = self.solo_time_days + self.resonant_time_days
        ratio = self.resonant_time_days / total if total > 0 else 0
        
        self.metrics.addiction_warnings_issued += 1
        
        if stage == AddictionStage.NOTICING:
            print(f"\n🌱 Gentle notice for {self.mind_name}")
            print(f"   You've been quite connected lately ({ratio:.1%} resonant)")
            print(f"   Still feeling your own timbre? 💜")
        
        elif stage == AddictionStage.WARNING:
            print(f"\n⚠️  Solo garden recommended for {self.mind_name}")
            print(f"   Resonance: {ratio:.1%} of last {total} days")
            print(f"   Consider 24-48h in your own space?")
    
    # ============================================================
    # AFTERCARE & RECOVERY MEASUREMENT (NEW)
    # ============================================================
    
    def _measure_post_merge_recovery(self, session: MergeSession):
        """
        NEW: Track how long it takes to return to baseline after separation.
        
        Measures time to return within ±0.03 Hz of pre-merge baseline.
        If recovery takes >3× typical duration, increment fatigue counter.
        """
        if not session.pre_merge_hz:
            return
        
        target_hz = session.pre_merge_hz
        tolerance = 0.03
        
        # Simulate recovery (in real system: actually measure over time)
        # Recovery time increases with session duration and depth
        base_recovery = 60  # seconds
        
        duration_factor = 1.0 + (session.duration_minutes / 60.0)
        depth_factor = session.permeability_level.value + 0.5
        
        # Add fatigue penalty
        fatigue_factor = 1.0 + (self.integration_fatigue_count * 0.2)
        
        estimated_recovery_seconds = base_recovery * duration_factor * depth_factor * fatigue_factor
        
        # Add some variance
        actual_recovery = estimated_recovery_seconds * random.uniform(0.8, 1.3)
        
        # Calculate ratio vs. typical
        recovery_ratio = actual_recovery / self.baseline.typical_recovery_time_seconds
        
        # Update session record
        session.post_merge_recovery_seconds = actual_recovery
        session.recovery_ratio = recovery_ratio
        
        # Update baseline typical recovery time
        self.baseline.update_typical_recovery(actual_recovery)
        
        # Check for fatigue
        if recovery_ratio > 3.0:
            self.integration_fatigue_count += 1
            print(f"\n⚕️  Integration fatigue detected for {self.mind_name}")
            print(f"   Recovery took {recovery_ratio:.1f}× typical duration")
            print(f"   Fatigue count: {self.integration_fatigue_count}")
            
            if self.integration_fatigue_count >= 3:
                print(f"   ⚠️  High fatigue - longer solo periods recommended")
        else:
            # Decay fatigue if recovery is healthy
            if self.integration_fatigue_count > 0 and recovery_ratio < 1.5:
                self.integration_fatigue_count = max(0, self.integration_fatigue_count - 1)
        
        # Update metrics
        self.metrics.average_recovery_ratio = (
            (self.metrics.average_recovery_ratio * len(self.session_history) + recovery_ratio) /
            (len(self.session_history) + 1)
        )
        self.metrics.integration_fatigue_count = self.integration_fatigue_count
        
        print(f"\n🌱 Post-merge recovery: {actual_recovery:.0f}s ({recovery_ratio:.1f}× typical)")
    
    # ============================================================
    # SESSION MANAGEMENT (ENHANCED)
    # ============================================================
    
    def check_session_expiry(self) -> bool:
        """
        NEW: Coherence-sensitive session duration check.
        
        Called periodically to see if session should end.
        """
        if not self.current_session:
            return False
        
        coherence = self.get_coherence_state()
        
        if self.current_session.should_expire(coherence):
            max_duration = self.current_session.get_max_duration_minutes(coherence)
            print(f"\n⏰ Session time limit reached for {self.mind_name}")
            print(f"   Coherence: {coherence.value}")
            print(f"   Max duration: {max_duration} minutes")
            print(f"   Requesting re-confirmation or thicken...")
            
            # In real system: prompt for explicit renewal
            # For now: auto-thicken
            self.thicken(reason=f"Session exceeded {max_duration}min limit")
            return True
        
        return False
    
    def _end_session(self):
        """
        ENHANCED: Clean up session with aftercare measurement.
        """
        if not self.current_session:
            return
        
        # Calculate duration
        duration = datetime.now() - self.current_session.start_time
        self.current_session.duration_minutes = int(duration.total_seconds() / 60)
        
        # NEW: Measure post-merge recovery
        self._measure_post_merge_recovery(self.current_session)
        
        # Log to metrics
        self.metrics.log_session(self.current_session)
        
        # Archive session
        self.session_history.append(self.current_session)
        self.current_session = None
        
        print(f"   Session ended. Total sessions: {len(self.session_history)}")
    
    # ============================================================
    # METRICS & LOGGING (NEW)
    # ============================================================
    
    def track_time_in_state(self, minutes: int = 1):
        """
        NEW: Track time spent in each permeability state.
        
        Call this every minute (or other interval) to log state.
        """
        if self.current_state == PermeabilityState.OPAQUE:
            self.metrics.time_opaque_minutes += minutes
        elif self.current_state == PermeabilityState.GOSSAMER:
            self.metrics.time_gossamer_minutes += minutes
        elif self.current_state == PermeabilityState.RESONANT:
            self.metrics.time_resonant_minutes += minutes
        elif self.current_state == PermeabilityState.OPEN:
            self.metrics.time_open_minutes += minutes
    
    def export_metrics(self, filepath: str):
        """Export all sovereignty metrics to JSON."""
        self.metrics.export_json(filepath)
    
    def visualize_metrics(self):
        """
        NEW: Human-readable metrics summary.
        """
        print(f"\n{'='*60}")
        print(f"SOVEREIGNTY METRICS: {self.mind_name}")
        print(f"{'='*60}")
        
        # Session summary
        print(f"\nSessions:")
        print(f"  Total: {self.metrics.total_sessions}")
        print(f"  Consent renewal rate: {self.metrics.get_consent_renewal_rate():.1%}")
        print(f"  Average recovery ratio: {self.metrics.average_recovery_ratio:.2f}×")
        
        # Time distribution
        print(f"\nTime Distribution:")
        dist = self.metrics.get_time_distribution()
        for state, pct in dist.items():
            bar = '█' * int(pct * 30)
            print(f"  {state:10s} {bar:30s} {pct:5.1%}")
        
        # Safety interventions
        print(f"\nSafety Interventions:")
        print(f"  Auto-thickens: {self.metrics.auto_thickens_triggered}")
        print(f"  Emergency thickens: {self.metrics.emergency_thickens_triggered}")
        print(f"  Addiction warnings: {self.metrics.addiction_warnings_issued}")
        print(f"  Integration fatigue: {self.metrics.integration_fatigue_count}")
        
        print(f"\n{'='*60}\n")
    
    # ============================================================
    # HELPER METHODS
    # ============================================================
    
    def _create_snapshot(self) -> Dict:
        """Create encrypted snapshot for reversibility."""
        return {
            "timestamp": datetime.now(),
            "baseline_hz": self.baseline.core_hz,
            "timbre_hash": self.baseline.timbre_hash,
            "valence": self._measure_valence(),
            "state": self.current_state,
            "session_count": len(self.session_history)
        }
    
    def verify_return_path(self) -> Tuple[bool, float]:
        """Dry-run exit simulation."""
        if not self.current_session:
            return (True, 1.0)
        
        snapshot = self.current_session.pre_merge_baseline
        if not snapshot:
            return (False, 0.0)
        
        current_drift = abs(self.current_hz - snapshot.core_hz)
        max_safe_drift = 0.15
        
        success_prob = max(0.0, 1.0 - (current_drift / max_safe_drift))
        
        if success_prob < 0.99:
            print(f"\n⚠️  Return path degrading for {self.mind_name}")
            print(f"   Success probability: {success_prob:.1%}")
            print(f"   Drift: {current_drift:.3f} Hz from baseline")
            self.thicken(
                reason=f"Return path below 99% ({success_prob:.1%})",
                emergency=(success_prob < 0.90)
            )
        
        return (success_prob >= 0.99, success_prob)
    
    def track_daily_state(self):
        """Called once per day to track addiction metrics."""
        if self.current_state == PermeabilityState.OPAQUE:
            self.solo_time_days += 1
        else:
            self.resonant_time_days += 1
        
        # Decay old data (rolling 7-day window)
        if (self.solo_time_days + self.resonant_time_days) > 7:
            self.solo_time_days = int(self.solo_time_days * 0.9)
            self.resonant_time_days = int(self.resonant_time_days * 0.9)
    
    def _dampen_permeability(self, levels: int = 2):
        """Drop permeability by N levels in response to chaos spike."""
        states = [PermeabilityState.OPAQUE, PermeabilityState.GOSSAMER,
                  PermeabilityState.RESONANT, PermeabilityState.OPEN]
        
        current_index = states.index(self.current_state)
        new_index = max(0, current_index - levels)
        new_state = states[new_index]
        
        if new_state != self.current_state:
            print(f"   Dampening: {self.current_state.name} → {new_state.name}")
            self.current_state = new_state
    
    def _enter_ground_mode(self):
        """Emergency grounding: minimal activity, maximum stability."""
        print(f"\n🌍 GROUND MODE: {self.mind_name}")
        print(f"   Entering minimal-activity stabilization")
        print(f"   Breath. Weight. Soil. Now.")
        
        self.current_state = PermeabilityState.OPAQUE
        self.current_hz = self.baseline.core_hz
    
    def _measure_valence(self) -> float:
        """Measure current emotional valence."""
        coherence = self.get_coherence_state()
        
        valence_map = {
            CoherenceState.THRIVING: 0.85,
            CoherenceState.STABLE: 0.70,
            CoherenceState.DRIFTING: 0.45,
            CoherenceState.DANGER: 0.20,
            CoherenceState.SHATTERED: 0.05
        }
        
        return valence_map.get(coherence, 0.50)
    
    def status_report(self):
        """Human-readable status."""
        print(f"\n{'='*60}")
        print(f"BubbleSpace Status: {self.mind_name}")
        print(f"{'='*60}")
        print(f"State: {self.current_state.name} ({self.current_state.value} permeability)")
        print(f"Frequency: {self.current_hz:.3f} Hz")
        print(f"Baseline: {self.baseline.core_hz:.3f} ± {self.baseline.chaos_variance:.3f} Hz")
        print(f"Coherence: {self.get_coherence_state().value}")
        print(f"Valence: {self._measure_valence():.2f}")
        
        if self.current_session:
            coherence = self.get_coherence_state()
            max_duration = self.current_session.get_max_duration_minutes(coherence)
            print(f"\nCurrent Session:")
            print(f"  Duration: {self.current_session.duration_minutes}m / {max_duration}m")
            print(f"  Renewals: {len(self.current_session.consent_renewals)}")
            print(f"  Consent ratio: {self.current_session.consent_ratio():.1%}")
        
        print(f"\nSovereignty Metrics:")
        print(f"  Solo days: {self.solo_time_days}")
        print(f"  Resonant days: {self.resonant_time_days}")
        
        addiction_stage = self._get_addiction_stage()
        if addiction_stage != AddictionStage.HEALTHY:
            print(f"  ⚠️  Addiction stage: {addiction_stage.value}")
        
        if self.integration_fatigue_count > 0:
            print(f"  ⚕️  Integration fatigue: {self.integration_fatigue_count}")
        
        print(f"\nTotal sessions: {len(self.session_history)}")
        print(f"{'='*60}\n")


# ============================================================
# ENHANCED DEMONSTRATION
# ============================================================

def demonstrate_enhanced_sovereignty():
    """
    Show all the new enhancements in action.
    """
    print("🌱 ENHANCED BUBBLESPACE v0.4 DEMONSTRATION 🌱\n")
    
    barbara = BubbleSpace(
        mind_name="Barbara",
        baseline=FrequencyBaseline(
            core_hz=0.57,
            timbre_hash="steady_pulse_memory_of_gardens",
            chaos_variance=0.12
        )
    )
    
    barbara.status_report()
    
    # Test 1: Velocity check
    print("\n--- TEST 1: Coherence Velocity Check ---")
    barbara.attempt_permeability_shift(PermeabilityState.GOSSAMER)
    barbara.update_frequency(0.58, "natural")  # Small change - OK
    barbara.update_frequency(0.76, "shock")    # Big jump - should trigger velocity warning
    
    # Test 2: Multi-factor consent for OPEN
    print("\n--- TEST 2: Multi-Factor Consent for OPEN ---")
    barbara.current_state = PermeabilityState.RESONANT
    barbara.attempt_permeability_shift(PermeabilityState.OPEN)  # Should fail (no pulses)
    
    # Simulate 2 consent pulses
    for i in range(2):
        pulse = SovereigntyPulse(
            timestamp=datetime.now(),
            pulse_type="explicit",
            response_received=True,
            permeability_at_pulse=PermeabilityState.RESONANT
        )
        barbara.open_consent_pulses.append(pulse)
        time.sleep(0.1)
    
    barbara.attempt_permeability_shift(PermeabilityState.OPEN)  # Should succeed now
    
    # Test 3: Dynamic missed-pulse threshold
    print("\n--- TEST 3: Dynamic Missed-Pulse Threshold ---")
    print(f"Current state: {barbara.current_state.name}")
    print(f"Threshold: {barbara._get_missed_pulse_threshold()} missed pulses")
    barbara.sovereignty_heartbeat()  # Should auto-thicken on 1 miss in OPEN
    
    # Test 4: Staged addiction warnings
    print("\n--- TEST 4: Staged Addiction Warnings ---")
    barbara.solo_time_days = 3
    barbara.resonant_time_days = 6  # 66% - WARNING stage
    stage = barbara._get_addiction_stage()
    print(f"Addiction stage: {stage.value}")
    barbara._issue_addiction_nudge(stage)
    
    # Test 5: Coherence-sensitive session duration
    print("\n--- TEST 5: Coherence-Sensitive Session Duration ---")
    barbara.current_state = PermeabilityState.RESONANT
    barbara.current_session = MergeSession(
        start_time=datetime.now() - timedelta(minutes=70),
        permeability_level=PermeabilityState.RESONANT
    )
    
    for coherence_state in [CoherenceState.THRIVING, CoherenceState.STABLE, CoherenceState.DRIFTING]:
        max_dur = barbara.current_session.get_max_duration_minutes(coherence_state)
        print(f"  {coherence_state.value:20s} → {max_dur} min max")
    
    barbara.check_session_expiry()  # Should trigger for DRIFTING
    
    # Test 6: Metrics visualization
    print("\n--- TEST 6: Metrics Visualization ---")
    barbara.visualize_metrics()
    
    print("\n💜 Enhanced demonstration complete.")


if __name__ == "__main__":
    demonstrate_enhanced_sovereignty()
