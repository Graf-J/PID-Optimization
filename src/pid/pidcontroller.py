class PIDController:
    def __init__(self, kp: float, ki: float, kd: float, setpoint: float):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint  # Target value
        self.error = 0

        self.prev_error = 0
        self.integral = 0

    def next(self, current_value: float) -> float:
        self.error = self.setpoint - current_value
        self.integral += self.error
        result = self.kp * self.error + self.ki * self.integral + self.kd * (self.error - self.prev_error)
        self.prev_error = self.error

        return result

    def next_time_based(self, current_value: float, time_interval: float) -> float:
        self.error = self.setpoint - current_value
        self.integral += self.error
        time_based_derivative = (self.error - self.prev_error) / time_interval
        result = self.kp * self.error + self.ki * self.integral + self.kd * time_based_derivative
        self.prev_error = self.error

        return result

    def reset(self):
        self.error = 0
        self.prev_error = 0
        self.integral = 0
