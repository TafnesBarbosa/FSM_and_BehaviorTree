import random
import math
from constants import *


class FiniteStateMachine(object):
    """
    A finite state machine.
    """
    def __init__(self, state):
        self.state = state

    def change_state(self, new_state):
        self.state = new_state

    def update(self, agent):
        self.state.check_transition(agent, self)
        self.state.execute(agent)


class State(object):
    """
    Abstract state class.
    """
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def check_transition(self, agent, fsm):
        """
        Checks conditions and execute a state transition if needed.

        :param agent: the agent where this state is being executed on.
        :param fsm: finite state machine associated to this state.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the state logic.

        :param agent: the agent where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class MoveForwardState(State):
    def __init__(self):
        super().__init__("MoveForward")
        # Todo: add initialization code
        self.number_calls = 0

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.number_calls > MOVE_FORWARD_TIME * FREQUENCY:
            state_machine.change_state(MoveInSpiralState())
        elif agent.get_bumper_state():
            state_machine.change_state(GoBackState())
        

    def execute(self, agent):
        # Todo: add execution logic
        self.number_calls += 1
        agent.set_velocity(FORWARD_SPEED, 0)


class MoveInSpiralState(State):
    def __init__(self):
        super().__init__("MoveInSpiral")
        # Todo: add initialization code
        self.number_calls = 0
        self.spiral_radius = INITIAL_RADIUS_SPIRAL
    
    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.number_calls > MOVE_IN_SPIRAL_TIME * FREQUENCY:
            state_machine.change_state(MoveForwardState())
        elif agent.get_bumper_state():
            state_machine.change_state(GoBackState())

    def execute(self, agent):
        # Todo: add execution logic
        self.number_calls += 1
        self.spiral_radius += SAMPLE_TIME * SPIRAL_FACTOR
        agent.set_velocity(FORWARD_SPEED, FORWARD_SPEED / self.spiral_radius)


class GoBackState(State):
    def __init__(self):
        super().__init__("GoBack")
        # Todo: add initialization code
        self.number_calls = 0

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.number_calls > GO_BACK_TIME * FREQUENCY:
            state_machine.change_state(RotateState())

    def execute(self, agent):
        # Todo: add execution logic
        self.number_calls += 1
        agent.set_velocity(BACKWARD_SPEED, 0)


class RotateState(State):
    def __init__(self):
        super().__init__("Rotate")
        # Todo: add initialization code
        self.number_calls = 0
        self.angle = random.random() * 2 * math.pi - math.pi

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.number_calls * SAMPLE_TIME * ANGULAR_SPEED > self.angle:
            state_machine.change_state(MoveForwardState())
    
    def execute(self, agent):
        # Todo: add execution logic
        self.number_calls += 1
        agent.set_velocity(0, ANGULAR_SPEED)
