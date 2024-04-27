class PIDController:
    def __init__(self, kp: float, ki: float, kd: float, setpoint: float):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint  # Target value

        self.prev_error = 0
        self.integral = 0

    def next(self, value: float) -> float:
        error = self.setpoint - value
        self.integral += error

        result = self.kp * error + self.ki * self.integral + self.kd * (error - self.prev_error)

        self.prev_error = error

        return result
