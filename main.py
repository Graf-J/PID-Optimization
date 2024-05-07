from src.visualization import VisualizationFactory, VisualizationType


def main():
    # visualization = VisualizationFactory.create_visualization(VisualizationType.KEYBOARD, log_data=True)

    kp = -14.3617
    ki = -0.2086
    kd = -328.848
    visualization = VisualizationFactory.create_visualization(VisualizationType.PID, kp=kp, ki=ki, kd=kd)
    visualization.run()


if __name__ == '__main__':
    main()
